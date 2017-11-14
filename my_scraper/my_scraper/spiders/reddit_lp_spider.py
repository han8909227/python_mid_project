import scrapy
from scrapy import Request
from my_scraper.items import PostItem


class Reddit_lp(scrapy.Spider):
    name = "redditlp"
    allowed_domains = ["reddit.com"]
    start_urls = ["https://www.reddit.com/r/learnprogramming/"]

    def parse(self, response):
        post_urls = response.xpath('//div[@id="siteTable"]/div/@data-url').extract()
        for post_url in post_urls:
            absolute_url = 'https://www.reddit.com' + post_url

            yield Request(absolute_url, callback=self.parse_page)

        next_url = response.xpath('//span[@class="next-button"]/a/@href').extract_first()
        yield Request(next_url, callback=self.parse)

    def parse_page(self, response):
        item = PostItem()
        item['title'] = response.xpath('//p[@class="title"]/a/text()').extract_first()
        item['score'] = response.xpath('//div[@class="score"]/span/text()').extract_first()
        item['content'] = response.xpath('//form/div[contains(@class, "md-container")]/div[@class="md"]/p/text()').extract()[9:]
        yield item
