from django.db import models
from django.utils.translation import gettext_lazy as _
from portfolio_form.models import PortfolioSettings 

class Job(models.Model):
    """
    Stores the raw job details scraped from the company sites.
    """
    platform_name = models.CharField(max_length=50, help_text="e.g., Deloitte, Accenture")
    platform_job_id = models.CharField(max_length=100, db_index=True)
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(max_length=1000)
    date_posted = models.CharField(max_length=50, blank=True, null=True)
    tags = models.JSONField(default=list, help_text="Stable AI-generated job tags")
    ai_metadata = models.JSONField(default=dict, blank=True, help_text="Stable AI-generated job metadata")
    ai_processed_at = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('platform_name', 'platform_job_id')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.company} - {self.title}"


class PortfolioJobMatch(models.Model):
    """
    The pivot table linking a user's portfolio to a job, storing the AI's specific analysis.
    """
    portfolio = models.ForeignKey(
        PortfolioSettings, 
        on_delete=models.CASCADE, 
        related_name='job_matches'
    )
    job = models.ForeignKey(
        Job, 
        on_delete=models.CASCADE, 
        related_name='portfolio_matches'
    )
    
    match_score = models.FloatField(help_text="Match percentage from 0 to 100")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('portfolio', 'job')
        ordering = ['-match_score']

    def __str__(self):
        return f"{self.portfolio.owner.username} -> {self.job.title} ({self.match_score}%)"
