import scrapy
import json
from w3lib.html import remove_tags
from tqdm import tqdm
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from res import SITE_CONFIG

class KPMGJobsSpider(scrapy.Spider):
    name = "kpmg_jobs"
    allowed_domains = ["ejgk.fa.em2.oraclecloud.com"]
    start_urls = [SITE_CONFIG["kpmg"]["url"]]

    custom_settings = {
        'FEEDS': {
            SITE_CONFIG["kpmg"]["output_file"]: {
                'format': 'json',
                'indent': 4,
                'overwrite': True,
            }
        },
        'LOG_LEVEL': 'DEBUG',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.offset = 0
        self.limit = 25
        self.site_number = "CX_3001"
        self.api_base = "https://ejgk.fa.em2.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(KPMGJobsSpider, cls).from_crawler(crawler, *args, **kwargs)
        spider.pbar = tqdm(desc="Jobs Scraped", unit="job")
        crawler.signals.connect(spider.item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def item_scraped(self, item, response, spider):
        self.pbar.update(1)

    def spider_closed(self, spider):
        self.pbar.close()

    def start_requests(self):
        # We start by hitting the API, not the browser URL
        api_url = f"{self.api_base}?onlyData=true&expand=requisitionList.reqFlexfields&finder=findReqs;siteNumber={self.site_number},limit={self.limit},offset={self.offset}"
        yield scrapy.Request(url=api_url, callback=self.parse_api_list, headers={'Accept': 'application/json'})

    def parse(self, response):
        # This is a mandatory fallback method for Scrapy to satisfy the interface
        pass

    def parse_api_list(self, response):
        data = json.loads(response.text)
        items = data.get('items', [])
        
        job_list = items[0]['requisitionList'] if items and 'requisitionList' in items[0] else []

        for job in job_list:
            job_id = job.get('Id')
            if not job_id:
                continue
            
            job_detail_url = f"{self.api_base}/{job_id}?expand=all"
            yield scrapy.Request(
                url=job_detail_url,
                callback=self.parse_job_details,
                headers={'Accept': 'application/json'},
                meta={'job_url': f"https://ejgk.fa.em2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/{self.site_number}/job/{job_id}"}
            )

        if len(job_list) == self.limit:
            self.offset += self.limit
            next_api_url = f"{self.api_base}?onlyData=true&expand=requisitionList.reqFlexfields&finder=findReqs;siteNumber={self.site_number},limit={self.limit},offset={self.offset}"
            yield scrapy.Request(url=next_api_url, callback=self.parse_api_list, headers={'Accept': 'application/json'})

    def parse_job_details(self, response):
        job_data = json.loads(response.text)
        if 'items' in job_data and len(job_data['items']) > 0:
            job_data = job_data['items'][0]

        raw_description = job_data.get('ShortDescription', '') + " " + job_data.get('Description', '')
        desc_sel = scrapy.Selector(text=raw_description)
        
        # Proven robust XPath for qualification/experience headers
        quals_xpath = './/*[self::p or self::h2 or self::h3 or self::h4 or self::div or self::strong or self::b][(contains(translate(., "QUALIFICATION", "qualification"), "qualification") or contains(translate(., "QUALIFY", "qualify"), "qualify")) and string-length(normalize-space(.)) < 45]/following::ul[1]//li//text()'
        quals = desc_sel.xpath(quals_xpath).getall()
        
        exp_xpath = './/*[self::p or self::h2 or self::h3 or self::h4 or self::div or self::strong or self::b][contains(translate(., "EXPERIENCE", "experience"), "experience") and string-length(normalize-space(.)) < 45]/following::ul[1]//li//text()'
        exp = desc_sel.xpath(exp_xpath).getall()

        yield {
            'job_id': str(job_data.get('Id')),
            'title': job_data.get('Title'),
            'url': response.meta['job_url'],
            'date_posted': job_data.get('PostedDate', 'Unknown')[:10],
            'location': job_data.get('PrimaryLocation', 'Unspecified'),
            'description': self._clean_text(raw_description),
            'qualifications': " | ".join([q.strip() for q in quals if q.strip()]) if quals else None,
            'experience_requirements': " | ".join([e.strip() for e in exp if e.strip()]) if exp else None,
            'hiring_organization': 'KPMG'
        }

    def _clean_text(self, raw_html):
        if not raw_html: return None
        return " ".join(remove_tags(raw_html).split())

if __name__ == "__main__":
    process = CrawlerProcess(settings={
        'FEEDS': {
            SITE_CONFIG["kpmg"]["output_file"]: {
                'format': 'json',
                'indent': 4,
                'overwrite': True,
            }
        },
        'LOG_LEVEL': 'DEBUG',
    })
    process.crawl(KPMGJobsSpider)
    process.start()