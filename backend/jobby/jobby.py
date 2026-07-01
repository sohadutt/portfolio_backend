import json
import time
from typing import List, Dict
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from .models import Job, PortfolioJobMatch
from portfolio_form.models import PortfolioSettings

load_dotenv()

MAIN_PROCESS_PROMPT = """
You are a job matching assistant.

User Portfolio:
{portfolio}

Analyze the following batch of job descriptions.
For each job, determine how well it matches the user's portfolio.
Return ONLY valid JSON.

Format:
[
    {{
        "job_id": "exact job_id",
        "match_score": float between 0 and 100,
        "tags": ["relevant skill tags"]
    }}
]

Job Descriptions:
{jobs}
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
        self.model = ChatGoogleGenerativeAI(
            model="gemini-3.1-flash-lite",
            temperature=0.2
        )

    def analyze_job(self, job_data: Dict) -> str:
        for attempt in range(3):
            try:
                prompt = MAIN_PROCESS_PROMPT.format(
                    portfolio=json.dumps(job_data.get("portfolio", {})),
                    jobs=json.dumps(job_data.get("jobs", []))
                )
                response = self.model.invoke([HumanMessage(content=prompt)])
                return response.content
            except Exception as e:
                print(f"Gemini attempt {attempt+1} failed: {e}")
                time.sleep(10)
        return "[]"

class JsonUpdater:
    @staticmethod
    def get_existing_job_ids(file_path: str) -> set:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return {item.get("job_id") for item in json.load(f) if item.get("job_id")}
        except (FileNotFoundError, json.JSONDecodeError):
            return set()

    @staticmethod
    def update_json_file(file_path: str, new_data: List[Dict]):
        if not new_data: return
        existing_data = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        merged = {item["job_id"]: item for item in existing_data if item.get("job_id")}
        for item in new_data:
            if item.get("job_id"):
                merged[item["job_id"]] = item

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(list(merged.values()), f, indent=4)
        print(f"Updated {file_path}")

class AddJobdata:
    def __init__(self, job_store: JobStore):
        self.job_store = job_store

    def _add_job(self, name: str):
        filename = f"{name}_jobs_output.json"
        try:
            with open(filename, "r", encoding="utf-8") as f:
                for job in json.load(f):
                    self.job_store.add_job(job)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error reading {filename}: {e}")

class DatabaseUpdater:
    @staticmethod
    def save_batch_to_db(raw_jobs: List[Dict], ai_matches: List[Dict], portfolio_id: int, site_name: str):
        try:
            portfolio_instance = PortfolioSettings.objects.get(id=portfolio_id)
        except PortfolioSettings.DoesNotExist:
            print(f"Portfolio {portfolio_id} not found")
            return

        match_lookup = {match["job_id"]: match for match in ai_matches if match.get("job_id")}

        for raw_job in raw_jobs:
            job_id = raw_job.get("job_id")
            if not job_id: continue

            job_obj, _ = Job.objects.update_or_create(
                platform_name=site_name,
                platform_job_id=job_id,
                defaults={
                    "title": raw_job.get("title") or "Unknown Title",
                    "company": raw_job.get("hiring_organization") or "Unknown Company",
                    "location": raw_job.get("location") or "",
                    "url": raw_job.get("url") or "",
                    "date_posted": str(raw_job.get("date_posted") or "")
                }
            )

            if job_id in match_lookup:
                match = match_lookup[job_id]
                PortfolioJobMatch.objects.update_or_create(
                    portfolio=portfolio_instance,
                    job=job_obj,
                    defaults={
                        "match_score": match.get("match_score", 0),
                        "tags": match.get("tags", [])
                    }
                )

class JobManager:
    def __init__(self, job_store, analyzer, json_updater, add_jobdata, db_updater):
        self.job_store = job_store
        self.analyzer = analyzer
        self.json_updater = json_updater
        self.add_jobdata = add_jobdata
        self.db_updater = db_updater

    def truncate_text(self, text, max_chars=1200):
        return str(text)[:max_chars] if text else ""

    def prepare_jobs_for_ai(self, jobs: List[Dict]) -> List[Dict]:
        return [{
            "job_id": j.get("job_id"),
            "title": j.get("title"),
            "description": self.truncate_text(j.get("description"), 1200),
            "skills": j.get("skills"),
            "company": j.get("hiring_organization")
        } for j in jobs]

    def process_jobs(self, portfolio: Dict, portfolio_id: int, output_file: str, batch_size: int = 25, site_name: str = "deloitte"):
        self.job_store.clear_jobs()
        self.add_jobdata._add_job(site_name)
        jobs = self.job_store.get_jobs()

        if not jobs:
            print("No jobs found"); return

        existing_ids = self.json_updater.get_existing_job_ids(output_file)
        to_process = [j for j in jobs if j.get("job_id") not in existing_ids]

        print(f"Skipping {len(jobs) - len(to_process)} already analyzed jobs. Processing {len(to_process)} new.")

        for i in range(0, len(to_process), batch_size):
            batch = to_process[i:i + batch_size]
            print(f"Processing batch {(i // batch_size) + 1}...")

            analysis_result = self.analyzer.analyze_job({"portfolio": portfolio, "jobs": self.prepare_jobs_for_ai(batch)})
            
            try:
                cleaned = analysis_result.replace("```json", "").replace("```", "").strip()
                analysis_json = json.loads(cleaned)
                
                self.json_updater.update_json_file(output_file, analysis_json)
                self.db_updater.save_batch_to_db(batch, analysis_json, portfolio_id, site_name)
                time.sleep(3)
            except json.JSONDecodeError:
                print("JSON decode failed for batch.")