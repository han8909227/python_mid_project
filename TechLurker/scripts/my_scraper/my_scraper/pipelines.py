# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pyramid.config import Configurator
from TechLurker.models import AllData, PyjobData, SecurityNewsData
import os


def main():
    """ This functon returns a Pyramid WSGI application.
    """
    settings = {}
    settings['sqlalchemy.url'] = os.environ['DATABASE_URL']
    config = Configurator(settings=settings)
    config.include('TechLurker.models')
    SessionFactory = config.registry["dbsession_factory"]
    session = SessionFactory()
    return session


class AddTablePipeline(object):
    def __init__(self, url):
        """."""
        self.url = url

    def process_item(self, item, spider):
        """."""
        if 'content' in item.keys():
            record = AllData(title=item['title'],
                             content=' '.join(item['content']),
                             score=item['score'])
        elif 'job_type' in item.keys():
            record = PyjobData(title=item['title'],
                               descrip=' '.join(item['descrip']),
                               loc=item['loc'],
                               job_type=' '.join(item['job_type']),
                               url=item['url'])
        elif 'articleContent' in item.keys():
            record = SecurityNewsData(title=item['title'],
                                      articleContent=item['articleContent'],
                                      date=item['date'],
                                      url=item['url'])
        try:
            # import pdb; pdb.set_trace()
            self.session.add(record)
            self.session.commit()
        except:
            self.session.rollback()
        return item

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            url=os.environ['DATABASE_URL'])

    def open_spider(self, spider):
        self.session = main()

    def close_spider(self, spider):
        self.session.close()


