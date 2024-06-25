# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
import os
import re

import settings
from items import URLSItem, MMDItem

cat_dic = {
    "视频推荐": 11,
    "游戏": 10,
    "百科": 9,
    "萌图": 8,
    "动作数据": 7,
    "场景模型": 6,
    "人物模型": 5,
}


class jwhuspiderPipeline:
    def process_item(self, item, spider):
        return item


class URLSPipeline:
    def process_item(self, item, spider):
        if isinstance(item, URLSItem):
            return item
        elif isinstance(item, MMDItem):
            return item
        else:
            return item


class MMDPipeline:
    def process_item(self, item, spider):
        if isinstance(item, MMDItem):
            print("发布文章:db=", item)
        else:
            return item




class DownloadImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for imgurl in item['imgurls']:
            yield Request(imgurl["url"], meta={'path': item['path'], "imgurl": imgurl})

    def file_path(self, request, response=None, info=None):
        path = request.meta['path']
        imgurl = request.meta["imgurl"]
        imgname = request.url.split('/')[-1]
        extname = request.url.split('.')[-1]
        filename = u'{0}/{1}'.format(path, imgurl["title"] + "." + extname)
        print(filename)
        return filename

    def thumb_path(self, request, thumb_id, response=None, info=None):
        path = request.meta["path"]
        image_name = request.url.split("/")[-1]
        thumbname = u'{0}/{1}/{2}'.format(path, thumb_id, image_name)
        return thumbname
