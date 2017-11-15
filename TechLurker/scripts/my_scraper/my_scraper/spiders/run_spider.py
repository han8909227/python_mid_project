
# # # import scrapy
# # # from scrapy.crawler import CrawlerProcess
# # # from reddit_lp_spider import Reddit_lp
# # # from scrapy.utils.project import get_project_settings


# # # process = CrawlerProcess(get_project_settings())

# # # process.crawl(Reddit_lp)
# # # process.start()


# from twisted.internet import reactor, defer
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.log import configure_logging
# from reddit_lp_spider import Reddit_lp
# from pyjob_detail_spider import PyjobSpider_detail
# from scrapy.utils.project import get_project_settings


# configure_logging()
# get_project_settings()
# runner = CrawlerRunner()


# @defer.inlineCallbacks
# def crawl():
#     yield runner.crawl(Reddit_lp)
#     yield runner.crawl(PyjobSpider_detail)
#     reactor.stop()

# crawl()
# reactor.run()  # the script will block here until the last crawl call is finished

