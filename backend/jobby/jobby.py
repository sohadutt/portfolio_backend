import json
import time
from pathlib import Path
from typing import Any, Dict, List

from django.conf import settings
from django.db import transaction
from django.utils import timezone
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from portfolio_form.models import PortfolioSettings

from .models import Job, PortfolioJobMatch

load_dotenv()

JOB_ENRICHMENT_PROMPT = """
You are a job classification assistant.

Analyze the following jobs and extract stable job-level metadata only.
Do not compare the jobs to any user portfolio.

Return ONLY a valid JSON array. Do not include markdown formatting, comments, or backticks.
Each object must contain EXACTLY these keys:
- "job_id": The exact string job_id provided for the job.
- "tags": A concise list of stable job tags, such as skills, role family, tools, domain, seniority, and work type.
- "ai_metadata": An object with compact stable metadata. Use keys like role_family, seniority, primary_skills, domain, tools, and location_type when known.

Jobs: {jobs}
"""

MATCH_ONLY_PROMPT = """
You are a portfolio-to-job matching assistant.

User Portfolio: {portfolio}

Score how well each compact job record matches the user's portfolio.
The jobs already contain stable AI tags and metadata, so do not infer or return tags.

Return ONLY a valid JSON array. Do not include markdown formatting, comments, backticks, explanations, or extra keys.
Each object must contain EXACTLY these keys:
- "job_id": The exact string job_id provided for the job. Do not change it.
- "match_score": A float between 0 and 100.

Jobs: {jobs}
"""


def _truncate(value: Any, limit: int) -> str:
    text = str(value or "").strip()
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0]


def _json_file_path(file_path: str | Path) -> Path:
    path = Path(file_path)
    if path.is_absolute():
        return path
    return Path(settings.BASE_DIR) / path


def _clean_ai_json(raw_text: str) -> list[dict[str, Any]]:
    cleaned = raw_text.replace("```json", "").replace("```", "").strip()
    parsed = json.loads(cleaned)
    if isinstance(parsed, dict):
        parsed = parsed.get("jobs") or parsed.get("results") or []
    if not isinstance(parsed, list):
        return []
    return [item for item in parsed if isinstance(item, dict)]


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
        self._model = None

    @property
    def model(self):
        if self._model is None:
            print(f"[{time.strftime('%H:%M:%S')}] Initializing Google Gemini AI Model...")
            self._model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
        return self._model

    def _invoke(self, prompt: str) -> str:
        for attempt in range(3):
            try:
                response = self.model.invoke([HumanMessage(content=prompt)])
                return response.content
            except Exception as e:
                print(f"[!] Gemini attempt {attempt + 1} failed: {e}")
                time.sleep(5)
        return "[]"

    def analyze_job_enrichment(self, jobs: list[dict[str, Any]]) -> str:
        prompt = JOB_ENRICHMENT_PROMPT.format(jobs=json.dumps(jobs, ensure_ascii=True))
        return self._invoke(prompt)

    def analyze_match_scores(self, portfolio: dict[str, Any], jobs: list[dict[str, Any]]) -> str:
        prompt = MATCH_ONLY_PROMPT.format(
            portfolio=json.dumps(portfolio, ensure_ascii=True),
            jobs=json.dumps(jobs, ensure_ascii=True),
        )
        return self._invoke(prompt)

    def analyze_job(self, job_data: Dict) -> str:
        return self.analyze_match_scores(
            portfolio=job_data.get("portfolio", {}),
            jobs=job_data.get("jobs", []),
        )


