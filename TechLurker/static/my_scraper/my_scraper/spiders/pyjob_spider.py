import scrapy
from scrapy import Request
from my_scraper.items import RecruitItem


class PyjobSpider(scrapy.Spider):
    name = "pyjob"
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
            company = job.xpath('h2/span/text()').extract()

            yield {
                'title': title,
                'loc': address,
                'url': absolute_url,
                'type': job_type,
                'company': company
            }

            # yield Request(absolute_url, callback=self.parse_page, meta={'URL': absolute_url, 'Title': title, 'Address':address})
        relative_next_url = response.xpath('//a[contains(@href, "?page=")]/@href')[-1].extract()
        absolute_next_url = "https://www.python.org/jobs/" + relative_next_url
        yield Request(absolute_next_url, callback=self.parse)



    # def parse_page(self, response):
    #     item = RecruitItem()
    #     item['url'] = response.meta.get('URL')
    #     item['title'] = response.meta.get('Title')
    #     item['address'] = response.meta.get('Address')
    #     item['description'] = "".join(line for line in response.xpath('//*[@id="postingbody"]/text()').extract()).strip()
    #     item['compensation'] = response.xpath('//p[@class="attrgroup"]/span[1]/b/text()').extract_first()
    #     item['employment_type'] = response.xpath('//p[@class="attrgroup"]/span[2]/b/text()').extract_first()
    #     yield item
