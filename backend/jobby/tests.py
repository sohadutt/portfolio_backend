from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from portfolio_form.models import PortfolioSettings

from .jobby import DatabaseUpdater
from .models import Job, PortfolioJobMatch
from .serializers import PortfolioJobMatchSerializer


User = get_user_model()


def create_portfolio(user, order_index=1):
    return PortfolioSettings.objects.create(
        owner=user,
        order_index=order_index,
        short_name="TU",
        title="Backend Developer",
        subtitle="APIs and automation",
        location="Kolkata",
        email=user.email,
    )


class JobbyMatchOnlyTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester",
            email="tester@example.com",
            password="testpass123",
            job_analysis_limit=1,
        )
        self.portfolio = create_portfolio(self.user)
        self.job = Job.objects.create(
            platform_name="deloitte",
            platform_job_id="358335",
            title="Backend Engineer",
            company="Deloitte",
            location="Bengaluru",
            url="https://example.com/jobs/358335",
            tags=["Backend Development", "Python", "APIs"],
            ai_metadata={"role_family": "Software Engineering"},
        )

    def test_match_score_save_does_not_modify_job_tags(self):
        saved_count = DatabaseUpdater.save_match_scores_to_db(
            ai_matches=[{"job_id": "358335", "match_score": 155}],
            portfolio_id=self.portfolio.id,
            site_name="deloitte",
        )

        self.assertEqual(saved_count, 1)
        match = PortfolioJobMatch.objects.get(portfolio=self.portfolio, job=self.job)
        self.assertEqual(match.match_score, 100.0)

        self.job.refresh_from_db()
        self.assertEqual(self.job.tags, ["Backend Development", "Python", "APIs"])

    def test_match_serializer_exposes_tags_from_job(self):
        match = PortfolioJobMatch.objects.create(
            portfolio=self.portfolio,
            job=self.job,
            match_score=80,
        )

        data = PortfolioJobMatchSerializer(match).data

        self.assertEqual(data["tags"], ["Backend Development", "Python", "APIs"])
        self.assertEqual(data["job"]["tags"], ["Backend Development", "Python", "APIs"])

    def test_start_signal_consumes_credit_and_dispatches_match_only_task(self):
        client = APIClient()
        client.force_authenticate(user=self.user)

        with patch("jobby.views.run_job_pipeline.delay", return_value=SimpleNamespace(id="task-1")) as delay:
            response = client.post("/api/jobs/signals/start/deloitte/?match_only=true")

        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.json()["job_analysis_limit"], 0)
        delay.assert_called_once_with("deloitte", False, True, self.portfolio.id, True)

        self.user.refresh_from_db()
        self.assertEqual(self.user.job_analysis_limit, 0)

    def test_start_signal_rejects_when_no_analysis_credit_left(self):
        self.user.job_analysis_limit = 0
        self.user.save(update_fields=["job_analysis_limit"])

        client = APIClient()
        client.force_authenticate(user=self.user)

        with patch("jobby.views.run_job_pipeline.delay") as delay:
            response = client.post("/api/jobs/signals/start/deloitte/?match_only=true")

        self.assertEqual(response.status_code, 402)
        self.assertEqual(response.json()["error"], "No credit left for analysis.")
        delay.assert_not_called()