class JsonUpdater:
    def __init__(self):
        # OPTIMIZATION: Cache file contents so we don't hit the disk on every batch
        self._cache: Dict[str, Dict[str, Any]] = {}

    def _get_cache(self, path: Path) -> Dict[str, Any]:
        path_str = str(path)
        if path_str not in self._cache:
            try:
                with path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._cache[path_str] = {str(item.get("job_id")): item for item in data if item.get("job_id")}
            except (FileNotFoundError, json.JSONDecodeError):
                self._cache[path_str] = {}
        return self._cache[path_str]

    def get_existing_job_ids(self, file_path: str | Path) -> set[str]:
        print(f"[{time.strftime('%H:%M:%S')}] Scanning existing JSON file for processed IDs...")
        cache = self._get_cache(_json_file_path(file_path))
        print(f"[{time.strftime('%H:%M:%S')}] Found {len(cache)} processed jobs in JSON.")
        return set(cache.keys())

    def update_json_file(self, file_path: str | Path, new_data: List[Dict]):
        if not new_data:
            return

        resolved_path = _json_file_path(file_path)
        cache = self._get_cache(resolved_path)

        for item in new_data:
            if item.get("job_id"):
                cache[str(item["job_id"])] = item

        # Write the cached dictionary directly to disk once
        with resolved_path.open("w", encoding="utf-8") as f:
            json.dump(list(cache.values()), f, indent=4)
            print(f"[*] Successfully updated {resolved_path.name} with {len(new_data)} jobs.")


class AddJobdata:
    def __init__(self, job_store: JobStore):
        self.job_store = job_store

    def _add_job(self, name: str):
        filename = _json_file_path(f"{name}_jobs_output.json")
        print(f"[{time.strftime('%H:%M:%S')}] Reading raw scraped jobs from {filename.name}...")
        try:
            with filename.open("r", encoding="utf-8") as f:
                job_data_list = json.load(f)
            for job in job_data_list:
                self.job_store.add_job(job)
            print(f"[{time.strftime('%H:%M:%S')}] Loaded {len(job_data_list)} raw jobs into memory.")
        except json.JSONDecodeError:
            print(f"[!] Failed to decode JSON from {filename}.")
        except FileNotFoundError:
            print(f"[!] File {filename} not found.")


