import json
from pathlib import Path
from django.conf import settings
from jobby.models import Job

def run_backfill(site_name: str = "deloitte"):
    file_path = Path(settings.BASE_DIR) / f"{site_name}_jobs_output.json"
    
    if not file_path.exists():
        print(f"[!] Raw jobs file not found: {file_path}")
        return
        
    print(f"[*] Reading raw jobs from {file_path.name}...")
    with file_path.open("r", encoding="utf-8") as f:
        raw_jobs = json.load(f)
        
    # Create a quick lookup dictionary: { "job_id": "description" }
    desc_lookup = {
        str(job.get("job_id")): job.get("description", "")
        for job in raw_jobs
        if job.get("job_id") and job.get("description")
    }
    
    print(f"[*] Fetching existing {site_name} jobs from the database...")
    jobs_in_db = Job.objects.filter(platform_name__iexact=site_name)
    
    jobs_to_update = []
    for job in jobs_in_db:
        new_desc = desc_lookup.get(str(job.platform_job_id))
        
        # Only update if a description exists and it differs from what is currently in the DB
        if new_desc and job.description != new_desc:
            job.description = new_desc
            jobs_to_update.append(job)
            
    if jobs_to_update:
        print(f"[*] Backfilling descriptions for {len(jobs_to_update)} jobs...")
        # Update all records in a single database query
        Job.objects.bulk_update(jobs_to_update, ['description'])
        print("[*] Backfill complete!")
    else:
        print("[*] All jobs are already up to date. No descriptions needed backfilling.")