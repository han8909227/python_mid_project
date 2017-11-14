import scrapy
from scrapy import Request
from my_scraper.items import IndeedItem


class Indeed_spider(scrapy.Spider):
    name = "indeed"
    allowed_domains = ["indeed.com"]
    start_urls = ["https://www.indeed.com/q-software-engineer-l-Seattle,-WA-jobs.html"]

    def parse(self, response):
        item = IndeedItem()
        titles = response.xpath('//td[@id="resultsCol"]/div[@class="  row  result"]/h2/a/@title').extract()
        for title in titles:
            item['title'] = title
            yield item
        relative_next_url = response.xpath('//a[contains(@href, "/jobs?q=")]/@href')[-2].extract()
        absolute_next_url = "https://indeed.com" + relative_next_url
        yield Request(absolute_next_url, callback=self.parse)