class DatabaseUpdater:
    @staticmethod
    def _job_id_from_raw(raw_job: dict[str, Any]) -> str:
        return str(raw_job.get("job_id") or "").strip()

    @staticmethod
    def _clean_score(score: Any) -> float:
        try:
            cleaned = float(score)
        except (TypeError, ValueError):
            return 0.0
        return max(0.0, min(100.0, cleaned))

    @staticmethod
    def _job_defaults(raw_job: dict[str, Any]) -> dict[str, Any]:
        return {
            "title": raw_job.get("title") or "Unknown Title",
            "company": raw_job.get("hiring_organization") or raw_job.get("company") or "Unknown Company",
            "location": raw_job.get("location") or "",
            "url": raw_job.get("url") or "",
            "date_posted": str(raw_job.get("date_posted") or ""),
        }

    @classmethod
    def save_raw_jobs_to_db(cls, raw_jobs: List[Dict], site_name: str) -> int:
        """
        OPTIMIZATION: Uses bulk_create to save hundreds of jobs instantly.
        """
        print(f"[{time.strftime('%H:%M:%S')}] Checking database for missing raw jobs...")
        
        # 1. Fetch exactly what exists right now
        existing_ids = set(Job.objects.filter(platform_name__iexact=site_name).values_list('platform_job_id', flat=True))
        
        # 2. Prepare only the missing jobs
        new_jobs_to_create = []
        seen_in_batch = set()
        
        for raw_job in raw_jobs:
            job_id = cls._job_id_from_raw(raw_job)
            if not job_id or job_id == "None" or job_id in existing_ids or job_id in seen_in_batch:
                continue
                
            seen_in_batch.add(job_id)
            defaults = cls._job_defaults(raw_job)
            new_jobs_to_create.append(
                Job(platform_name=site_name, platform_job_id=job_id, **defaults)
            )

        # 3. Fire a single fast query
        if new_jobs_to_create:
            Job.objects.bulk_create(new_jobs_to_create, ignore_conflicts=True)
            print(f"[{time.strftime('%H:%M:%S')}] Inserted {len(new_jobs_to_create)} NEW raw jobs into DB.")
        else:
            print(f"[{time.strftime('%H:%M:%S')}] DB is up to date (no new raw jobs).")
            
        return len(new_jobs_to_create)

    @classmethod
    def save_enriched_jobs_to_db(cls, raw_jobs: List[Dict], ai_enrichments: List[Dict], site_name: str) -> int:
        """
        OPTIMIZATION: Uses bulk_update instead of looping update_or_create.
        """
        enrichment_lookup = {
            str(item.get("job_id")): item
            for item in ai_enrichments
            if item.get("job_id")
        }

        if not enrichment_lookup:
            return 0
            
        # 1. Fetch exactly the jobs we need to update in one query
        jobs_to_update = list(Job.objects.filter(
            platform_name__iexact=site_name, 
            platform_job_id__in=enrichment_lookup.keys()
        ))
        
        # 2. Mutate in memory
        now = timezone.now()
        for job in jobs_to_update:
            enrichment = enrichment_lookup[str(job.platform_job_id)]
            job.tags = enrichment.get("tags") or []
            job.ai_metadata = enrichment.get("ai_metadata") or {}
            job.ai_processed_at = now
            
        # 3. Update all rows in one swift DB hit
        if jobs_to_update:
            Job.objects.bulk_update(jobs_to_update, ['tags', 'ai_metadata', 'ai_processed_at'])
            
        return len(jobs_to_update)

    @classmethod
    def save_match_scores_to_db(cls, ai_matches: List[Dict], portfolio_id: int, site_name: str) -> int:
        try:
            portfolio_instance = PortfolioSettings.objects.get(id=portfolio_id)
        except PortfolioSettings.DoesNotExist:
            print(f"[!] Portfolio ID {portfolio_id} not found. Skipping DB update.")
            return 0

        match_lookup = {
            str(match.get("job_id")): match
            for match in ai_matches
            if match.get("job_id")
        }
        if not match_lookup:
            return 0

        jobs_by_platform_id = {
            str(job.platform_job_id): job
            for job in Job.objects.filter(
                platform_name__iexact=site_name,
                platform_job_id__in=list(match_lookup.keys()),
            )
        }

        saved_count = 0
        with transaction.atomic():
            for job_id, match_data in match_lookup.items():
                job_obj = jobs_by_platform_id.get(job_id)
                if not job_obj:
                    continue

                PortfolioJobMatch.objects.update_or_create(
                    portfolio=portfolio_instance,
                    job=job_obj,
                    defaults={
                        "match_score": cls._clean_score(match_data.get("match_score", 0)),
                    },
                )
                saved_count += 1
        return saved_count


