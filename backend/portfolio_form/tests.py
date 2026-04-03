from django.contrib.auth import get_user_model
from django.test import TestCase
import json

from .models import ContactFormSubmission


User = get_user_model()


class SubmitFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="alice",
            email="alice@example.com",
            password="testpass123",
        )

    def login_and_get_bearer_token(self):
        response = self.client.post(
            "/api/auth/login/",
            data=json.dumps(
                {
                    "email": self.user.email,
                    "password": "testpass123",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["data"]["temporary_token"])
        self.assertTrue(response.json()["data"]["bearer_token"])
        return response.json()["data"]["bearer_token"]

    def test_create_profile_creates_user(self):
        response = self.client.post(
            "/api/profiles/",
            data=json.dumps(
                {
                    "email": "bob@example.com",
                    "password": "bobpass123",
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        created_user = User.objects.get(email="bob@example.com")
        self.assertEqual(response.json()["data"]["user_id"], created_user.id)
        self.assertEqual(response.json()["data"]["email"], "bob@example.com")
        self.assertTrue(response.json()["data"]["share_token"])

    def test_create_profile_rejects_duplicate_email(self):
        response = self.client.post(
            "/api/profiles/",
            data=json.dumps(
                {
                    "email": "alice@example.com",
                    "password": "anotherpass123",
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)

    def test_login_returns_temporary_and_bearer_tokens(self):
        response = self.client.post(
            "/api/auth/login/",
            data=json.dumps(
                {
                    "email": self.user.email,
                    "password": "testpass123",
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["email"], self.user.email)
        self.assertEqual(response.json()["data"]["token_type"], "Bearer")
        self.assertTrue(response.json()["data"]["temporary_token"])
        self.assertTrue(response.json()["data"]["bearer_token"])

    def test_login_rejects_invalid_credentials(self):
        response = self.client.post(
            "/api/auth/login/",
            data=json.dumps(
                {
                    "email": self.user.email,
                    "password": "wrong-password",
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)

    def test_login_requires_json_input(self):
        response = self.client.post(
            "/api/auth/login/",
            data={
                "email": self.user.email,
                "password": "testpass123",
            },
        )

        self.assertEqual(response.status_code, 415)

    def test_submission_is_saved_for_owner_from_token(self):
        response = self.client.post(
            f"/api/shares/{self.user.share_token}/submissions/",
            data=json.dumps(
                {
                    "name": "Visitor",
                    "email": "visitor@example.com",
                    "phone": "1234567890",
                    "message": "Hello Alice",
                    "for_work": True,
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        submission = ContactFormSubmission.objects.get()
        self.assertEqual(submission.owner, self.user)
        self.assertEqual(submission.message, "Hello Alice")
        self.assertTrue(submission.for_work)
        self.assertEqual(submission.display_index, 1)
        self.assertEqual(response.json()["data"]["owner_user_id"], self.user.id)

    def test_invalid_token_returns_404(self):
        response = self.client.post(
            "/api/shares/invalid-token/submissions/",
            data=json.dumps(
                {
                    "name": "Visitor",
                    "email": "visitor@example.com",
                    "message": "Hello",
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)

    def test_display_index_increments_per_contact(self):
        for number in range(3):
            self.client.post(
                f"/api/shares/{self.user.share_token}/submissions/",
                data=json.dumps(
                    {
                        "name": f"Visitor {number}",
                        "email": f"visitor{number}@example.com",
                        "message": f"Hello {number}",
                    }
                ),
                content_type="application/json",
            )

        indices = list(
            ContactFormSubmission.objects.values_list("display_index", flat=True)
        )
        self.assertEqual(indices, [1, 2, 3])

    def test_updating_display_index_reorders_other_contacts(self):
        created = []
        for number in range(3):
            self.client.post(
                f"/api/shares/{self.user.share_token}/submissions/",
                data=json.dumps(
                    {
                        "name": f"Visitor {number}",
                        "email": f"visitor{number}@example.com",
                        "message": f"Hello {number}",
                    }
                ),
                content_type="application/json",
            )
            created.append(
                ContactFormSubmission.objects.get(email=f"visitor{number}@example.com")
            )

        bearer_token = self.login_and_get_bearer_token()

        response = self.client.patch(
            f"/api/submissions/{created[2].id}/",
            data=json.dumps({"display_index": 1}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {bearer_token}",
        )

        self.assertEqual(response.status_code, 200)
        ordered = list(
            ContactFormSubmission.objects.order_by("display_index").values_list(
                "email",
                "display_index",
            )
        )
        self.assertEqual(
            ordered,
            [
                ("visitor2@example.com", 1),
                ("visitor0@example.com", 2),
                ("visitor1@example.com", 3),
            ],
        )

    def test_share_token_cannot_update_form_without_login(self):
        submission = ContactFormSubmission.objects.create(
            owner=self.user,
            name="Visitor",
            email="visitor@example.com",
            message="Hello",
            display_index=1,
        )

        response = self.client.post(
            f"/api/submissions/{submission.id}/",
            data=json.dumps({"is_dismissed": True}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 401)
        submission.refresh_from_db()
        self.assertFalse(submission.is_dismissed)

    def test_share_token_cannot_view_dashboard_without_login(self):
        ContactFormSubmission.objects.create(
            owner=self.user,
            name="Visitor",
            email="visitor@example.com",
            message="Hello",
            display_index=1,
        )

        response = self.client.get(
            "/api/submissions/"
        )

        self.assertEqual(response.status_code, 401)

    def test_bearer_token_can_view_dashboard(self):
        ContactFormSubmission.objects.create(
            owner=self.user,
            name="Visitor",
            email="visitor@example.com",
            message="Hello",
            display_index=1,
        )

        bearer_token = self.login_and_get_bearer_token()

        response = self.client.get(
            "/api/submissions/",
            HTTP_AUTHORIZATION=f"Bearer {bearer_token}",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["owner_user_id"], self.user.id)
        self.assertEqual(len(response.json()["submissions"]), 1)

    def test_bearer_token_can_get_profile_tokens(self):
        bearer_token = self.login_and_get_bearer_token()

        response = self.client.get(
            "/api/profile/tokens/",
            HTTP_AUTHORIZATION=f"Bearer {bearer_token}",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["share_token"], self.user.share_token)
