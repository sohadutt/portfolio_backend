import subprocess
import json
import os
class ScraperManager:
    """
    A reusable class to trigger Scrapy spiders safely on demand.
    """
    def __init__(self, site_name="deloitte"):
        self.spider_script = f"{site_name}_spider.py"
        self.output_file = f"{site_name}_jobs_output.json"

    def run_scraper(self):
        """
        Executes the spider safely in a separate process and returns the scraped data.
        You can call this method as many times as you want.
        """
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

    def load_data(self):
        """Internal method to read and return the JSON data."""
        if not os.path.exists(self.output_file):
            print("No output file found. The spider may have failed or found no jobs.")
            return []
            
        with open(self.output_file, 'r', encoding='utf-8') as f:
            return json.load(f)