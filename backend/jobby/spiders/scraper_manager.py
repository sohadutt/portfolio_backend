import subprocess
import json
import os
import time
from config import settings
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
        self.site_name = site_name.lower()
        self.spider_path = os.path.join(settings.BASE_DIR, 'jobby', 'spiders', f'{self.site_name}_spider.py')
        self.output_file = SITE_CONFIG[self.site_name]["output_file"]

    @timer
    def run_scraper(self):
        print(f"DEBUG: Looking for spider at: {self.spider_path}")
        if not os.path.exists(self.spider_path):
            raise FileNotFoundError(f"Spider file not found at: {self.spider_path}")
        print(f"Starting scraper: {self.spider_path}...")
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        try:
            subprocess.run(["python", self.spider_path], check=True, capture_output=True, text=True)
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