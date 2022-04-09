from scrapy import cmdline

spider = 'bocconi_spider'
cmdline.execute(["scrapy", "crawl", spider])