# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BocconiItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    title = scrapy.Field()
    email = scrapy.Field()
    bio_note = scrapy.Field()
    academic_cv = scrapy.Field()
    research_area = scrapy.Field()
    course = scrapy.Field()
    pubs = scrapy.Field()
    personal_page = scrapy.Field()