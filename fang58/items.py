# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Fang58Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title=scrapy.Field()
    price=scrapy.Field()
    di_zhi=scrapy.Field()
    nian_dai=scrapy.Field()

class Fang58ItemZu(scrapy.Item):
    url=scrapy.Field()
    title=scrapy.Field()
    price=scrapy.Field()

class Fang58ItemShou(scrapy.Item):
    url=scrapy.Field()
    title=scrapy.Field()
    zong_jia=scrapy.Field()
    dan_jia=scrapy.Field()
    mian_ji=scrapy.Field()
    url_r=scrapy.Field()


