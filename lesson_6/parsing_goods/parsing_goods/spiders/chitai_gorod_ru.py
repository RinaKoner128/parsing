import scrapy
from scrapy.http import HtmlResponse
from parsing_goods.items import ParsingGoodsItem
from scrapy.loader import ItemLoader

class ChitaiGorodRuSpider(scrapy.Spider):
    name = "chitai-gorod_ru"
    allowed_domains = ["chitai-gorod.ru"]

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.start_urls = ["https://www.chitai-gorod.ru/catalog/kanctovars/penaly-3713"]

    def parse(self, response:HtmlResponse):
        page_links = response.xpath("//article//a/@href").getall()
        for link in page_links:
            yield response.follow(link, callback=self.parse_goods)

    def parse_goods(self, response:HtmlResponse):
        loader = ItemLoader(item=ParsingGoodsItem(), response=response)

        # loader.add_xpath('name', "//span[@class='product-detail-offer-header__price-currency']/text()")
        loader.add_xpath('name', "/html/head/title/text()")
        loader.add_value('url', response.url)
        loader.add_value('_id', response.url)
        loader.add_xpath('price', "//span[@class='product-detail-offer-header__price-currency']/text()")
        loader.add_xpath('photos', "//img[@class='product-gallery__image']/@src")
        yield loader.load_item()














