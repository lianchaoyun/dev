# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
import os  # 用于路径拼接、判断是否存在等
import re

from hub.db.mysql import MysqlWordpress
from hub.db.sqlite import SqliteTool
from jwhuspider import settings
from jwhuspider.items import URLSItem, MMDItem

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
            for url in item["urls"]:
                mmd = SqliteTool.Mmd.get_or_none(SqliteTool.Mmd.url == url)
                if mmd is None:
                    a = SqliteTool.Mmd.create(url=url, status=0)
                    print("新地址 [" + url + "] 入库.id=" + str(a))
        elif isinstance(item, MMDItem):
            mmd = SqliteTool.Mmd.get_or_none(SqliteTool.Mmd.url == item["url"])
            if mmd is None:
                a = SqliteTool.Mmd.create(url=item["url"], status=0)
                print("新地址 [" + item["url"] + "] 入库.id=" + str(a))
            return item
        else:
            return item


class MMDPipeline:
    def process_item(self, item, spider):
        if isinstance(item, MMDItem):
            mmd = SqliteTool.Mmd.get_or_none(SqliteTool.Mmd.url == item["url"])
            if mmd is None:
                return item
            rs = self.post_content(item)
            ua = SqliteTool.Mmd.update(status=1, status_db=rs).where(SqliteTool.Mmd.url == item["url"]).where(
                SqliteTool.Mmd.status.in_([0, 3])).execute()
            print("发布文章:db=", rs, "  cache=", ua)
        else:
            return item

    def post_content(self, item):
        term_taxonomy_id = cat_dic.get(item["cat_name"])
        if term_taxonomy_id is None:
            return 3  # 其他错误
        else:
            if MysqlWordpress.original_address_is_exist(item["url"]):
                return 4
            rs = MysqlWordpress.create(term_taxonomy_id=term_taxonomy_id, post_author=1, post_content=item['content'],
                                       post_title=item['title'], original_address=item["url"])
            if rs:
                return 1  # 发布成功
            else:
                return 2  # 发布失败


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
