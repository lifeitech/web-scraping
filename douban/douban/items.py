# -*- coding: utf-8 -*-

import scrapy

class DoubanItem(scrapy.Item):
    rank = scrapy.Field()
    title = scrapy.Field()