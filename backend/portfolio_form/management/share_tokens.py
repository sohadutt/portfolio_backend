from django.core.management.base import CommandError

from portfolio_form.models import User, generate_share_token


def normalize_user_ids(user_ids):
    return sorted(set(user_ids or []))


def get_target_users(*, user_ids):
    user_ids = normalize_user_ids(user_ids)
    users = User.objects.order_by("id")

    if not user_ids:
        return users, []

    matched_users = users.filter(id__in=user_ids)
    matched_ids = set(matched_users.values_list("id", flat=True))
    missing_ids = [user_id for user_id in user_ids if user_id not in matched_ids]

    return matched_users, missing_ids


def require_target_users(*, user_ids):
    users, missing_ids = get_target_users(user_ids=user_ids)

    if missing_ids:
        missing_text = ", ".join(str(user_id) for user_id in missing_ids)
        raise CommandError(f"User id(s) not found: {missing_text}")

    if not users.exists():
        raise CommandError("No users found.")

    return users


def set_share_token_enabled(*, user_ids, enabled):
    users = require_target_users(user_ids=user_ids)
    status = True if enabled else False

    for user in users:
        user.enable_share_token = enabled
        user.save(update_fields=["enable_share_token"])

    return users, status


def regenerate_tokens(*, user_ids):
    users = require_target_users(user_ids=user_ids)

    for user in users:
        user.share_token = generate_share_token()
        user.save(update_fields=["share_token"])

    return users
