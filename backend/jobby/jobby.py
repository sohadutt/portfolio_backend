import json
import time
from typing import List, Dict
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from django.db import transaction
from .models import Job, PortfolioJobMatch
from portfolio_form.models import PortfolioSettings 

load_dotenv()

MAIN_PROCESS_PROMPT = """
You are a job matching assistant.
User Portfolio: {portfolio}

Analyze the following batch of job descriptions. 
For each job, determine how well it matches the user's portfolio.

Return ONLY a valid JSON array of objects. Do not include markdown formatting or backticks.
Each object must contain EXACTLY these keys:
- "job_id": The exact string job_id provided in the job description.
- "match_score": A float between 0 and 100.
- "tags": A list of relevant string tags.

Job Descriptions: {jobs}
"""

class JobStore:
    def __init__(self):
        self.jobs: List[Dict] = []

    def add_job(self, job_data: Dict):
        self.jobs.append(job_data)

    def get_jobs(self) -> List[Dict]:
        return self.jobs

    def clear_jobs(self):
        self.jobs.clear()

class AIJobAnalyzer:
    def __init__(self):
        self.model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    def analyze_job(self, job_data: Dict) -> str:
        prompt = MAIN_PROCESS_PROMPT.format(
            portfolio=json.dumps(job_data.get('portfolio', {})),
            jobs=json.dumps(job_data.get('jobs', []))
        )
        
        for attempt in range(3):
            try:
                response = self.model.invoke([HumanMessage(content=prompt)]) 
                return response.content
            except Exception as e:
                print(f"[!] Gemini attempt {attempt+1} failed: {e}")
                time.sleep(5)
        return "[]"
    
