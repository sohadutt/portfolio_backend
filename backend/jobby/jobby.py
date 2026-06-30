import json
from typing import List, Dict
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
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
        self.model = ChatGoogleGenerativeAI()

    def analyze_job(self, job_data: Dict) -> str:
        prompt = MAIN_PROCESS_PROMPT.format(
            portfolio=json.dumps(job_data.get('portfolio', {})),
            jobs=json.dumps(job_data.get('jobs', []))
        )
        response = self.model.invoke([HumanMessage(content=prompt)]) 
        return response.content
    
class JsonUpdater:
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

        merged_dict = {item.get('job_id'): item for item in existing_data if item.get('job_id')}
        
        for item in new_data:
            if item.get('job_id'):
                merged_dict[item['job_id']] = item 
                
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(list(merged_dict.values()), f, indent=4)
            print(f"Successfully updated {file_path} with new job data.")

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
            print(f"Failed to decode JSON from {filename}.")
        except FileNotFoundError:
            print(f"File {filename} not found.")

class JobManager:
    def __init__(self, job_store: JobStore, analyzer: AIJobAnalyzer, json_updater: JsonUpdater, add_jobdata: AddJobdata, db_updater: DatabaseUpdater):
        self.job_store = job_store
        self.analyzer = analyzer
        self.json_updater = json_updater
        self.add_jobdata = add_jobdata
        self.db_updater = db_updater

    def process_jobs(self, portfolio: Dict, portfolio_id: int, output_file: str, batch_size: int = 10, site_name: str = "deloitte"):
        self.add_jobdata._add_job(site_name)
        jobs = self.job_store.get_jobs()
        
        if not jobs:
            print("No jobs to process.")
            return            
        total_jobs = len(jobs)
        for i in range(0, total_jobs, batch_size):
            batch = jobs[i : i + batch_size]
            current_batch_num = (i // batch_size) + 1
            
            job_data = {
                "portfolio": portfolio,
                "jobs": batch
            }           
            analysis_result = self.analyzer.analyze_job(job_data)          
            try:
                cleaned_result = analysis_result.replace('```json', '').replace('```', '').strip()
                analysis_json = json.loads(cleaned_result) # These are the AI MATCHES               
                self.json_updater.update_json_file(output_file, analysis_json)
                self.db_updater.save_batch_to_db(
                    raw_jobs=batch, 
                    ai_matches=analysis_json, 
                    portfolio_id=portfolio_id, 
                    site_name=site_name
                )
                print(f"Batch {current_batch_num} saved to JSON and DB.")
                
            except json.JSONDecodeError:
                print(f"Failed to decode JSON for batch {current_batch_num}. Skipping.")


class DatabaseUpdater:
    @staticmethod
    def save_batch_to_db(raw_jobs: List[Dict], ai_matches: List[Dict], portfolio_id: int, site_name: str):
        """
        Saves the raw jobs to the Job model, and the AI matches to the PortfolioJobMatch model.
        """
        try:
            portfolio_instance = PortfolioSettings.objects.get(id=portfolio_id)
        except PortfolioSettings.DoesNotExist:
            print(f"Portfolio ID {portfolio_id} not found. Skipping DB update.")
            return

        match_lookup = {match.get('job_id'): match for match in ai_matches if match.get('job_id')}

        for raw_job in raw_jobs:
            job_id = raw_job.get('job_id')
            if not job_id:
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