import time
from django.core.management.base import BaseCommand
from portfolio_form.models import PortfolioSettings
from portfolio_form.tasks import run_job_pipeline

class Command(BaseCommand):
    help = 'Manually trigger the job scraping and processing pipeline.'

    def add_arguments(self, parser):
        parser.add_argument('--site', type=str, required=True, help='Name of the site (e.g., deloitte)')
        parser.add_argument('--portfolio', type=int, required=True, help='Portfolio ID to run against')
        parser.add_argument('--no-scrape', action='store_false', dest='scrape', help='Skip scraping phase')
        parser.add_argument('--no-process', action='store_false', dest='process', help='Skip AI processing phase')
        parser.add_argument('--async', action='store_true', help='Run via Celery instead of synchronously')

    def handle(self, *args, **options):
        site = options['site']
        portfolio_id = options['portfolio']
        run_scrape = options['scrape']
        run_process = options['process']
        run_async = options['async']
        start_total = time.time()

        try:
            PortfolioSettings.objects.get(id=portfolio_id)
        except PortfolioSettings.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Portfolio ID {portfolio_id} does not exist."))
            return

        self.stdout.write(self.style.NOTICE(f"--- Pipeline Starting: {site} (Portfolio: {portfolio_id}) ---"))

        if run_async:
            task = run_job_pipeline.delay(site, run_scrape, run_process, portfolio_id)
            self.stdout.write(self.style.SUCCESS(f"Task dispatched to Celery. Task ID: {task.id}"))
        
        try:
            result = run_job_pipeline(site, options['scrape'], options['process'], portfolio_id)
            total_duration = time.time() - start_total
            self.stdout.write(self.style.SUCCESS(f"--- Pipeline Complete in {total_duration:.2f}s ---"))
            self.stdout.write(str(result))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Pipeline crashed: {str(e)}"))