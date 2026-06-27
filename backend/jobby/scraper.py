import scrapy
import json
import w3lib
from scrapy import signals
from typing import Dict

URLS = ['https://www.deloitte.com/in/en/careers/',
        'https://www.accenture.com/in-en/careers/jobsearch',
        'https://www.mckinsey.com/careers/search-jobs',
        'https://www.bain.com/careers/',
        'https://www.bcg.com/careers',
        'https://www.ey.com/en_in/careers',
        'https://www.pwc.com/gx/en/careers.html',
        'https://www.kpmg.com/careers',
        'https://www.capgemini.com/careers/',
        'https://www.tcs.com/careers',
        'https://career.infosys.com/jobs/jobsStatus?companyhiringtype=IL&countrycode=IN',
        'https://careers.wipro.com',
        'https://www.hcltech.com/careers',
        'https://www.lntinfotech.com/careers/',
        'https://www.techmahindra.com/careers/',
        'https://www.larsentoubro.com/careers/',
        'https://www.mahindra.com/careers',
        'https://www.adityabirla.com/careers',
        'https://www.reliancecareers.com/',
        'https://www.jpmorganchase.com/careers',
        'https://www.goldmansachs.com/careers/',
        'https://www.bankofamerica.com/careers/',
        'https://www.citigroup.com/citi/careers/',
        'https://www.wellsfargo.com/careers/',
        'https://www.hsbc.com/careers/',
        'https://www.barclays.com/careers/',
        'https://www.credit-suisse.com/careers/',
        'https://www.deutschebank.com/careers/',
        'https://www.jpmorgan.com/careers/',
        'https://www.morganstanley.com/careers/',
        'https://www.goldmansachs.com/careers/',
        'https://www.ubs.com/global/en/careers.html',
        'https://www.credit-suisse.com/careers/',
        'https://www.nomura.com/careers/',
        'https://www.barclays.com/careers/',
        'https://www.hsbc.com/careers/',
        'https://www.standardchartered.com/careers/',
        'https://www.rbs.com/careers/',
        'https://icbpjb.fa.ocs.oraclecloud.com/hcmUI/CandidateExperience/en/sites/LazardProfessionalCareers/jobs']


class JobsStore:
    def __init__(self):
        self._jobs: Dict[int, dict] = {}
        self._next_id = 1
    
    def add_job(self, category: str, location: str, title: str, description: str, requirements: str, company: str, tags: list, match_score: float) -> int:
        job_id = self._next_id
        self._jobs[job_id] = {
            "category": category,
            "location": location,
            "title": title,
            "description": description,
            "requirements": requirements,
            "company": company,
            "tags": tags,
            "match_score": match_score
        }
        self._next_id += 1
        return job_id

class JobProcessor:
    @staticmethod
    def process_job_data(job_data):
        cleaned_data = {}
        
        data = {}
        
        return data
    
class JobService:
    def __init__(self):
        self.jobs_store = JobsStore()
        self.job_processor = JobProcessor()
    
    def add_job(self, category: str, location: str, title: str, description: str, requirements: str, company: str, tags: list, match_score: float) -> int:
        job_id = self.jobs_store.add_job(category, location, title, description, requirements, company, tags, match_score)
        return job_id

class JobScraper(scrapy.Spider):
    name = 'job_scraper'

    def start_spider(self):
        for url in URLS:
            yield scrapy.Request(url=url, callback=self.parse)

class Parser:
    @staticmethod
    def parse_job_data(data):
        cleaned_data = w3lib.html.remove_tags(data)
        return cleaned_data

