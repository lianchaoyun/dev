import time
from urllib import parse
from urllib.parse import urlsplit

import scrapy
import re
from scrapy.item import Item, Field
from scrapy.spiders import Rule
from w3lib.html import remove_tags
from bs4 import BeautifulSoup

# scrapy crawl zuowenwang
from tinydb import TinyDB, Query

from spider.items import MMDItem, URLSItem


class MMDSpider(scrapy.Spider):
    name = 'mmd'
    allowed_domains = ['mmd.xiaolindraw.com']
    start_urls = ['http://mmd.xiaolindraw.com/index.html']

    def parse(self, response):
        print("抓取页面=:", response)
        #提取网页中的所有链接
        all_urls = [response.urljoin(url) for url in
                    response.css("a::attr(href)").extract()]  # parse.urljoin(response.url, url)
        if all_urls and len(all_urls) > 0:
            urlsItem = URLSItem(action="URLSItem")
            urlsItem["name"] = self.name
            urlsItem["urls"] = all_urls
            yield urlsItem

        #提取正文内容
        title = response.xpath("//div[@class='article']/div[@class='title']/h1/text()").get()
        cat_name = response.xpath("//div[@class='article']//a[@rel='category tag']/text()").get()
        content = response.xpath("//div[@class='article']//div[@class='article_content']")
        contentstr = content.get()
        for img in content.xpath('//img'):
            imgsrc = img.css("img::attr(src)").get()
            newsrc = response.urljoin(imgsrc)
            contentstr = contentstr.replace(imgsrc, newsrc)

        if cat_name and title and contentstr:
            mmdItem = MMDItem(action="MMDItem")
            mmdItem["url"] = response.url
            mmdItem["cat_name"] = cat_name
            mmdItem["title"] = title
            mmdItem["content"] = SqliteTool.clean_attrs(contentstr)
            yield mmdItem
        else:
            SqliteTool.Mmd.update(status=2).where(SqliteTool.Mmd.url == response.url).where(
                SqliteTool.Mmd.status.in_([0, 3])).execute()

        #time.sleep(1)
        #下一页内容提取
        while True:
            nextMmd = SqliteTool.Mmd.get_or_none(SqliteTool.Mmd.status == 0)
            if nextMmd:
                if urlsplit(nextMmd.url).hostname in self.allowed_domains:
                    a = SqliteTool.Mmd.update(status=3).where(SqliteTool.Mmd.url == nextMmd.url).execute()
                    # print("下一页",nextMmd,nextMmd.url,a)
                    yield scrapy.Request(url=nextMmd.url, callback=self.parse)
                    break
                else:
                    a = SqliteTool.Mmd.update(status=4).where(SqliteTool.Mmd.url == nextMmd.url).execute()
                    print("外部域名，下一个", a, nextMmd.url)
            else:
                print("无下一页")
                break
