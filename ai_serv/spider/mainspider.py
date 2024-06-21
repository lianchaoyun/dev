from scrapy.cmdline import execute

# 本程序为爬虫起始入口，直接运行本程序即可运行爬虫
# execute(['scrapy', 'crawl', 'mmd'])
execute(['scrapy', 'crawl', 'mmd', '--nolog'])
