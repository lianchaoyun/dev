import scrapy

from spider.items import ExampleItem
from scrapy_splash import SplashRequest

class ExampleSpider(scrapy.Spider):
    name = "example"
    #allowed_domains = ['itcast.com']
    start_urls = [
        "https://www.pinterest.com/pin/228487381086622331/",
    ]
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, args={'wait': 10})
    def parse(self, response):
        context = response.xpath('/html/head/title/text()')
        print(response.xpath("body"))
        title = context.extract_first()
        print(title)
        image_urls = response.xpath('//img')
        for image_url in image_urls:
            print(image_url)
            imgsrc = image_url.css("img::attr(src)").get()  #originals

            print(imgsrc)
            #yield scrapy.Request(image_url, callback=self.save_image)

        for quote in response.css("div.quote"):
            yield {
                "author": quote.xpath("span/small/text()").get(),
                "text": quote.css("span.text::text").get(),
            }
        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)