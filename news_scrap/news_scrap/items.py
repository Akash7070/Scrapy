# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsScrapItem(scrapy.Item):
    # define the fields for your item here like:
    news_title = scrapy.Field()
    news_link = scrapy.Field()
    paragraph = scrapy.Field()
    button_link = scrapy.Field()
    news_image = scrapy.Field()
    pub_date = scrapy.Field()
    upd_date = scrapy.Field()
    pass
