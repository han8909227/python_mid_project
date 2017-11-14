import scrapy
from scrapy import Request
from my_scraper.items import NewsItem


class Secuirty_news(scrapy.Spider):
    name = "security"
    allowed_domains = ["trendmicro.com"]
    start_urls = ["https://www.trendmicro.com/vinfo/us/security/news/all/page/2"]

    def parse(self, response):
        posts = response.xpath('//div[@class="list_Content"]/ul/li')
        for post in posts:

            relative_url = post.xpath('div/a/@href').extract_first()
            absolute_url = response.urljoin(relative_url)

            yield Request(absolute_url, callback=self.parse_page)

        current_pg = response.url.rsplit('/', 1)
        next_pg = current_pg[0] + '/' + str(int(current_pg[1]) + 1)
        yield Request(next_pg, callback=self.parse)
        # relative_next_url = response.xpath('//a[contains(@href, "?page=")]/@href')[-1].extract()
        # absolute_next_url = "https://www.python.org/jobs/" + relative_next_url
        # yield Request(absolute_next_url, callback=self.parse)

    def parse_page(self, response):
        item = NewsItem()
        item['url'] = response.url
        item['title'] = response.xpath('//h1/text()').extract_first()
        item['articleContent'] = response.xpath('//section[@class="articleContent"]/p/text()').extract()
        item['date'] = response.xpath('//div[@id="datePub"]/text()').extract_first()
        yield item