class JobManager:
    def __init__(self, job_store: JobStore, analyzer: AIJobAnalyzer, json_updater: JsonUpdater, add_jobdata: AddJobdata, db_updater: DatabaseUpdater):
        self.job_store = job_store
        self.analyzer = analyzer
        self.json_updater = json_updater
        self.add_jobdata = add_jobdata
        self.db_updater = db_updater

    @staticmethod
    def _compact_raw_job(raw_job: dict[str, Any]) -> dict[str, Any]:
        return {
            "job_id": str(raw_job.get("job_id") or ""),
            "title": raw_job.get("title") or "",
            "company": raw_job.get("hiring_organization") or raw_job.get("company") or "",
            "location": raw_job.get("location") or "",
            "description": _truncate(raw_job.get("description"), 4500),
            "qualifications": _truncate(raw_job.get("qualifications"), 2500),
            "experience_requirements": _truncate(raw_job.get("experience_requirements"), 2500),
        }

    @staticmethod
    def _compact_enriched_job(job: Job) -> dict[str, Any]:
        metadata = job.ai_metadata if isinstance(job.ai_metadata, dict) else {}
        return {
            "job_id": str(job.platform_job_id),
            "title": job.title,
            "company": job.company,
            "location": job.location or "",
            "tags": job.tags or [],
            "ai_metadata": metadata,
        }

    def process_jobs(
        self,
        portfolio: Dict,
        portfolio_id: int,
        output_file: str,
        batch_size: int = 10,
        site_name: str = "deloitte",
        run_match_after: bool = True,
        match_batch_size: int = 75,
    ):
        print(f"\n[{time.strftime('%H:%M:%S')}] === PHASE 1: LOADING & SYNCING ===")
        self.add_jobdata._add_job(site_name)
        all_jobs = self.job_store.get_jobs()

        if not all_jobs:
            print("[!] No jobs to process.")
            return {"status": "error", "message": "No raw jobs to process.", "enriched": 0, "matched": 0}

        self.db_updater.save_raw_jobs_to_db(all_jobs, site_name)

        print(f"\n[{time.strftime('%H:%M:%S')}] === PHASE 2: FILTERING PRE-ENRICHED JOBS ===")
        existing_file_ids = self.json_updater.get_existing_job_ids(output_file)
        
        print(f"[{time.strftime('%H:%M:%S')}] Querying DB for existing enriched jobs...")
        existing_db_ids = set(
            Job.objects.filter(platform_name__iexact=site_name, ai_processed_at__isnull=False)
            .values_list("platform_job_id", flat=True)
        )
        
        existing_ids = {str(job_id) for job_id in existing_file_ids | existing_db_ids}
        jobs = [job for job in all_jobs if str(job.get("job_id")) not in existing_ids]

        skipped_count = len(all_jobs) - len(jobs)
        print(f"[*] Found {len(all_jobs)} total raw jobs.")
        print(f"[*] Skipping {skipped_count} already enriched jobs.")
        print(f"[*] Proceeding to enrich {len(jobs)} new jobs.")

        enriched_count = 0
        if jobs:
            print(f"\n[{time.strftime('%H:%M:%S')}] === PHASE 3: AI ENRICHMENT ===")
            total_jobs = len(jobs)
            total_batches = (total_jobs + batch_size - 1) // batch_size
            start_time_total = time.time()

            for i in range(0, total_jobs, batch_size):
                batch = jobs[i : i + batch_size]
                current_batch_num = (i // batch_size) + 1

                print(f"\n[{time.strftime('%H:%M:%S')}] Enriching batch {current_batch_num}/{total_batches} ({len(batch)} jobs)...")

                compact_batch = [self._compact_raw_job(job) for job in batch]
                start_ai = time.time()
                analysis_result = self.analyzer.analyze_job_enrichment(compact_batch)
                print(f"[{time.strftime('%H:%M:%S')}] AI enrichment for batch {current_batch_num} took {time.time() - start_ai:.2f}s.")

                try:
                    analysis_json = _clean_ai_json(analysis_result)
                    if not analysis_json:
                        print(f"[!] AI returned no valid enrichment rows for batch {current_batch_num}. Skipping batch.")
                        continue

                    print(f"[{time.strftime('%H:%M:%S')}] Saving enriched batch {current_batch_num} to JSON and database...")
                    self.json_updater.update_json_file(output_file, analysis_json)
                    enriched_count += self.db_updater.save_enriched_jobs_to_db(
                        raw_jobs=batch,
                        ai_enrichments=analysis_json,
                        site_name=site_name,
                    )
                    print(f"[{time.strftime('%H:%M:%S')}] Enrichment batch {current_batch_num} completed successfully.")
                    time.sleep(1)

                except json.JSONDecodeError:
                    print(f"[!] Failed to decode JSON for enrichment batch {current_batch_num}. Skipping.")
                    print(f"Raw output snippet: {analysis_result[:200]}")

            total_duration = time.time() - start_time_total
            print(f"\n[*] Finished enriching new jobs in {total_duration:.2f} seconds.")
        else:
            print("[*] All jobs are already enriched.")

        matched_count = 0
        if run_match_after:
            print(f"\n[{time.strftime('%H:%M:%S')}] === PHASE 4: PORTFOLIO MATCHING ===")
            match_result = self.process_match_only(
                portfolio=portfolio,
                portfolio_id=portfolio_id,
                site_name=site_name,
                batch_size=match_batch_size,
            )
            matched_count = int(match_result.get("matched", 0))

        return {
            "status": "success",
            "site_name": site_name,
            "enriched": enriched_count,
            "matched": matched_count,
        }

    def process_match_only(
        self,
        portfolio: Dict,
        portfolio_id: int,
        site_name: str = "deloitte",
        output_file: str | None = None,
        batch_size: int = 75,
        rematch_existing: bool = False,
    ) -> dict[str, Any]:
        if output_file is None:
            output_file = f"{site_name}_matches_portfolio_{portfolio_id}_output.json"

        jobs_query = Job.objects.filter(platform_name__iexact=site_name).exclude(tags=[])
        jobs = list(jobs_query.order_by("platform_job_id"))
        if not jobs:
            message = f"No enriched jobs found for {site_name}. Run full processing first."
            print(f"[!] {message}")
            return {"status": "error", "message": message, "matched": 0}

        if not rematch_existing:
            print(f"[{time.strftime('%H:%M:%S')}] Checking DB for jobs already matched to Portfolio {portfolio_id}...")
            existing_job_ids = set(
                PortfolioJobMatch.objects.filter(
                    portfolio_id=portfolio_id,
                    job__platform_name__iexact=site_name,
                ).values_list("job__platform_job_id", flat=True)
            )
            jobs = [job for job in jobs if str(job.platform_job_id) not in existing_job_ids]

        if not jobs:
            print("[*] All enriched jobs already have match scores for this portfolio.")
            return {"status": "success", "site_name": site_name, "matched": 0}

        total_jobs = len(jobs)
        total_batches = (total_jobs + batch_size - 1) // batch_size
        matched_count = 0
        start_time_total = time.time()

        print(f"[*] Proceeding to score {total_jobs} enriched jobs for portfolio {portfolio_id}.")

        for i in range(0, total_jobs, batch_size):
            batch = jobs[i : i + batch_size]
            current_batch_num = (i // batch_size) + 1
            compact_batch = [self._compact_enriched_job(job) for job in batch]

            print(f"\n[{time.strftime('%H:%M:%S')}] Scoring batch {current_batch_num}/{total_batches} ({len(batch)} jobs)...")

            start_ai = time.time()
            analysis_result = self.analyzer.analyze_match_scores(portfolio=portfolio, jobs=compact_batch)
            print(f"[{time.strftime('%H:%M:%S')}] AI match scoring for batch {current_batch_num} took {time.time() - start_ai:.2f}s.")

            try:
                analysis_json = _clean_ai_json(analysis_result)
                if not analysis_json:
                    print(f"[!] AI returned no valid score rows for batch {current_batch_num}. Skipping batch.")
                    continue

                self.json_updater.update_json_file(output_file, analysis_json)
                matched_count += self.db_updater.save_match_scores_to_db(
                    ai_matches=analysis_json,
                    portfolio_id=portfolio_id,
                    site_name=site_name,
                )
                print(f"[{time.strftime('%H:%M:%S')}] Match batch {current_batch_num} completed successfully.")
                time.sleep(1)

            except json.JSONDecodeError:
                print(f"[!] Failed to decode JSON for match batch {current_batch_num}. Skipping.")
                print(f"Raw output snippet: {analysis_result[:200]}")

        total_duration = time.time() - start_time_total
        print(f"\n[*] Finished scoring jobs in {total_duration:.2f} seconds.")
        return {
            "status": "success",
            "site_name": site_name,
            "matched": matched_count,
        }