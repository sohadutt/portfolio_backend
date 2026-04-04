import json
from unittest.mock import patch

from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.utils import override_settings
from django.core import mail

from .models import (
    ContactFormSubmission,
    Experience,
    FeaturedModule,
    HeroMetric,
    Link,
    PortfolioSettings,
    Project,
    ShowcaseCategory,
    SkillGroup,
)


User = get_user_model()


class SubmitFormTests(TestCase):
    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(
            username="alice",
            email="alice@example.com",
            password="testpass123",
            enable_share_token=True,
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

    def build_portfolio_payload(self):
        return {
            "personalInfo": {
                "name": "Alice Doe",
                "shortName": "AD",
                "title": "Full Stack Developer",
                "subtitle": "Building reliable products",
                "location": "Kolkata, India",
                "email": self.user.email,
                "github": "https://github.com/alice",
                "linkedin": "https://linkedin.com/in/alice",
            },
            "navigationLinks": [
                {"label": "About", "href": "#about"},
                {"label": "Projects", "href": "#projects"},
            ],
            "heroContent": {
                "eyebrow": "Available for work",
                "title": "I build products end to end.",
                "description": "Focused on thoughtful UX and maintainable systems.",
            },
            "heroMetrics": [
                {"value": "3+", "label": "Years Experience"},
                {"value": "12+", "label": "Projects"},
            ],
            "aboutContent": {
                "title": "About Me",
                "description": "I enjoy building dependable software.",
            },
            "skillGroups": [
                {
                    "title": "Backend",
                    "description": "APIs and systems",
                    "items": ["Django", "PostgreSQL"],
                }
            ],
            "projects": [
                {
                    "title": "Portfolio Backend",
                    "eyebrow": "Featured",
                    "description": "A portfolio backend with nested content.",
                    "stack": ["Django", "DRF"],
                    "stat": "Live",
                }
            ],
            "experience": [
                {
                    "period": "2024 - Present",
                    "title": "Developer",
                    "company": "Example Co",
                    "relation": "Full-time",
                    "summary": "Builds backend and frontend systems.",
                    "highlights": ["Shipped APIs"],
                    "relatedComponents": ["Portfolio", "Dashboard"],
                },
                {
                    "period": "2027 - Present",
                    "title": "onlyfans",
                    "company": "Example Co",
                    "relation": "Full-time",
                    "summary": "makes onlyfans",
                    "highlights": ["sandwitches"],
                    "relatedComponents": ["Portfolio", "Dashboard"],
                }
            ],
            "showcaseCategories": [
                {
                    "title": "Web Apps",
                    "icon": "Monitor",
                    "relation": "Featured",
                    "preview": "Modern product engineering work.",
                    "items": ["Dashboards", "Portfolio Sites"],
                }
            ],
            "featuredModules": [
                {
                    "title": "Case Studies",
                    "icon": "Briefcase",
                    "relation": "Selected Work",
                    "body": "High-impact builds and experiments.",
                    "details": "Backend systems, UX improvements, and launches.",
                }
            ],
            "contactMethods": [
                {
                    "label": "Email",
                    "value": self.user.email,
                    "href": f"mailto:{self.user.email}",
                    "icon": "Mail",
                }
            ],
            "footerLinks": [
                {"label": "GitHub", "href": "https://github.com/alice"}
            ],
            "statusPills": [
                {"label": "Open to Work", "icon": "Sparkles"}
            ],
        }

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
        self.assertFalse(response.json()["data"]["enable_share_token"])
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
        self.assertTrue(response.json()["data"]["enable_share_token"])
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

    def test_portfolio_submit_url_is_not_captured_as_share_token(self):
        bearer_token = self.login_and_get_bearer_token()

        response = self.client.post(
            "/api/portfolio/submit/",
            data=json.dumps(self.build_portfolio_payload()),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {bearer_token}",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(PortfolioSettings.objects.filter(owner=self.user).exists())

    def test_portfolio_update_url_is_not_captured_as_share_token(self):
        bearer_token = self.login_and_get_bearer_token()
        self.client.post(
            "/api/portfolio/submit/",
            data=json.dumps(self.build_portfolio_payload()),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {bearer_token}",
        )

        payload = self.build_portfolio_payload()
        payload["personalInfo"]["title"] = "Updated Portfolio Title"
        response = self.client.post(
            "/api/portfolio/update/",
            data=json.dumps(payload),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {bearer_token}",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            PortfolioSettings.objects.get(owner=self.user).title,
            "Updated Portfolio Title",
        )

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

    def test_submission_uses_shared_portfolio_owner(self):
        portfolio_owner = User.objects.create_user(
            username="bob",
            email="bob@example.com",
            password="bobpass123",
            enable_share_token=True,
        )
        portfolio = PortfolioSettings.objects.create(
            owner=portfolio_owner,
            short_name="BOB",
            title="Bob Portfolio",
            subtitle="Backend Developer",
            location="Kolkata",
            email="bob@example.com",
            github="https://github.com/bob",
            linkedin="https://linkedin.com/in/bob",
            hero_eyebrow="Available for work",
            hero_title="Building APIs",
            hero_description="I build backend systems.",
            about_title="About Bob",
            about_description="Experienced backend engineer.",
        )

        response = self.client.post(
            f"/api/shares/{portfolio_owner.share_token}/submissions/",
            data=json.dumps(
                {
                    "name": "Visitor",
                    "email": "visitor@example.com",
                    "message": "Hello shared portfolio",
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        submission = ContactFormSubmission.objects.get(email="visitor@example.com")
        self.assertEqual(submission.owner, portfolio_owner)
        self.assertEqual(submission.portfolio, portfolio)
        self.assertEqual(response.json()["data"]["owner_user_id"], portfolio_owner.id)
        self.assertEqual(response.json()["data"]["portfolio_id"], portfolio.id)

    def test_submission_fails_when_share_token_is_disabled(self):
        disabled_user = User.objects.create_user(
            username="charlie",
            email="charlie@example.com",
            password="charliepass123",
            enable_share_token=False,
        )
        PortfolioSettings.objects.create(
            owner=disabled_user,
            short_name="CHR",
            title="Charlie Portfolio",
            subtitle="Developer",
            location="Kolkata",
            email="charlie@example.com",
            github="https://github.com/charlie",
            linkedin="https://linkedin.com/in/charlie",
            hero_eyebrow="Open",
            hero_title="Building things",
            hero_description="Portfolio",
            about_title="About Charlie",
            about_description="Software engineer.",
        )

        response = self.client.post(
            f"/api/shares/{disabled_user.share_token}/submissions/",
            data=json.dumps(
                {
                    "name": "Visitor",
                    "email": "visitor-disabled@example.com",
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

    def test_reorder_submissions_updates_full_order(self):
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

        response = self.client.post(
            "/api/submissions/reorder/",
            data=json.dumps({"order": [created[1].id, created[2].id, created[0].id]}),
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
                ("visitor1@example.com", 1),
                ("visitor2@example.com", 2),
                ("visitor0@example.com", 3),
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

    def test_bearer_token_can_dismiss_form_enquiry(self):
        submission = ContactFormSubmission.objects.create(
            owner=self.user,
            name="Visitor",
            email="visitor@example.com",
            message="Hello",
            display_index=1,
        )
        bearer_token = self.login_and_get_bearer_token()

        response = self.client.patch(
            f"/api/submissions/{submission.id}/",
            data=json.dumps({"is_dismissed": True}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {bearer_token}",
        )

        self.assertEqual(response.status_code, 200)
        submission.refresh_from_db()
        self.assertTrue(submission.is_dismissed)

    @override_settings(
        CONTACT_FORM_RATE_LIMIT_MAX_REQUESTS=2,
        CONTACT_FORM_RATE_LIMIT_WINDOW_SECONDS=60,
        CONTACT_FORM_BLOCK_SECONDS=24 * 60 * 60,
    )
    def test_contact_form_blocks_after_too_many_requests_from_same_ip(self):
        payload = {
            "name": "Visitor",
            "email": "visitor@example.com",
            "message": "Hello Alice",
        }

        first_response = self.client.post(
            "/api/forms/submit/",
            data=json.dumps(payload),
            content_type="application/json",
            REMOTE_ADDR="203.0.113.10",
        )
        second_response = self.client.post(
            "/api/forms/submit/",
            data=json.dumps(
                {
                    **payload,
                    "email": "visitor2@example.com",
                }
            ),
            content_type="application/json",
            REMOTE_ADDR="203.0.113.10",
        )
        third_response = self.client.post(
            "/api/forms/submit/",
            data=json.dumps(
                {
                    **payload,
                    "email": "visitor3@example.com",
                }
            ),
            content_type="application/json",
            REMOTE_ADDR="203.0.113.10",
        )

        self.assertEqual(first_response.status_code, 201)
        self.assertEqual(second_response.status_code, 201)
        self.assertEqual(third_response.status_code, 429)
        self.assertEqual(ContactFormSubmission.objects.count(), 2)
        self.assertEqual(third_response.json()["blocked_for_seconds"], 24 * 60 * 60)

    @override_settings(
        CONTACT_FORM_RATE_LIMIT_MAX_REQUESTS=2,
        CONTACT_FORM_RATE_LIMIT_WINDOW_SECONDS=60,
        CONTACT_FORM_BLOCK_SECONDS=24 * 60 * 60,
    )
    def test_contact_form_block_persists_beyond_request_window(self):
        payload = {
            "name": "Visitor",
            "email": "visitor@example.com",
            "message": "Hello Alice",
        }

        with patch("portfolio_form.views.time.time", return_value=1_000):
            self.client.post(
                "/api/forms/submit/",
                data=json.dumps(payload),
                content_type="application/json",
                REMOTE_ADDR="203.0.113.11",
            )
            self.client.post(
                "/api/forms/submit/",
                data=json.dumps(
                    {
                        **payload,
                        "email": "visitor2@example.com",
                    }
                ),
                content_type="application/json",
                REMOTE_ADDR="203.0.113.11",
            )
            blocking_response = self.client.post(
                "/api/forms/submit/",
                data=json.dumps(
                    {
                        **payload,
                        "email": "visitor3@example.com",
                    }
                ),
                content_type="application/json",
                REMOTE_ADDR="203.0.113.11",
            )

        with patch("portfolio_form.views.time.time", return_value=1_000 + 120):
            blocked_response = self.client.post(
                "/api/forms/submit/",
                data=json.dumps(
                    {
                        **payload,
                        "email": "visitor4@example.com",
                    }
                ),
                content_type="application/json",
                REMOTE_ADDR="203.0.113.11",
            )

        self.assertEqual(blocking_response.status_code, 429)
        self.assertEqual(blocked_response.status_code, 429)
        self.assertEqual(ContactFormSubmission.objects.count(), 2)

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
        self.assertTrue(response.json()["enable_share_token"])
        self.assertEqual(response.json()["share_token"], self.user.share_token)

    def test_authenticated_user_can_submit_portfolio(self):
        bearer_token = self.login_and_get_bearer_token()

        response = self.client.post(
            "/api/submit_portfolio/",
            data=json.dumps(self.build_portfolio_payload()),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {bearer_token}",
        )

        self.assertEqual(response.status_code, 201)
        portfolio = PortfolioSettings.objects.get(owner=self.user)
        self.assertEqual(portfolio.name, "Alice Doe")
        self.assertEqual(portfolio.short_name, "AD")
        self.assertEqual(HeroMetric.objects.filter(owner=self.user).count(), 2)
        self.assertEqual(SkillGroup.objects.filter(owner=self.user).count(), 1)
        self.assertEqual(Link.objects.filter(owner=self.user, type=Link.LinkType.NAV).count(), 2)
        self.assertEqual(response.json()["data"]["personalInfo"]["name"], "Alice Doe")
        self.assertEqual(
            response.json()["data"]["showcaseCategories"][0]["icon"],
            "Monitor",
        )

    def test_portfolio_submit_requires_authentication(self):
        response = self.client.post(
            "/api/submit_portfolio/",
            data=json.dumps(self.build_portfolio_payload()),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 401)

    def test_portfolio_submit_accepts_icon_name_aliases(self):
        bearer_token = self.login_and_get_bearer_token()
        payload = self.build_portfolio_payload()
        payload["showcaseCategories"][0].pop("icon")
        payload["showcaseCategories"][0]["iconName"] = "Sparkles"
        payload["featuredModules"][0].pop("icon")
        payload["featuredModules"][0]["iconName"] = "Database"
        payload["contactMethods"][0].pop("icon")
        payload["contactMethods"][0]["iconName"] = "Mail"
        payload["statusPills"][0].pop("icon")
        payload["statusPills"][0]["iconName"] = "ArrowUpRight"

        response = self.client.post(
            "/api/submit_portfolio/",
            data=json.dumps(payload),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {bearer_token}",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["data"]["showcaseCategories"][0]["icon"], "Sparkles")
        self.assertEqual(response.json()["data"]["featuredModules"][0]["icon"], "Database")
        self.assertEqual(response.json()["data"]["contactMethods"][0]["icon"], "Mail")
        self.assertEqual(response.json()["data"]["statusPills"][0]["icon"], "ArrowUpRight")

    def test_free_tier_user_cannot_submit_more_than_three_experiences(self):
        bearer_token = self.login_and_get_bearer_token()
        payload = self.build_portfolio_payload()
        payload["experience"] = [
            {
                "period": f"202{index} - Present",
                "title": f"Developer {index}",
                "company": f"Example Co {index}",
                "relation": "Full-time",
                "summary": f"Summary {index}",
                "highlights": [f"Highlight {index}"],
                "relatedComponents": [f"Component {index}"],
            }
            for index in range(4)
        ]

        response = self.client.post(
            "/api/submit_portfolio/",
            data=json.dumps(payload),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {bearer_token}",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("experience", response.json())
        self.assertEqual(Experience.objects.filter(owner=self.user).count(), 0)

    def test_superuser_can_submit_more_than_three_experiences(self):
        admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="adminpass123",
        )
        response = self.client.post(
            "/api/auth/login/",
            data=json.dumps(
                {
                    "email": admin_user.email,
                    "password": "adminpass123",
                }
            ),
            content_type="application/json",
        )
        bearer_token = response.json()["data"]["bearer_token"]

        payload = self.build_portfolio_payload()
        payload["personalInfo"]["email"] = admin_user.email
        payload["contactMethods"][0]["value"] = admin_user.email
        payload["contactMethods"][0]["href"] = f"mailto:{admin_user.email}"
        payload["experience"] = [
            {
                "period": f"202{index} - Present",
                "title": f"Lead {index}",
                "company": f"Admin Co {index}",
                "relation": "Full-time",
                "summary": f"Summary {index}",
                "highlights": [f"Highlight {index}"],
                "relatedComponents": [f"Component {index}"],
            }
            for index in range(4)
        ]

        response = self.client.post(
            "/api/submit_portfolio/",
            data=json.dumps(payload),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {bearer_token}",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Experience.objects.filter(owner=admin_user).count(), 4)

    def test_paid_user_can_submit_more_than_three_experiences(self):
        paid_user = User.objects.create_user(
            username="paid",
            email="paid@example.com",
            password="paidpass123",
            tier=User.Tier.PRO,
        )
        response = self.client.post(
            "/api/auth/login/",
            data=json.dumps(
                {
                    "email": paid_user.email,
                    "password": "paidpass123",
                }
            ),
            content_type="application/json",
        )
        bearer_token = response.json()["data"]["bearer_token"]

        payload = self.build_portfolio_payload()
        payload["personalInfo"]["email"] = paid_user.email
        payload["contactMethods"][0]["value"] = paid_user.email
        payload["contactMethods"][0]["href"] = f"mailto:{paid_user.email}"
        payload["experience"] = [
            {
                "period": f"202{index} - Present",
                "title": f"Engineer {index}",
                "company": f"Paid Co {index}",
                "relation": "Full-time",
                "summary": f"Summary {index}",
                "highlights": [f"Highlight {index}"],
                "relatedComponents": [f"Component {index}"],
            }
            for index in range(4)
        ]

        response = self.client.post(
            "/api/submit_portfolio/",
            data=json.dumps(payload),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {bearer_token}",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Experience.objects.filter(owner=paid_user).count(), 4)


class PublicPortfolioTests(TestCase):
    def setUp(self):
        self.default_user = User.objects.create_user(
            # Remove: id=1,
            username="soham",
            email="soham@example.com",
            password="testpass123",
            enable_share_token=True,
        )
        self.shared_user = User.objects.create_user(
            username="alice",
            email="alice@example.com",
            password="testpass123",
            enable_share_token=True,
        )

        self.create_portfolio_fixture(self.default_user, "Soham Dutta", "SD")
        self.create_portfolio_fixture(self.shared_user, "Alice Doe", "AD")

    def create_portfolio_fixture(self, user, name, short_name):
        PortfolioSettings.objects.create(
            owner=user,
            name=name,
            short_name=short_name,
            title="Full-stack Developer",
            subtitle="JavaScript, Python, Django, React",
            location="India",
            email=user.email,
            github=f"https://github.com/{user.username}",
            linkedin=f"https://linkedin.com/in/{user.username}",
            hero_eyebrow=name,
            hero_title=f"{name} builds reliable systems.",
            hero_description=f"{name} works across backend and frontend.",
            about_title="About",
            about_description=f"This is {name}'s portfolio.",
        )
        HeroMetric.objects.create(owner=user, order=1, value="2024", label="Started")
        SkillGroup.objects.create(
            owner=user,
            order=1,
            title="Backend & APIs",
            description="Backend work",
            items=["Python", "Django"],
        )
        Project.objects.create(
            owner=user,
            order=1,
            title="Portfolio API",
            eyebrow="Backend",
            description="Public portfolio endpoint",
            stack=["Django", "REST API"],
            stat="Live",
        )
        Experience.objects.create(
            owner=user,
            order=1,
            period="2024 - Present",
            title="Developer",
            company="Example Co",
            relation="automation",
            summary="Builds systems",
            highlights=["Shipped APIs"],
            related_components=["Table", "Toast"],
        )
        ShowcaseCategory.objects.create(
            owner=user,
            order=1,
            title="Display & Feedback",
            icon_name="Sparkles",
            relation="workflow",
            preview="Preview text",
            items=["Alert", "Badge"],
        )
        FeaturedModule.objects.create(
            owner=user,
            order=1,
            title="Config automation",
            icon_name="Database",
            relation="automation",
            body="Backend automation work",
            details="More detail",
        )
        Link.objects.create(
            owner=user,
            order=1,
            type=Link.LinkType.NAV,
            label="About",
            href="#about",
        )
        Link.objects.create(
            owner=user,
            order=1,
            type=Link.LinkType.FOOTER,
            label="GitHub",
            href=f"https://github.com/{user.username}",
        )
        Link.objects.create(
            owner=user,
            order=1,
            type=Link.LinkType.CONTACT,
            label="Email",
            value=user.email,
            href=f"mailto:{user.email}",
            icon_name="Mail",
        )
        Link.objects.create(
            owner=user,
            order=1,
            type=Link.LinkType.STATUS,
            label="Backend and config automation",
            icon_name="ArrowUpRight",
        )

    def test_portfolio_without_token_returns_default_user_portfolio(self):
        response = self.client.get("/api/portfolio/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["personalInfo"]["name"], "Soham Dutta")
        self.assertEqual(response.json()["personalInfo"]["shortName"], "SD")

    def test_portfolio_with_share_token_returns_shared_user_portfolio(self):
        response = self.client.get(f"/api/portfolio/{self.shared_user.share_token}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["personalInfo"]["name"], "Alice Doe")
        self.assertEqual(response.json()["personalInfo"]["shortName"], "AD")

    def test_portfolio_response_matches_frontend_shape(self):
        response = self.client.get("/api/portfolio/")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("personalInfo", data)
        self.assertIn("navigationLinks", data)
        self.assertIn("heroContent", data)
        self.assertIn("heroMetrics", data)
        self.assertIn("aboutContent", data)
        self.assertIn("skillGroups", data)
        self.assertIn("projects", data)
        self.assertIn("experience", data)
        self.assertIn("showcaseCategories", data)
        self.assertIn("featuredModules", data)
        self.assertIn("contactMethods", data)
        self.assertIn("footerLinks", data)
        self.assertIn("statusPills", data)
        self.assertEqual(data["navigationLinks"][0], {"label": "About", "href": "#about"})
        self.assertEqual(data["contactMethods"][0]["icon"], "Mail")
        self.assertEqual(data["showcaseCategories"][0]["icon"], "Sparkles")
        self.assertEqual(data["featuredModules"][0]["icon"], "Database")
        self.assertEqual(data["experience"][0]["relatedComponents"], ["Table", "Toast"])

    def test_portfolio_with_invalid_share_token_returns_404(self):
        response = self.client.get("/api/portfolio/invalid-token/")

        self.assertEqual(response.status_code, 404)

class OTPAuthenticationTests(TestCase):
    def setUp(self):
        cache.clear()
        mail.outbox = [] # Clear the test email outbox

    def test_request_otp_creates_partial_profile(self):
        response = self.client.post(
            "/api/profile/auth_otp/", # Adjust URL to match your exact routing
            data=json.dumps({"email": "newuser@example.com"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "If the email is valid, an OTP has been sent.")
        
        # Verify a partial profile was created
        user = User.objects.get(email="newuser@example.com")
        self.assertFalse(user.is_verified)
        self.assertFalse(user.has_usable_password())

        # Verify an email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Your OTP Code", mail.outbox[0].subject)
        self.assertEqual(mail.outbox[0].to, ["newuser@example.com"])

        # Verify OTP is in cache
        cached_otp = cache.get("otp:newuser@example.com")
        self.assertIsNotNone(cached_otp)
        self.assertEqual(len(cached_otp), 6)

    def test_request_otp_for_existing_verified_user(self):
        User.objects.create_user(
            username="existing",
            email="existing@example.com",
            password="testpass123",
            is_verified=True
        )

        response = self.client.post(
            "/api/profile/auth_otp/", 
            data=json.dumps({"email": "existing@example.com"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        
        # Verify user is STILL verified and wasn't overwritten
        user = User.objects.get(email="existing@example.com")
        self.assertTrue(user.is_verified)
        self.assertTrue(user.has_usable_password())
        
        # Verify email was still sent (for login)
        self.assertEqual(len(mail.outbox), 1)

    def test_verify_otp_completes_partial_profile_and_returns_tokens(self):
        # 1. Setup a partial profile and an OTP in cache
        user = User.objects.create(
            username="partial_user",
            email="partial@example.com",
            is_verified=False
        )
        user.set_unusable_password()
        user.save()
        
        valid_otp = "123456"
        cache.set("otp:partial@example.com", valid_otp, timeout=300)

        # 2. Attempt verification
        response = self.client.post(
            "/api/profile/verify_otp/", 
            data=json.dumps({
                "email": "partial@example.com",
                "otp": valid_otp
            }),
            content_type="application/json",
        )

        # 3. Assertions
        self.assertEqual(response.status_code, 200)
        self.assertIn("tokens", response.json())
        self.assertIn("access", response.json()["tokens"])
        
        # Verify the user is now fully verified
        user.refresh_from_db()
        self.assertTrue(user.is_verified)
        
        # Verify the OTP was deleted from cache (single-use)
        self.assertIsNone(cache.get("otp:partial@example.com"))

    def test_verify_otp_fails_with_invalid_code(self):
        cache.set("otp:test@example.com", "123456", timeout=300)

        response = self.client.post(
            "/api/profile/verify_otp/", 
            data=json.dumps({
                "email": "test@example.com",
                "otp": "654321" # Wrong OTP
            }),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Invalid or expired OTP.")


class ProfileRegistrationTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_password_registration_takes_over_partial_profile(self):
        # Setup an unverified user (simulating someone who requested an OTP but abandoned it)
        User.objects.create(
            username="abandoned",
            email="abandoned@example.com",
            is_verified=False
        )

        # They now try to register using the standard password form
        response = self.client.post(
            "/api/profile/register/", 
            data=json.dumps({
                "email": "abandoned@example.com",
                "password": "StrongPassword123!"
            }),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        
        user = User.objects.get(email="abandoned@example.com")
        self.assertTrue(user.is_verified)
        self.assertTrue(user.check_password("StrongPassword123!"))

    def test_password_registration_blocked_for_verified_users(self):
        # Setup a fully verified user
        User.objects.create_user(
            username="verified",
            email="verified@example.com",
            password="OldPassword123!",
            is_verified=True
        )

        # They attempt to register again
        response = self.client.post(
            "/api/profile/register/", 
            data=json.dumps({
                "email": "verified@example.com",
                "password": "NewPassword123!"
            }),
            content_type="application/json",
        )

        # Should be blocked by the serializer's validate_email
        self.assertEqual(response.status_code, 400)
        self.assertIn("A user with this email already exists.", str(response.content))