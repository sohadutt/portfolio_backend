import scrapy
import json
from w3lib.html import remove_tags
from tqdm import tqdm
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from res import SITE_CONFIG

class EYJobsSpider(scrapy.Spider):
    name = "ey_jobs"
    allowed_domains = ["careers.ey.com"]
    start_urls = [SITE_CONFIG["ey"]["url"]]

    custom_settings = {
        'FEEDS': {
            SITE_CONFIG["ey"]["output_file"]: {
                'format': 'json',
                'indent': 4,
                'overwrite': True,
            }
        },
        'LOG_LEVEL': 'INFO',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(EYJobsSpider, cls).from_crawler(crawler, *args, **kwargs)
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
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        rows = response.css('table#searchresults tbody tr.data-row')
        
        for row in rows:
            title_link = row.css('td.colTitle a.jobTitle-link')
            if not title_link:
                continue
                
            job_url = response.urljoin(title_link.attrib['href'])
            
            meta_data = {
                'job_id': job_url.split('/')[-2] if len(job_url.split('/')) > 2 else None,
                'title': title_link.css('::text').get(default='').strip(),
                'url': job_url,
                'location': row.css('td.colLocation span.jobLocation::text').get(default='').strip(),
                'hiring_organization': 'EY'
            }
            
            yield scrapy.Request(
                url=job_url, 
                callback=self.parse_job, 
                meta={'job_data': meta_data}
            )

        next_page = response.css('ul.pagination li.active + li a::attr(href)').get() 
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_job(self, response):
        job = response.meta['job_data']
        ld_json_data = response.xpath('//script[@type="application/ld+json"]/text()').get()
        
        if ld_json_data:
            try:
                json_info = json.loads(ld_json_data)
                job['date_posted'] = json_info.get('datePosted')
                job['description'] = self._clean_text(json_info.get('description'))
                job['qualifications'] = self._clean_text(json_info.get('qualifications'))
                job['experience_requirements'] = self._clean_text(json_info.get('experienceRequirements'))
            except json.JSONDecodeError:
                self._html_fallback(response, job)
        else:
            self._html_fallback(response, job)
            
        yield job

    def _html_fallback(self, response, job):
        desc_container = response.css('.jobdescription')
        if not desc_container:
            desc_container = response.css('.jobDisplay .content')

        raw_desc = desc_container.get() or ""
        job['description'] = self._clean_text(raw_desc)
        
        date_posted = response.css('meta[itemprop="datePosted"]::attr(content)').get()
        if not date_posted:
            date_posted = response.css('span[data-careersite-propertyid="date"]::text').get()
        job['date_posted'] = date_posted.strip() if date_posted else None

        # Limiting string length to < 45 chars ensures we only match actual Headers, ignoring full paragraphs
        quals_xpath = './/*[self::p or self::h2 or self::h3 or self::h4 or self::div or self::strong or self::b][(contains(translate(., "QUALIFICATION", "qualification"), "qualification") or contains(translate(., "QUALIFY", "qualify"), "qualify")) and string-length(normalize-space(.)) < 45]/following::ul[1]//li//text()'
        quals = desc_container.xpath(quals_xpath).getall()
        job['qualifications'] = " | ".join([q.strip() for q in quals if q.strip()]) if quals else None

        exp_xpath = './/*[self::p or self::h2 or self::h3 or self::h4 or self::div or self::strong or self::b][contains(translate(., "EXPERIENCE", "experience"), "experience") and string-length(normalize-space(.)) < 45]/following::ul[1]//li//text()'
        exp = desc_container.xpath(exp_xpath).getall()
        job['experience_requirements'] = " | ".join([e.strip() for e in exp if e.strip()]) if exp else None

    def _clean_text(self, raw_html):
        if not raw_html:
            return None
        text = remove_tags(raw_html)
        return " ".join(text.split())

if __name__ == "__main__":
    process = CrawlerProcess(settings={
        'FEEDS': {
            SITE_CONFIG["ey"]["output_file"]: {
                'format': 'json',
                'indent': 4,
                'overwrite': True,
            }
        },
        'LOG_LEVEL': 'INFO',
    })
    process.crawl(EYJobsSpider)
    process.start()