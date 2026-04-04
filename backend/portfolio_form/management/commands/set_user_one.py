from django.core.management.base import BaseCommand
from django.db import connection, transaction
from portfolio_form.models import User

class Command(BaseCommand):
    help = 'Changes a specific user to ID 1 and updates all relations'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Target username')

    @transaction.atomic
    def handle(self, *args, **options):
        username = options['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"User '{username}' not found."))
            return

        old_id = user.id
        if old_id == 1:
            self.stdout.write(self.style.SUCCESS("User is already ID 1."))
            return

        # Check if ID 1 is already occupied
        if User.objects.filter(id=1).exists():
            self.stdout.write(self.style.ERROR("ID 1 is already taken by another user. Delete them or move them first."))
            return

        with connection.cursor() as cursor:
            # We use raw SQL because Django doesn't like it when you manually edit PKs
            self.stdout.write(f"Moving {username} from ID {old_id} to 1...")
            
            # Update the User
            cursor.execute("UPDATE portfolio_form_user SET id = 1 WHERE id = %s", [old_id])
            
            # List of tables that link to User (Foreign Keys)
            related_tables = [
                "portfolio_form_portfoliosettings",
                "portfolio_form_contactformsubmission",
                "portfolio_form_experience",
                "portfolio_form_project",
                "portfolio_form_skillgroup",
                "portfolio_form_herometric",
                "portfolio_form_link",
            ]

            for table in related_tables:
                cursor.execute(f"UPDATE {table} SET owner_id = 1 WHERE owner_id = %s", [old_id])

            # Reset the Postgres sequence so it doesn't get stuck
            cursor.execute("SELECT setval('portfolio_form_user_id_seq', (SELECT MAX(id) FROM portfolio_form_user))")

        self.stdout.write(self.style.SUCCESS(f"Successfully moved '{username}' to ID 1 and updated all relations."))