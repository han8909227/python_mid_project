# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RecruitItem(scrapy.Item):
    """Python job."""

    title = scrapy.Field()
    descrip = scrapy.Field()
    loc = scrapy.Field()
    job_type = scrapy.Field()
    url = scrapy.Field()


class NewsItem(scrapy.Item):
    """Cyber security news."""

    title = scrapy.Field()
    articleContent = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()


class PostItem(scrapy.Item):
    """Reddit forums only."""

    title = scrapy.Field()
    content = scrapy.Field()
    score = scrapy.Field()


class IndeedItem(scrapy.Item):
    """Indeed."""

    title = scrapy.Field()


class TechRepulicItem(scrapy.Item):
    """Tech repulic forums only."""

    title = scrapy.Field()
    content = scrapy.Field()
    votes = scrapy.Field()
    from_forum = scrapy.Field()
