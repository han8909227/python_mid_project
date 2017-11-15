
# # import scrapy
# # from scrapy.crawler import CrawlerProcess
# # from reddit_lp_spider import Reddit_lp
# # from scrapy.utils.project import get_project_settings


# # process = CrawlerProcess(get_project_settings())

# # process.crawl(Reddit_lp)
# # process.start()


# import sys
# import os
# from scrapy.utils.project import get_project_settings
# from reddit_lp_spider import Reddit_lp
# from pyjob_detail_spider import PyjobSpider_detail
# from scrapy import signals, log
# from twisted.internet import reactor
# from scrapy.crawler import Crawler


# class CrawlRunner:

#     def __init__(self):
#         self.running_crawlers = []

#     def spider_closing(self, spider):
#         # log.msg("Spider closed: %s" % spider, level=log.INFO)
#         self.running_crawlers.remove(spider)
#         if not self.running_crawlers:
#             reactor.stop()

#     def run(self):

#         # sys.path.append(os.path.join(os.path.curdir, "my_scraper/spiders"))
#         # os.environ['SCRAPY_SETTINGS_MODULE'] = 'scrapy_somesite.settings'
#         settings = get_project_settings()
#         # log.start(loglevel=log.DEBUG)

#         to_crawl = [Reddit_lp, PyjobSpider_detail]

#         for spider in to_crawl:

#             crawler = Crawler(settings)
#             crawler_obj = spider()
#             self.running_crawlers.append(crawler_obj)

#             crawler.signals.connect(self.spider_closing, signal=signals.spider_closed)
#             crawler.configure()
#             crawler.crawl(crawler_obj)
#             crawler.start()

#         reactor.run()
