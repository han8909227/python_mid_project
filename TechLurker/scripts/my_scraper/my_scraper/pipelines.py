# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pyramid.config import Configurator
import os
from TechLurker.models import AllData


def main():
    """ This function returns a Pyramid WSGI application.
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
        record = AllData(title=item['title'],
                         content=' '.join(item['content']),
                         score=item['score'])

        try:
            self.session.add(record)
            self.session.commit()
        except:
            raise ValueError('fail')
        return item

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            url=os.environ['DATABASE_URL'])

    def open_spider(self, spider):
        self.session = main()

    def close_spider(self, spider):
        self.session.close()
