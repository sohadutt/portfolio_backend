import sys
if "twisted.internet.reactor" not in sys.modules:
    from twisted.internet import asyncioreactor
    asyncioreactor.install()

import scrapy
from w3lib.html import remove_tags
from tqdm import tqdm
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy_playwright.page import PageMethod
from res import SITE_CONFIG

class AccentureJobsSpider(scrapy.Spider):
    name = "accenture_jobs"
    allowed_domains = ["accenture.com"]
    start_urls = [SITE_CONFIG["accenture"]["url"]]

    custom_settings = {
        'FEEDS': {
            SITE_CONFIG["accenture"]["output_file"]: {
                'format': 'json',
                'indent': 4,
                'overwrite': True,
            }
        },
        'LOG_LEVEL': 'INFO',
        'DOWNLOAD_HANDLERS': {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        'TWISTED_REACTOR': "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        'PLAYWRIGHT_LAUNCH_OPTIONS': {
            'headless': True,
        }
    }

    def __init__(self, *args, **kwargs):
        super(AccentureJobsSpider, self).__init__(*args, **kwargs)
        self.current_page = 1

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(AccentureJobsSpider, cls).from_crawler(crawler, *args, **kwargs)
        spider.pbar = tqdm(desc="Jobs Scraped", unit="job")
        crawler.signals.connect(spider.item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def item_scraped(self, item, response, spider):
        self.pbar.update(1)

    def spider_closed(self, spider):
        self.pbar.close()

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url, 
                callback=self.parse,
                errback=self.errback_close,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_load_state", "networkidle"),
                        PageMethod("wait_for_timeout", 3000)
                    ]
                }
            )

    def parse(self, response):
        job_cards = response.css('div.rad-filters-vertical__job-card')

        if not job_cards:
            self.logger.info("No job cards found. Assume end of pagination.")
            return

        for card in job_cards:
            job_id = card.css('button.rad-save-job::attr(data-job-id)').get()
            title = card.css('h3.rad-filters-vertical__job-card-title::text').get()
            
            if not job_id or not title:
                continue
            
            url = card.css('a.rad-filters-vertical__job-card-content-link-button::attr(href)').get()
            location = card.css('span.rad-filters-vertical__job-card-details-location::text').get()
            date_posted = card.css('span.rad-filters-vertical__job-card-content-job-posted-date-dynamic-text::text').get()
            experience = card.css('span.rad-filters-vertical__job-card-details-type::text').get()
            skill = card.css('span.rad-filters-vertical__job-card-details-skills-dynamic-text::text').get()
            raw_description = card.css('div.rad-filters-vertical__job-card-content-job-description-dynamic-text::text').get()

            qualifications = f"{experience if experience else ''} | Required Skill: {skill if skill else ''}".strip(' |')

            yield {
                'job_id': job_id,
                'title': title.strip(),
                'url': response.urljoin(url) if url else None,
                'date_posted': date_posted.strip() if date_posted else "Unknown",
                'location': location.strip() if location else "Unspecified",
                'description': self._clean_text(raw_description),
                'qualifications': qualifications,
                'experience_requirements': experience.replace('Experience:', '').strip() if experience else None,
                'hiring_organization': 'Accenture'
            }

        self.current_page += 1
        base_url = response.url.split('?')[0]
        next_page_url = f"{base_url}?page={self.current_page}"
        
        yield scrapy.Request(
            url=next_page_url, 
            callback=self.parse,
            errback=self.errback_close,
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_load_state", "networkidle"),
                    PageMethod("wait_for_timeout", 3000)
                ]
            }
        )

    def errback_close(self, failure):
        self.logger.info(f"Playwright timeout or error reached. Closing gracefully. {failure.getErrorMessage()}")

    def _clean_text(self, raw_html):
        if not raw_html:
            return None
        text = remove_tags(raw_html)
        return " ".join(text.split())

if __name__ == "__main__":
    process = CrawlerProcess(settings={
        'FEEDS': {
            SITE_CONFIG["accenture"]["output_file"]: {
                'format': 'json',
                'indent': 4,
                'overwrite': True,
            }
        },
        'LOG_LEVEL': 'INFO',
        'DOWNLOAD_HANDLERS': {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        'TWISTED_REACTOR': "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    })
    process.crawl(AccentureJobsSpider)
    process.start()