# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Source(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    name = scrapy.Field()
    domain = scrapy.Field()
    cookie = scrapy.Field()


class Novel(scrapy.Item):
    id = scrapy.Field()
    source_id = scrapy.Field()
    name = scrapy.Field()
    slug = scrapy.Field()


class NovelChapter(scrapy.Item):
    lang = scrapy.Field()
    novel_id = scrapy.Field()
    source_link = scrapy.Field()
    name = scrapy.Field()
    chapter_number = scrapy.Field()
    slug = scrapy.Field()
    list_language = scrapy.Field()
    date_create = scrapy.Field()
