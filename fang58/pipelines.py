# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from fang58.items import Fang58Item, Fang58ItemShou, Fang58ItemZu

class MongoPipeline(object):

    collection_name='scrapy_items'
    item_save = dict()

    def  __init__(self, mongo_uri, mongo_db):
        self.mongo_uri=mongo_uri
        self.mongo_db=mongo_db


    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGODB_URI'),   #提取出了mongodb配置
            mongo_db=crawler.settings.get('MONGODB_DATABASE', 'items')   
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)  #连接数据库
        self.db = self.client[self.mongo_db]



    def close_spider(self,spider):
        self.client.close()

    def process_item(self, item, spider): 
        if isinstance(item, Fang58ItemShou):
            # 求平均值
            item_save = self.item_save.get(item['url_r'], [])

            if item_save:
                # 不满30个，我们继续添加，如果满了30个就计算平均价格
                if len(item_save) >= 29:
                    print(item)
                    # 计算均价

                    item_save.append(item)
                    sum_ = 0
                    for i in item_save:
                        sum_ += int(i['dan_jia'].replace('元/㎡', ''))
                    jun_jia = sum_ / 30
                    print('均价：{}'.format(jun_jia))
                    del self.item_save[item['url_r']]

                else:
                    # 继续添加
                    item_save.append(item)
                    
            else:
                self.item_save[item['url_r']] = [item]

        self.db[self.collection_name].insert_one(dict(item))

        return item