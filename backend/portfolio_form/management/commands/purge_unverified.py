import sys
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from portfolio_form.models import User

class Command(BaseCommand):
    help = 'Identifies and deletes unverified users older than the threshold.'

    def handle(self, *args, **options):
        # CHANGE 'days=1' to 'minutes=1' if you want to test with a brand new account!
        threshold = timezone.now() - timedelta(days=1)
        
        self.stdout.write(f"Checking for unverified users created before: {threshold}")

        # 1. Identify the targets
        targets = User.objects.filter(
            created_at__lt=threshold,
            is_verified=False
        ).exclude(is_superuser=True).exclude(is_staff=True)

        count = targets.count()

        # 2. If no users found
        if count == 0:
            self.stdout.write(self.style.WARNING("\nNo stale unverified users found."))
            self.stdout.write("Note: Users created in the last 24h are skipped for safety.")
            return

        # 3. Detailed List
        self.stdout.write(self.style.NOTICE(f"\n[!] Found {count} unverified users to purge:"))
        for user in targets:
            self.stdout.write(f"  ID: {user.id} | Name: {user.username} | Email: {user.email} | Joined: {user.created_at}")

        # 4. Confirmation Prompt
        confirm = input("\nPROMPT: Type 'yes' to permanently delete these users: ").lower()

        if confirm == 'yes':
            total_deleted, detail_map = targets.delete()
            self.stdout.write(self.style.SUCCESS(f"\nDONE: Purged {total_deleted} total database objects."))
            
            # Print the breakdown of what exactly was deleted
            for model_path, amt in detail_map.items():
                model_name = model_path.split('.')[-1]
                self.stdout.write(f"  - {model_name}: {amt}")
        else:
            self.stdout.write(self.style.ERROR("\nABORTED: No changes made to the database."))