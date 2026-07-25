import scrapy

class GeoLeadItem(scrapy.Item):
    name = scrapy.Field()
    phone = scrapy.Field()
    address = scrapy.Field()
    city = scrapy.Field()
    district = scrapy.Field()
    industry = scrapy.Field()
    source = scrapy.Field()
    source_id = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    rating = scrapy.Field()
    tags = scrapy.Field()