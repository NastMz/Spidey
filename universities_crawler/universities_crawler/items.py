# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UniversitiesCrawlerItem(scrapy.Item):
    university = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    country = scrapy.Field()
