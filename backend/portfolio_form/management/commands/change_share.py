from django.core.management.base import BaseCommand

from portfolio_form.management.share_tokens import (
    regenerate_tokens,
    set_share_token_enabled,
)

USER_IDS = []

class Command(BaseCommand):
    help = "Change share-token state for users in USER_IDS. If USER_IDS is empty, apply to all users."

    def add_arguments(self, parser):
        parser.add_argument("action",choices=["enable", "disable", "regenerate"], help="Action to perform on share tokens: enable, disable, or regenerate.")

    def handle(self, *args, **options):
        action = options["action"]

        if action == "enable":
            users, status = set_share_token_enabled(user_ids=USER_IDS, enabled=True)
            for user in users:
                self.stdout.write(
                    self.style.SUCCESS(f"Share token {status} for user {user.email}.")
                )
            return

        if action == "disable":
            users, status = set_share_token_enabled(user_ids=USER_IDS, enabled=False)
            for user in users:
                self.stdout.write(
                    self.style.SUCCESS(f"Share token {status} for user {user.email}.")
                )
            return

        users = regenerate_tokens(user_ids=USER_IDS)
        for user in users:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Share token regenerated for user {user.email}: {user.share_token}"
                )
            )
