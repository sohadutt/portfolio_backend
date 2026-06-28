import scrapy
import json
import tqdm
import w3lib
from scrapy import signals
from typing import Dict, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from django.conf import settings

URLS = ['https://www.deloitte.com/in/en/careers/',
        'https://www.accenture.com/in-en/careers/jobsearch',
        'https://careers.ey.com/ey/search/?createNewAlert=false&q=&locationsearch&local=en_US',
        'https://www.pwc.in/careers/experienced-jobs.html',
        'https://ejgk.fa.em2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_3001/jobs',
        'https://www.capgemini.com/careers/join-capgemini/job-search/',]

MAIN_PROCESS_PROMPT = """
You are a job matching assistant.
User Portfolio: {portfolio}

Analyze the following batch of job descriptions. 
For each job, determine how well it matches the user's portfolio.

Return ONLY a valid JSON array of objects. Do not include markdown formatting or backticks.
Each object must contain EXACTLY these keys:
- "batch_index": The integer index provided in the prompt.
- "match_score": A float between 0 and 100.
- "tags": A list of relevant string tags.

Job Descriptions: {jobs}
"""

class JobsStore:
    def __init__(self):
        self._jobs: Dict[int, dict] = {}
        self._next_id = 1
    
    def add_job(self, job_data: dict) -> int:
        job_id = self._next_id
        job_data["internal_id"] = job_id 
        self._jobs[job_id] = job_data
        self._next_id += 1
        return job_id

    def get_all_jobs(self) -> List[dict]:
        return list(self._jobs.values())

class AIJobProcessor:
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=settings.GEMINI_API_KEY)
    @staticmethod
    async def process_batch(self, jobs_chunk: List[dict], user_portfolio: dict) -> List[dict]:       
        jobs_for_prompt = []
        for idx, job in enumerate(jobs_chunk):
            cleaned_desc = w3lib.html.remove_tags(job.get("description", ""))
            jobs_for_prompt.append({
                "batch_index": idx,
                "title": job.get("title", ""),
                "description": cleaned_desc[:2000] 
            })
        
        prompt = MAIN_PROCESS_PROMPT.format(
            portfolio=json.dumps(user_portfolio),
            jobs=json.dumps(jobs_for_prompt)
        )       
        try:
            response = await self.llm.ainvoke([HumanMessage(content=prompt)])
            response_text = response.content.replace('```json', '').replace('```', '').strip()
            ai_results = json.loads(response_text)          
            for result in ai_results:
                idx = result.get("batch_index")
                if idx is not None and 0 <= idx < len(jobs_chunk):
                    jobs_chunk[idx]["match_score"] = result.get("match_score", 0)
                    jobs_chunk[idx]["tags"] = result.get("tags", [])
                  
        except Exception as e:
            print(f"Error processing AI batch: {e}")
            for job in jobs_chunk:
                job["match_score"] = 0
                job["tags"] = []
                
        return jobs_chunk

class JobBatchPipeline:
    """
    Scrapy pipeline to chunk items, send them to the AI, 
    store them in JobsStore, and export a single JSON at the end.
    """
    def __init__(self):
        self.batch = []
        self.chunk_size = 50
        self.store = JobsStore()
        self.portfolio = {"skills": ["Python", "Django", "Scrapy"], "experience": "3 years"}

    async def process_item(self, item, spider):
        self.batch.append(dict(item))
        if len(self.batch) >= self.chunk_size:
            await self._flush_batch()     
        return item

    async def _flush_batch(self):
        if not self.batch:
            return     
        processed_jobs = await AIJobProcessor.process_batch(self.batch, self.portfolio)
        for job in processed_jobs:
            self.store.add_job(job)   
        self.batch = []

    async def close_spider(self, spider):
        await self._flush_batch()       
        all_jobs = self.store.get_all_jobs()
        with open('all_processed_jobs.json', 'w', encoding='utf-8') as f:
            json.dump(all_jobs, f, indent=4, ensure_ascii=False)       
        spider.logger.info(f"Successfully processed and stored {len(all_jobs)} jobs.")

class JobsSpider(scrapy.Spider):
    name = "corporate_jobs"
    custom_settings = {
        'ITEM_PIPELINES': {
            '__main__.JobBatchPipeline': 100,
        },
        'LOG_LEVEL': 'INFO',
    }

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(JobsSpider, cls).from_crawler(crawler, *args, **kwargs)     
        spider.pbar = tqdm(desc="Jobs Scraped & Processed", unit="job")     
        crawler.signals.connect(spider.item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def item_scraped(self, item, response, spider):
        self.pbar.update(1)

    def spider_closed(self, spider):
        self.pbar.close()

    def start_requests(self):
        for url in URLS:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        Dummy parser block. 
        You will need to implement specific parsing logic for each URL domain.
        """
        yield {
            "category": "Software Engineering",
            "location": "Remote",
            "title": "Backend Developer",
            "description": "We are looking for a Python/Django developer...",
            "requirements": "3+ years Python, Scrapy experience.",
            "company": "Tech Corp",
        }