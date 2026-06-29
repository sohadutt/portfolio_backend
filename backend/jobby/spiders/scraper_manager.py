import subprocess
import json
import os
import time
from .res import SITE_CONFIG

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        ex = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__!r} took: {end_time - start_time:.4f} seccond to complete ")
        return ex
    return wrapper

class ScraperManager:
    def __init__(self, site_name="deloitte"):
        site_key = site_name.lower()  
        self.spider_script = f"{site_key}_spider.py"
        self.output_file = SITE_CONFIG[site_key]["output_file"]
        
    @timer
    def run_scraper(self):
        print(f"Starting scraper: {self.spider_script}...")
        
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

        try:
            subprocess.run(["python", self.spider_script], check=True)
            print("Scraping completed successfully.")
            return self.load_data()
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running the spider: {e}")
            return None
            
    @timer
    def load_data(self):
        if not os.path.exists(self.output_file):
            print("No output file found. The spider may have failed or found no jobs.")
            return []
            
        with open(self.output_file, 'r', encoding='utf-8') as f:
            return json.load(f)