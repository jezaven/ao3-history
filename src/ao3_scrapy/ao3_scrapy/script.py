import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.ao3_spider import HistorySpider

process = CrawlerProcess(get_project_settings())

process.crawl(HistorySpider)
process.start() # the script will block here until the crawling is finished
