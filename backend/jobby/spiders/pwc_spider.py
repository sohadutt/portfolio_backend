import json
import re

import scrapy
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from tqdm import tqdm
from w3lib.html import remove_tags

from res import SITE_CONFIG


class PWCJobsSpider(scrapy.Spider):
    """
    Spider to extract job postings from PwC India's current opportunities page.
    The page embeds a JavaScript dbdata array with the public job listing data.
    """
    name = "pwc_jobs"
    allowed_domains = ["pwc.in", "pwc.darwinbox.com", "pwc.wd3.myworkdayjobs.com"]
    start_urls = [SITE_CONFIG["pwc"]["url"]]

    custom_settings = {
        "FEEDS": {
            SITE_CONFIG["pwc"]["output_file"]: {
                "format": "json",
                "indent": 4,
                "overwrite": True,
            }
        },
        "LOG_LEVEL": "INFO",
        "USER_AGENT": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
    }

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(PWCJobsSpider, cls).from_crawler(crawler, *args, **kwargs)
        spider.pbar = tqdm(desc="Jobs Scraped", unit="job")
        crawler.signals.connect(spider.item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def item_scraped(self, item, response, spider):
        self.pbar.update(1)

    def spider_closed(self, spider):
        self.pbar.close()

    async def start(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        jobs = self._extract_dbdata(response.text)
        if not jobs:
            self.logger.warning("No PwC dbdata array found on %s", response.url)
            return

        for job in jobs:
            if self._is_test_job(job):
                continue

            yield self._format_job(job)

    def _extract_dbdata(self, html):
        match = re.search(r"var\s+dbdata\s*=\s*(\[.*?\])\s*;", html, re.S)
        if not match:
            return []

        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            self.logger.error("Failed to decode PwC dbdata JSON.")
            return []

    def _format_job(self, job):
        title = self._clean_text(job.get("title"))
        location = self._clean_text(job.get("location")) or "India"
        line_of_service = self._clean_text(job.get("los"))
        job_id = job.get("jobid") or job.get("jobreqid") or job.get("reqid")
        description_parts = [
            title,
            f"Line of service: {line_of_service}" if line_of_service else None,
            f"Location: {location}" if location else None,
        ]

        return {
            "job_id": str(job_id),
            "title": title,
            "url": job.get("apply"),
            "date_posted": None,
            "location": location,
            "description": ". ".join(part for part in description_parts if part),
            "qualifications": line_of_service,
            "experience_requirements": None,
            "hiring_organization": "PwC India",
        }

    def _is_test_job(self, job):
        title = (job.get("title") or "").lower()
        return "testing purpose" in title or "do not apply" in title

    def _clean_text(self, raw_text):
        if not raw_text:
            return None
        return " ".join(remove_tags(str(raw_text)).split())


if __name__ == "__main__":
    process = CrawlerProcess(
        settings={
            "FEEDS": {
                SITE_CONFIG["pwc"]["output_file"]: {
                    "format": "json",
                    "indent": 4,
                    "overwrite": True,
                }
            },
            "LOG_LEVEL": "INFO",
        }
    )
    process.crawl(PWCJobsSpider)
    process.start()