class JsonUpdater:
    @staticmethod
    def get_existing_job_ids(file_path: str) -> set:
        """Reads the existing JSON and returns a set of already processed job_ids."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return {str(item.get('job_id')) for item in data if item.get('job_id')}
        except (FileNotFoundError, json.JSONDecodeError):
            return set()

    @staticmethod
    def update_json_file(file_path: str, new_data: List[Dict]):
        if not new_data:
            return

        existing_data = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        merged_dict = {str(item.get('job_id')): item for item in existing_data if item.get('job_id')}
        
        for item in new_data:
            if item.get('job_id'):
                merged_dict[str(item['job_id'])] = item 
                
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(list(merged_dict.values()), f, indent=4)
            print(f"[*] Successfully updated {file_path} with {len(new_data)} jobs.")

class AddJobdata:
    def __init__(self, job_store: JobStore):
        self.job_store = job_store

    def _add_job(self, name: str):
        filename = f"{name}_jobs_output.json" 
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                job_data_list = json.load(f)
            for job in job_data_list:
                self.job_store.add_job(job)
        except json.JSONDecodeError:
            print(f"[!] Failed to decode JSON from {filename}.")
        except FileNotFoundError:
            print(f"[!] File {filename} not found.")

class DatabaseUpdater:
    @staticmethod
    def save_batch_to_db(raw_jobs: List[Dict], ai_matches: List[Dict], portfolio_id: int, site_name: str):
        """
        Saves the raw jobs to the Job model, and the AI matches to the PortfolioJobMatch model.
        """
        try:
            portfolio_instance = PortfolioSettings.objects.get(id=portfolio_id)
        except PortfolioSettings.DoesNotExist:
            print(f"[!] Portfolio ID {portfolio_id} not found. Skipping DB update.")
            return

        match_lookup = {str(match.get('job_id')): match for match in ai_matches if match.get('job_id')}

        with transaction.atomic():
            for raw_job in raw_jobs:
                job_id = str(raw_job.get('job_id'))
                if not job_id or job_id == "None":
                    continue

                job_obj, _ = Job.objects.update_or_create(
                    platform_name=site_name,
                    platform_job_id=job_id,
                    defaults={
                        'title': raw_job.get('title') or 'Unknown Title',
                        'company': raw_job.get('hiring_organization') or 'Unknown Company',
                        'location': raw_job.get('location') or '',
                        'url': raw_job.get('url') or '',
                        'date_posted': str(raw_job.get('date_posted') or '')
                    }
                )

                if job_id in match_lookup:
                    match_data = match_lookup[job_id]
                    
                    PortfolioJobMatch.objects.update_or_create(
                        portfolio=portfolio_instance,
                        job=job_obj,
                        defaults={
                            'match_score': match_data.get('match_score', 0),
                            'tags': match_data.get('tags', [])
                        }
                    )

class JobManager:
    def __init__(self, job_store: JobStore, analyzer: AIJobAnalyzer, json_updater: JsonUpdater, add_jobdata: AddJobdata, db_updater: DatabaseUpdater):
        self.job_store = job_store
        self.analyzer = analyzer
        self.json_updater = json_updater
        self.add_jobdata = add_jobdata
        self.db_updater = db_updater

    def process_jobs(self, portfolio: Dict, portfolio_id: int, output_file: str, batch_size: int = 10, site_name: str = "deloitte"):
        self.add_jobdata._add_job(site_name)
        all_jobs = self.job_store.get_jobs()
        
        if not all_jobs:
            print("[!] No jobs to process.")
            return            

        existing_ids = self.json_updater.get_existing_job_ids(output_file)
        jobs = [job for job in all_jobs if str(job.get("job_id")) not in existing_ids]

        skipped_count = len(all_jobs) - len(jobs)
        print(f"[*] Found {len(all_jobs)} total raw jobs.")
        print(f"[*] Skipping {skipped_count} already analyzed jobs.")
        print(f"[*] Proceeding to process {len(jobs)} new jobs.")

        if not jobs:
            print("[*] All jobs are already processed and up to date. Exiting.")
            return
            
        total_jobs = len(jobs)
        total_batches = (total_jobs + batch_size - 1) // batch_size
        
        start_time_total = time.time()

        for i in range(0, total_jobs, batch_size):
            batch = jobs[i : i + batch_size]
            current_batch_num = (i // batch_size) + 1
            
            print(f"\n[{time.strftime('%H:%M:%S')}] Processing batch {current_batch_num}/{total_batches} ({len(batch)} jobs)...")
            
            job_data = {
                "portfolio": portfolio,
                "jobs": batch
            }           
            
            start_ai = time.time()
            analysis_result = self.analyzer.analyze_job(job_data)          
            print(f"[{time.strftime('%H:%M:%S')}] AI Analysis for batch {current_batch_num} took {time.time() - start_ai:.2f}s.")
            
            try:
                cleaned_result = analysis_result.replace('```json', '').replace('```', '').strip()
                analysis_json = json.loads(cleaned_result) # These are the AI MATCHES               
                
                if isinstance(analysis_json, dict):
                    analysis_json = analysis_json.get("jobs", [])
                    
                if not isinstance(analysis_json, list):
                    print(f"[!] AI returned invalid format. Expected list, got {type(analysis_json)}. Skipping batch.")
                    continue

                print(f"[{time.strftime('%H:%M:%S')}] Saving batch {current_batch_num} to JSON and Database...")
                
                self.json_updater.update_json_file(output_file, analysis_json)
                self.db_updater.save_batch_to_db(
                    raw_jobs=batch, 
                    ai_matches=analysis_json, 
                    portfolio_id=portfolio_id, 
                    site_name=site_name
                )
                print(f"[{time.strftime('%H:%M:%S')}] Batch {current_batch_num} completed successfully.")
                time.sleep(2)
                
            except json.JSONDecodeError:
                print(f"[!] Failed to decode JSON for batch {current_batch_num}. Skipping.")
                print(f"Raw output snippet: {analysis_result[:200]}")
                
        total_duration = time.time() - start_time_total
        print(f"\n[*] Finished processing all new jobs in {total_duration:.2f} seconds.")