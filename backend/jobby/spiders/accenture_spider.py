import scrapy
from w3lib.html import remove_tags
from tqdm import tqdm
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from res import SITE_CONFIG

class AccentureJobsSpider(scrapy.Spider):
    """
    Spider to extract job postings from the Accenture Careers portal.
    Parses the DOM directly since Accenture does not use application/ld+json.
    """
    name = "accenture_jobs"
    allowed_domains = ["accenture.com"]
    start_urls = [SITE_CONFIG["accenture"]["url"]]

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': SITE_CONFIG["accenture"]["output_file"],
        'FEED_EXPORT_INDENT': 4,
        'LOG_LEVEL': 'INFO',
    }

    def __init__(self, *args, **kwargs):
        super(AccentureJobsSpider, self).__init__(*args, **kwargs)
        self.current_page = 1

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        """
        Instantiates the spider and connects Scrapy signals to the tqdm progress bar.
        """
        spider = super(AccentureJobsSpider, cls).from_crawler(crawler, *args, **kwargs)
        spider.pbar = tqdm(desc="Jobs Scraped", unit="job")
        crawler.signals.connect(spider.item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def item_scraped(self, item, response, spider):
        """Callback: Updates the progress bar every time a job is yielded."""
        self.pbar.update(1)

    def spider_closed(self, spider):
        """Callback: Closes the progress bar cleanly when the spider finishes."""
        self.pbar.close()

    def start_requests(self):
        """
        Initiates the scraping process by sending a request to the start URL.
        """
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        Parses the main search results page, extracting data directly from the HTML cards.
        """
        job_cards = response.css('div.rad-filters-vertical__job-card')

        for card in job_cards:
            # Extract raw data from the card's CSS classes
            job_id = card.css('button.rad-save-job::attr(data-job-id)').get()
            title = card.css('h3.rad-filters-vertical__job-card-title::text').get()
            url = card.css('a.rad-filters-vertical__job-card-content-link-button::attr(href)').get()
            location = card.css('span.rad-filters-vertical__job-card-details-location::text').get()
            date_posted = card.css('span.rad-filters-vertical__job-card-content-job-posted-date-dynamic-text::text').get()
            
            # Accenture stores experience and skills in separate spans
            experience = card.css('span.rad-filters-vertical__job-card-details-type::text').get()
            skill = card.css('span.rad-filters-vertical__job-card-details-skills-dynamic-text::text').get()
            
            # Combine experience and skills into the qualifications field to match our DB schema
            qualifications = f"{experience if experience else ''} | Required Skill: {skill if skill else ''}".strip(' |')
            
            raw_description = card.css('div.rad-filters-vertical__job-card-content-job-description-dynamic-text::text').get()

            # Make sure we actually found a job before yielding
            if job_id and title:
                yield {
                    'job_id': job_id,
                    'title': title.strip(),
                    'url': url,
                    'date_posted': date_posted.strip() if date_posted else "Unknown",
                    'location': location.strip() if location else "Unspecified",
                    'description': self._clean_text(raw_description),
                    'qualifications': qualifications,
                    'experience_requirements': experience.replace('Experience:', '').strip() if experience else None,
                    'hiring_organization': 'Accenture'
                }

        # --- Pagination Logic ---
        # Accenture uses JavaScript to load the next page, but their URL structure 
        # usually supports appending ?pg=X or ?page=X. 
        # We check if there's a "Next" button in the pagination footer.
        next_button_disabled = response.css('button.rad-pagination__next::attr(disabled)').get()
        
        if next_button_disabled is None and len(job_cards) > 0:
            self.current_page += 1
            
            # Base URL without existing pagination parameters
            base_url = response.url.split('?')[0]
            next_page_url = f"{base_url}?page={self.current_page}"
            
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def _clean_text(self, raw_html):
        """
        Strips HTML tags and standardizes whitespace for clean JSON formatting.
        """
        if not raw_html:
            return None
        text = remove_tags(raw_html)
        return " ".join(text.split())

if __name__ == "__main__":
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_INDENT': 4,
        'FEED_URI': SITE_CONFIG["accenture"]["output_file"],
        'LOG_LEVEL': 'INFO',
    })
    process.crawl(AccentureJobsSpider)
    process.start()