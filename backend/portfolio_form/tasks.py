from __future__ import annotations

import os
import vercel_blob
import smtplib
from collections import defaultdict
from celery import Task, shared_task
from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from .models import ContactFormSubmission, User, PortfolioSettings
from ..jobby.spiders.scraper_manager import ScraperManager
from ..jobby.jobby import JobStore, AIJobAnalyzer, JsonUpdater, AddJobdata, JobManager, DatabaseUpdater

@shared_task(bind=True, max_retries=3)
def send_otp_email_task(self: Task, email: str, secure_otp: str, subject: str = "Your OTP Code") -> str:
    try:
        send_mail(
            subject=subject,
            message=f"Your OTP code is: {secure_otp} \nThis code is valid for 3 minutes. \n Thank you for checking out my app - if you have any feedback or suggestions, or you want to support please let me know! \n\nBest regards,\nSoham Dutta",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False, 
        )
        return f"OTP sent to {email}"
        
    except smtplib.SMTPException as exc:
        raise self.retry(exc=exc, countdown=60)
        
    except Exception:
        raise
    
@shared_task
def cleanup_unverified_users() -> str:
    threshold = timezone.now() - timedelta(days=1)
    
    unverified_users = User.objects.filter(
        created_at__lt=threshold,
        is_verified=False,
        is_superuser=False
    )
    
    count = unverified_users.count()
    unverified_users.delete()
    
    return f"Deleted {count} unverified users."

@shared_task
def process_daily_urgent_notifications() -> str:
    urgent_subs = ContactFormSubmission.objects.filter(
        is_dismissed=False,
        priority=3 
    ).select_related('owner')

    if not urgent_subs.exists():
        return "No urgent submissions found today."

    user_submissions: defaultdict[User, list[ContactFormSubmission]] = defaultdict(list)
    for sub in urgent_subs:
        user_submissions[sub.owner].append(sub)

    emails_sent = 0
    for owner, subs in user_submissions.items():
        subject = f"Action Required: {len(subs)} Urgent Portfolio Submissions"

        message = f"Hello {owner.first_name or owner.username},\n\n"
        message += f"You have {len(subs)} URGENT contact form submissions waiting for your response:\n\n"
        
        for s in subs:
            message += f"- From: {s.name} ({s.email})\n"
            message += f"  Message: {s.message[:100]}...\n\n"
            
        message += "Please log in to your dashboard to view the full details and dismiss them to stop these alerts.\n"

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[owner.email],
                fail_silently=False, 
            )
            emails_sent += 1
        except Exception as e:
            print(f"Failed to send urgent digest to {owner.email}: {e}")

    return f"Sent urgent digests to {emails_sent} users."

@shared_task
def async_upload_profile_picture(user_id: int, temp_file_path: str, filename: str, old_url: str | None = None) -> None:
    try:
        with open(temp_file_path, 'rb') as f:
            resp = vercel_blob.put(
                path=f"profile_pics/{filename}", 
                data=f.read(), 
                options={
                    "access": "public",
                    "content_type": "image/webp"
                }
            )
        
        user = User.objects.get(id=user_id)
        user.profile_picture_url = resp["url"]
        user.save(update_fields=["profile_picture_url"])

        if old_url and "vercel-storage.com" in old_url:
            try:
                vercel_blob.delete(old_url)
            except Exception:
                pass
                
    except Exception as e:
        print(f"Failed to async upload profile picture: {e}")
        
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


@shared_task
def async_upload_resume(portfolio_id: int, temp_file_path: str, filename: str, old_url: str | None = None) -> None:
    try:
        with open(temp_file_path, 'rb') as f:
            resp = vercel_blob.put(
                path=f"resumes/{filename}", 
                data=f.read(), 
                options={
                    "access": "public",
                    "content_type": "application/pdf"
                }
            )     
        portfolio = PortfolioSettings.objects.get(id=portfolio_id)
        portfolio.resume_url = resp["url"]
        portfolio.save(update_fields=["resume_url"])

        if old_url and "vercel-storage.com" in old_url:
            try:
                vercel_blob.delete(old_url)
            except Exception:
                pass
        
    except Exception as e:
        print(f"Failed to async upload resume: {e}")
        
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@shared_task(bind=True)
def run_job_pipeline(self, site_name: str, run_scraper: bool, run_processor: bool, portfolio_id: int):
    if run_scraper:
        scraper = ScraperManager(site_name=site_name)
        scraper.run_scraper()
        
    if run_processor:
        try:
            portfolio_obj = PortfolioSettings.objects.get(id=portfolio_id)
        except PortfolioSettings.DoesNotExist:
            return {"status": "error", "message": f"Portfolio {portfolio_id} not found."}

        portfolio_dict = {
            "title": getattr(portfolio_obj, 'title', ''),
            "skills": [skill.name for skill in portfolio_obj.skillgroups.all()],
            "experience": [exp.description for exp in portfolio_obj.experiences.all()],
            "projects": [proj.description for proj in portfolio_obj.projects.all()]
        }

        job_store = JobStore()
        analyzer = AIJobAnalyzer()
        json_updater = JsonUpdater()
        db_updater = DatabaseUpdater()
        add_jobdata = AddJobdata(job_store)
        
        manager = JobManager(job_store, analyzer, json_updater, add_jobdata, db_updater)
        output_file = f"{site_name}_matches_output.json"
        
        manager.process_jobs(
            portfolio=portfolio_dict, 
            portfolio_id=portfolio_id,
            output_file=output_file, 
            batch_size=10, 
            site_name=site_name
        )
        
    return {"status": "success", "site_name": site_name}