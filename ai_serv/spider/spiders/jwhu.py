import time

import scrapy
import re
from w3lib.html import remove_tags
from bs4 import BeautifulSoup

# scrapy crawl zuowenwang
#from hub.browser.posts_learn import create
from tinydb import TinyDB, Query

db = TinyDB('./tmp/spiders.json')


# db.insert({'name': 'John', 'age': 22})
# uu = db.search(User.name == 'John1')

class ImageItem(scrapy.Item):
    path = scrapy.Field()  # 图片所属类别
    imgurls = scrapy.Field()  # 图片下载地址


class ZuowenwangSpider(scrapy.Spider):
    name = 'jwhu'
    allowed_domains = ['jwhu.com']
    start_urls = ['http://jwhu.com/']

    def parse(self, response):
        print("翻页 = :" + response.url)
        print(str(response.css("body::text")))
        item = ImageItem()
        imgurls = []
        for page in response.css('.video-list .guess-item'):
            print(page)
            title = page.css('a span::text').extract_first()
            print(title)
            logo = page.css('.image-wrapper .vod_pic_59484::attr(data-original)').extract_first()
            print(logo)
            data = {"title": title, "url": logo}
            imgurls.append(data)

        item["path"] = "test"
        item['imgurls'] = imgurls
        yield item
        #next_page = "http://soft3.aldeee.com"+response.css(".block-51softList-page a:nth-child(2)::attr(href)").extract_first()
        #print(next_page)
        #yield response.follow(next_page, self.parse)