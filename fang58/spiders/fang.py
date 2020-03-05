# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery
from fang58.items import Fang58Item, Fang58ItemShou, Fang58ItemZu


class FangSpider(scrapy.Spider):
    name = 'fang'
    allowed_domains = ['58.com']
    start_urls = ['https://cd.58.com/xiaoqu/']

    def parse(self, response):
        jpy = PyQuery(response.text)
        li_s = jpy('body > div.main-wrap > div.content-wrap > div.content-side-left > ul > li')

        for li in li_s.items():
            url = li('div.list-info > h2 > a').attr('href')
            self.logger.info(url)
            yield scrapy.Request(url=url, callback=self.fang_detail)

    def fang_detail(self, response):
        jpy = PyQuery(response.text)

        zai_shou_url = jpy('body > div.body-wrapper > div.basic-container > div.info-container > div.info-tb-container > table > tr.tb-btm > td:nth-child(2) > a').attr('href')
        zai_zu_url = jpy('body > div.body-wrapper > div.basic-container > div.info-container > div.info-tb-container > table > tr.tb-btm > td:nth-child(4) > a').attr('href')

        self.logger.info("{}, {}".format(zai_shou_url, zai_zu_url))
        
        yield scrapy.Request(url="https:{}".format(zai_shou_url), callback=self.shou_list)
        yield scrapy.Request(url="https:{}".format(zai_zu_url), callback=self.zu_list)

        i = Fang58Item()
        i['title'] = jpy('body > div.body-wrapper > div.title-bar > span.title').text()
        i['price'] = jpy('body > div.body-wrapper > div.basic-container > div.info-container > div.price-container > span.price').text()
        i['di_zhi'] = jpy('body > div.body-wrapper > div.basic-container > div.info-container > div.info-tb-container > table > tr:nth-child(1) > td:nth-child(4)').text()
        i['nian_dai'] = jpy('body > div.body-wrapper > div.basic-container > div.info-container > div.info-tb-container > table > tr:nth-child(4) > td:nth-child(2)').text()
        yield i

    def shou_list(self, response):
    #二手房列表页
        jpy = PyQuery(response.text)
        # 获取tr列表
        tr_s = jpy('#infolist > div.listwrap > table > tr')

        for tr in tr_s.items():
            i = Fang58ItemShou()
            i['title'] = tr('td.t > a.t').text()
            i['url'] =  tr('td.t > a.t').attr('href')
            i['dan_jia'] = tr('td.tc > span:nth-child(3)').text()
            i['zong_jia'] = tr('td.tc > b').text()
            i['mian_ji'] = tr('td.tc > span:nth-child(5)').text()
            i['url_r'] = response.url
            yield i


    def zu_list(self, response):
        # 租房列表页
        self.logger.info("zu: {}".format(response))
        jpy=PyQuery(response.text)

        # 获取tr列表
        tr_s = jpy('#infolist > div.listwrap > table > tr')
        
        for tr in tr_s.items():
            i = Fang58ItemZu()
            i['title'] = tr("td.t > a.t").text()
            i['price'] = tr('td.tc > b').text()
            i['url'] = tr('td.t > a.t').attr('href')
            yield i
            

        

