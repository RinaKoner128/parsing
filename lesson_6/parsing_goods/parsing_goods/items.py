# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Compose, TakeFirst


def clean_price(value):
    try:
        for v in value:
            value[value.index(v)] = v.replace('\xa0', '').replace('\n', '')
    except:
        return value
    return value


class ParsingGoodsItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=Compose(clean_price), output_processor=TakeFirst())
    photos = scrapy.Field()
    _id = scrapy.Field(output_processor=TakeFirst())

    pass
