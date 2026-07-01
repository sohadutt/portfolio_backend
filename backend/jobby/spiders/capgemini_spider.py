import json
from urllib.parse import urlencode

import scrapy
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from tqdm import tqdm
from w3lib.html import remove_tags

from res import SITE_CONFIG


class CapgeminiJobsSpider(scrapy.Spider):
    """
    Spider to extract India job postings from Capgemini's public JobStream API.
    """
    name = "capgemini_jobs"
    allowed_domains = ["cg-jobstream-api.azurewebsites.net"]
    api_base = "https://cg-jobstream-api.azurewebsites.net/api/job-search"
    country_code = "en-in"
    page_size = 50

    custom_settings = {
        "FEEDS": {
            SITE_CONFIG["capgemini"]["output_file"]: {
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
        "DEFAULT_REQUEST_HEADERS": {
            "Accept": "application/json",
            "Origin": "https://www.capgemini.com",
            "Referer": SITE_CONFIG["capgemini"]["url"],
        },
    }

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(CapgeminiJobsSpider, cls).from_crawler(crawler, *args, **kwargs)
        spider.pbar = tqdm(desc="Jobs Scraped", unit="job")
        crawler.signals.connect(spider.item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def item_scraped(self, item, response, spider):
        self.pbar.update(1)

    def spider_closed(self, spider):
        self.pbar.close()

    async def start(self):
        yield self._first_page_request()

    def start_requests(self):
        yield self._first_page_request()

    def parse(self, response):
        pass

    def parse_api_list(self, response):
        try:
            payload = json.loads(response.text)
        except json.JSONDecodeError:
            self.logger.error("Failed to decode Capgemini API response on %s", response.url)
            return

        jobs = payload.get("data") or []
        total = int(payload.get("total") or payload.get("count") or 0)
        page = response.meta.get("page", 1)

        for job in jobs:
            yield self._format_job(job)

        if jobs and page * self.page_size < total:
            next_page = page + 1
            yield scrapy.Request(
                url=self._build_api_url(page=next_page),
                callback=self.parse_api_list,
                meta={"page": next_page},
            )

    def _build_api_url(self, page):
        params = {
            "page": page,
            "size": self.page_size,
            "country_code": self.country_code,
        }
        return f"{self.api_base}?{urlencode(params)}"

    def _first_page_request(self):
        return scrapy.Request(
            url=self._build_api_url(page=1),
            callback=self.parse_api_list,
            meta={"page": 1},
        )

    def _format_job(self, job):
        raw_description = job.get("description") or job.get("description_stripped") or ""
        cleaned_description = self._clean_text(raw_description)

        return {
            "job_id": str(job.get("id") or job.get("ref") or job.get("_id")),
            "title": job.get("title"),
            "url": job.get("apply_job_url") or job.get("wp_url") or SITE_CONFIG["capgemini"]["url"],
            "date_posted": self._format_date(job.get("indexed_at") or job.get("updated_at")),
            "location": job.get("location") or "India",
            "description": cleaned_description,
            "qualifications": self._extract_qualifications(raw_description),
            "experience_requirements": (
                self._extract_experience(raw_description)
                or job.get("experience_level")
                or job.get("professional_communities")
            ),
            "hiring_organization": job.get("brand") or "Capgemini",
        }

    def _extract_qualifications(self, raw_html):
        return self._extract_list_after_heading(raw_html, ["qualification", "qualify", "technical skills"])

    def _extract_experience(self, raw_html):
        return self._extract_list_after_heading(raw_html, ["experience", "grade specific"])

    def _extract_list_after_heading(self, raw_html, keywords):
        if not raw_html:
            return None

        selector = scrapy.Selector(text=raw_html)
        keyword_match = " or ".join(
            f'contains(translate(., "{keyword.upper()}", "{keyword.lower()}"), "{keyword.lower()}")'
            for keyword in keywords
        )
        xpath = (
            ".//*[self::p or self::h2 or self::h3 or self::h4 or self::div or self::strong or self::b]"
            f"[({keyword_match}) and string-length(normalize-space(.)) < 60]"
            "/following::ul[1]//li//text()"
        )
        values = [value.strip() for value in selector.xpath(xpath).getall() if value.strip()]
        return " | ".join(values) if values else None

    def _format_date(self, value):
        if not value:
            return None
        return str(value)[:10]

    def _clean_text(self, raw_html):
        if not raw_html:
            return None
        return " ".join(remove_tags(raw_html).split())


if __name__ == "__main__":
    process = CrawlerProcess(
        settings={
            "FEEDS": {
                SITE_CONFIG["capgemini"]["output_file"]: {
                    "format": "json",
                    "indent": 4,
                    "overwrite": True,
                }
            },
            "LOG_LEVEL": "INFO",
        }
    )
    process.crawl(CapgeminiJobsSpider)
    process.start()
