from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import User
from .models import ContactFormSubmission
import smtplib

@shared_task(bind=True, max_retries=3)
def send_otp_email_task(self, email, secure_otp):
    try:
        send_mail(
            subject="Your OTP Code",
            message=f"Your OTP code is: {secure_otp} \nThis code is valid for 3 minutes. \n Thank you for checking out my app - if you have any feedback or suggestions, or you want to support please let me know! \n\nBest regards,\nSoham Dutta",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False, 
        )
        return f"OTP sent to {email}"
        
    except smtplib.SMTPException as exc:
        raise self.retry(exc=exc, countdown=60)
        
    except Exception as e:
        raise e
    
@shared_task
def cleanup_unverified_users():
    """Deletes users who haven't verified their email within 24 hours."""
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
def process_daily_urgent_notifications():
    urgent_subs = ContactFormSubmission.objects.filter(
        is_dismissed=False,
        priority=3 
    ).select_related('owner')

    if not urgent_subs.exists():
        return "No urgent submissions found today."

    # Group submissions by the portfolio owner
    user_submissions = {}
    for sub in urgent_subs:
        if sub.owner not in user_submissions:
            user_submissions[sub.owner] = []
        user_submissions[sub.owner].append(sub)

    emails_sent = 0
    for owner, subs in user_submissions.items():
        subject = f"Action Required: {len(subs)} Urgent Portfolio Submissions"
        
        # Build the email body
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