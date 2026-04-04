from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import User

@shared_task
def send_otp_email_task(email, secure_otp):
    """
    Background task to send the OTP email.
    """
    try:
        send_mail(
            subject="Your OTP Code",
            message=f"Your OTP code is: {secure_otp}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False, 
        )
        return f"OTP sent to {email}"
    except Exception as e:
        # In a real app, you might want to log this error using Python's logging module
        return f"Failed to send email to {email}: {str(e)}"
    
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