import scrapy


class FirstSpi(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    img = scrapy.Field()
