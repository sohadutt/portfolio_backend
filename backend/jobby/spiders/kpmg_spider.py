import scrapy
import json
from w3lib.html import remove_tags
from tqdm import tqdm
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from res import SITE_CONFIG

class KPMGJobsSpider(scrapy.Spider):
    """
    Spider to extract job postings from the KPMG (Oracle HCM) portal.
    Structured identically to the Deloitte spider.
    """
    name = "kpmg_jobs"
    allowed_domains = ["ejgk.fa.em2.oraclecloud.com"]
    start_urls = [SITE_CONFIG["kpmg"]["url"]]

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': SITE_CONFIG["kpmg"]["output_file"],
        'FEED_EXPORT_INDENT': 4,
        'LOG_LEVEL': 'DEBUG',
    }

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        """
        Instantiates the spider and connects Scrapy signals to the tqdm progress bar.
        """
        spider = super(KPMGJobsSpider, cls).from_crawler(crawler, *args, **kwargs)
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

    def parse(self, response):
        """
        Parses the main search results page.
        Extracts links to individual job postings and follows pagination.
        """
        job_links = response.css('a.job-list-item__link::attr(href)').getall() 
        job_links = list(set(job_links))

        for link in job_links:
            yield response.follow(link, callback=self.parse_job)

        next_page = response.css('a.paginationNextLink::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_job(self, response):
        """
        Parses individual job pages.
        Locates the application/ld+json block, parses it, and cleans the text.
        """
        ld_json_data = response.xpath('//script[@type="application/ld+json"]/text()').get()

        if ld_json_data:
            try:
                job_data = json.loads(ld_json_data)
                
                yield {
                    'job_id': job_data.get('identifier', {}).get('value') or response.url.split('/')[-1],
                    'title': job_data.get('title'),
                    'url': response.url,
                    'date_posted': job_data.get('datePosted'),
                    'location': self._format_location(job_data.get('jobLocation', {})),
                    'description': self._clean_text(job_data.get('description')),
                    'qualifications': self._clean_text(job_data.get('qualifications')),
                    'experience_requirements': self._clean_text(job_data.get('experienceRequirements')),
                    'hiring_organization': job_data.get('hiringOrganization', {}).get('name', 'KPMG')
                }
            except json.JSONDecodeError:
                self.logger.error(f"Failed to decode JSON-LD on {response.url}")
        else:
            yield {
                'job_id': response.url.split('/')[-1],
                'title': response.css('h1.job-details__title::text').get() or response.css('.job-tile__title::text').get(),
                'url': response.url,
                'date_posted': None,
                'location': None,
                'description': self._clean_text(response.css('.job-details__description-content').get()),
                'qualifications': None,
                'experience_requirements': None,
                'hiring_organization': 'KPMG'
            }

    def _format_location(self, location_data):
        """
        Extracts and formats the physical location from the Schema.org Place object.
        """
        # Sometimes Oracle wraps locations in a list
        if isinstance(location_data, list):
            location_data = location_data[0] if location_data else {}
            
        address = location_data.get('address', {})
        locality = address.get('addressLocality', '')
        region = address.get('addressRegion', '')
        
        parts = [part for part in [locality, region] if part]
        return ", ".join(parts) if parts else "Multiple Locations / Unspecified"

    def _clean_text(self, raw_html):
        """
        Strips HTML tags and standardizes whitespace for clean JSON formatting.
        """
        if not raw_html:
            return None
            
        text = remove_tags(raw_html)
        return " ".join(text.split())
    
    def start_requests(self):
        """
        Initiates the scraping process by sending a request to the start URL.
        """
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
            

if __name__ == "__main__":
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_INDENT': 4,
        'FEED_URI': SITE_CONFIG["kpmg"]["output_file"],
        'LOG_LEVEL': 'INFO',
    })
    process.crawl(KPMGJobsSpider)
    process.start()