import scrapy
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class KSUSpider(CrawlSpider):
    #spider name
    name = "ksu"
    #domain which the spider can crawl
    allowed_domains = ['kennesaw.edu']
    #initial urls to be crawled
    start_urls = ['https://www.kennesaw.edu/',
                  'https://ccse.kennesaw.edu/',
                  'https://fsl.kennesaw.edu/']
    #rules for Link Extractor
    rules = (
        #only allow the LinkExtractor to pull unique urls from the kennesaw.edu domain
        Rule(LinkExtractor(unique=True),callback = 'parse',follow=True),)
    #settings defining spider constraints
    custom_settings = {
        #identify the spider to webservers
        'USER_AGENT': 'KSU CS4422-IRbot/0.1',
        # wait 2.0s beofre downloading consecutive pages
        'DOWNLOAD_DELAY': '2',
        #respect robots.txt policies
        'ROBOTSTXT_OBEY': 'True',
        #run in depth first search (FIFO) order
        'DEPTH_PRIORITY': '1',
        'SCHEDULER_DISK_QUEUE': 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue',
        #terminate crawling once 1000 pages are reached
        'CLOSESPIDER_PAGECOUNT': '1250'}

    def parse(self, response):
        entry = dict.fromkeys(['pageid', 'url', 'title', 'body', 'emails'])
        #get url from response
        entry['url'] = response.request.url
        #use url string to create hashcode
        entry['pageid'] = str(hash(entry['url']))
        #get title text from response
        entry['title'] = response.css('title::text').get()
        #get the body's text
        entry['body'] = ' '.join(response.xpath('//body//p//text()').extract())
        #read emails into list
        entry['emails'] = response.xpath('//a[contains(@href, "mailto")]/@href').re('mailto:([^?]*)')
        yield entry