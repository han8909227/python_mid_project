import scrapy
from scrapy import Request
from TechLurker.scripts.my_scraper.my_scraper.items import RecruitItem


class PyjobSpider_detail(scrapy.Spider):
    name = "pyjobd"
    allowed_domains = ["python.org"]
    start_urls = ["https://www.python.org/jobs/"]

    def parse(self, response):
        jobs = response.xpath('//ol/li')
        for job in jobs:
            relative_url = job.xpath('h2/span/a/@href').extract_first()
            absolute_url = response.urljoin(relative_url)
            title = job.xpath('h2/span/a/text()').extract()[0]
            address = job.xpath('h2/span/a/text()').extract()[1]
            job_type = job.xpath('span/a/text()').extract()
            # company = job.xpath('h2/span/text()').extract()
            yield Request(absolute_url, callback=self.parse_page, meta={'URL': absolute_url, 'Title': title, 'Loc': address, 'JobType': job_type})
        relative_next_url = response.xpath('//a[contains(@href, "?page=")]/@href')[-1].extract()
        absolute_next_url = "https://www.python.org/jobs/" + relative_next_url
        yield Request(absolute_next_url, callback=self.parse)

    def parse_page(self, response):
        item = RecruitItem()
        item['url'] = response.meta.get('URL')
        item['title'] = response.meta.get('Title')
        item['loc'] = response.meta.get('Loc')
        item['job_type'] = response.meta.get('JobType')
        item['descrip'] = response.xpath('//div[@class="job-description"]/p/text()').extract()
        yield item
