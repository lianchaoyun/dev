# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class jwhuspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class MMDItem(scrapy.Item):
    action = scrapy.Field()
    cat_name = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()


class URLSItem(scrapy.Item):
    action = scrapy.Field()
    name = scrapy.Field()
    urls = scrapy.Field()
