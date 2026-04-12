import sys
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from portfolio_form.models import User

class Command(BaseCommand):
    help = 'Identifies and deletes unverified users older than the threshold.'

    def handle(self, *args, **options):       
        self.stdout.write(f"Checking for unverified users")

        targets = User.objects.filter(
            is_superuser=False,
            is_verified=False
        ).exclude(is_superuser=True).exclude(is_staff=True)

        count = targets.count()

        if count == 0:
            self.stdout.write(self.style.WARNING("\nNo stale unverified users found."))
            self.stdout.write("Note: Users created in the last 24h are skipped for safety.")
            return

        self.stdout.write(self.style.NOTICE(f"\n[!] Found {count} unverified users to purge:"))
        for user in targets:
            self.stdout.write(f"  ID: {user.id} | Name: {user.username} | Email: {user.email} | Joined: {user.created_at}")

        confirm = input("\nPROMPT: Type 'yes' or 'y' to permanently delete these users: ").lower()

        if confirm == 'yes' or 'y':
            total_deleted, detail_map = targets.delete()
            self.stdout.write(self.style.SUCCESS(f"\nDONE: Purged {total_deleted} total database objects."))
            
            for model_path, amt in detail_map.items():
                model_name = model_path.split('.')[-1]
                self.stdout.write(f"  - {model_name}: {amt}")
        else:
            self.stdout.write(self.style.ERROR("\nABORTED: No changes made to the database."))