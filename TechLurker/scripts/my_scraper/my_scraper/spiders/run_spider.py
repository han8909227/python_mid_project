
import os
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

from TechLurker.scripts.my_scraper.my_scraper.spiders.reddit_lp_spider import Reddit_lp
from TechLurker.scripts.my_scraper.my_scraper.spiders.reddit_dp_spider import Reddit_dp
from TechLurker.scripts.my_scraper.my_scraper.spiders.tr_employment_spider import Tr_employment
from TechLurker.scripts.my_scraper.my_scraper.spiders.tr_security_spider import Tr_security
from TechLurker.scripts.my_scraper.my_scraper.spiders.tr_webdev_spider import Tr_webdev
from TechLurker.scripts.my_scraper.my_scraper.spiders.tr_os_win_spider import Tr_os_win
from TechLurker.scripts.my_scraper.my_scraper.spiders.tr_software_spider import Tr_software
from TechLurker.scripts.my_scraper.my_scraper.spiders.pyjob_detail_spider import PyjobSpider_detail
from TechLurker.scripts.my_scraper.my_scraper.spiders.security_news_spider import Secuirty_news

# from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
import nltk

def spider_crawl():
    nltk.download('punkt')
    settings = Settings()

    configure_logging()

    setting_path = os.environ.get('PROJ_PATH')
    settings.setmodule(setting_path, priority='project')

    runner = CrawlerRunner(settings)

    spiders = [Reddit_lp, Reddit_dp, PyjobSpider_detail, Tr_employment, Tr_security, Tr_software, Tr_os_win, Tr_webdev, Secuirty_news]

    @defer.inlineCallbacks
    def crawl():
        for spider in spiders:
            yield runner.crawl(spider)
        reactor.stop()

    crawl()
    reactor.run()  # the script will block here until the last crawl call is finished
