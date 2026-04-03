import secrets

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models, transaction
from django.db.models import Max


def generate_share_token():
    return secrets.token_urlsafe(24)


def generate_dashboard_token():
    return secrets.token_urlsafe(32)


class User(AbstractUser):
    objects = UserManager()

    email = models.EmailField(unique=True)
    share_token = models.CharField(max_length=64,unique=True,default=generate_share_token,editable=False,)
    dashboard_token = models.CharField(max_length=80, unique=True, default=generate_dashboard_token, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class ContactFormSubmission(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="submissions",
    )
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField()
    for_work = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    priority = models.IntegerField(default=0)
    is_dismissed = models.BooleanField(default=False)
    display_index = models.PositiveIntegerField()

    class Meta:
        ordering = ["display_index", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "display_index"],
                name="unique_submission_index_per_owner",
            )
        ]

    def save(self, *args, **kwargs):
        if self._state.adding and not self.display_index:
            max_index = (
                ContactFormSubmission.objects.filter(owner=self.owner)
                .aggregate(max_index=Max("display_index"))
                .get("max_index")
            )
            self.display_index = (max_index or 0) + 1
        super().save(*args, **kwargs)

    @transaction.atomic
    def move_to_index(self, new_index):
        owner_submissions = list(
            ContactFormSubmission.objects.select_for_update()
            .filter(owner=self.owner)
            .order_by("display_index", "id")
        )
        total = len(owner_submissions)
        new_index = max(1, min(int(new_index), total))

        if new_index == self.display_index:
            return

        moving_submission = next(
            submission for submission in owner_submissions if submission.pk == self.pk
        )
        reordered = [
            submission for submission in owner_submissions if submission.pk != self.pk
        ]
        reordered.insert(new_index - 1, moving_submission)

        offset = total + 1000
        for index, submission in enumerate(reordered, start=1):
            submission.display_index = index + offset
            submission.save(update_fields=["display_index"])

        for index, submission in enumerate(reordered, start=1):
            submission.display_index = index
            submission.save(update_fields=["display_index"])

        self.display_index = new_index

    def __str__(self):
        return (
            f"{self.name} - {self.email} - {self.owner.username} - "
            f"{self.submitted_at.strftime('%Y-%m-%d %H:%M:%S')}"
        )
