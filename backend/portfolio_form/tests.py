import json

from django.contrib.auth import get_user_model
from django.test import TestCase

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


class PublicPortfolioTests(TestCase):
    def setUp(self):
        self.default_user = User.objects.create_user(
            id=1,
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
