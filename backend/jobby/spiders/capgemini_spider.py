import scrapy
import json
from w3lib.html import remove_tags
from tqdm import tqdm
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from res import URLS, OUTPUT_FILES