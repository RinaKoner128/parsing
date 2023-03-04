import scrapy
from scrapy.http import HtmlResponse
from parser_job.items import ParserJobItem

def pr(sice):
    salary = {'minim': 0, 'maxim': 0, 'val': '', 'sps': ''}
    if sice != 'з/п не указана':
        salary['sps'] = sice[-1]
        for s in sice[:-2]:
            if s == 'от ':
                salary['minim'] = int(sice[sice.index(s) + 1].replace('\xa0', ''))
            if s == ' до ':
                salary['maxim'] = int(sice[sice.index(s) + 1].replace('\xa0', ''))
            if s == ' ':
                salary['val'] = sice[sice.index(s) + 1]
    else:
        salary['val'] = 'з/п не указана'
    return salary


class HhRuSpider(scrapy.Spider):
    name = 'hh_ru'
    allowed_domains = ['hh.ru']
    start_urls = [
        'https://spb.hh.ru/search/vacancy?area=76&search_field=name&search_field=company_name&search_field=description&text=python&no_magic=true&L_save_area=true&items_on_page=20',
        'https://spb.hh.ru/search/vacancy?area=88&search_field=name&search_field=company_name&search_field=description&text=python&no_magic=true&L_save_area=true&items_on_page=20'
    ]

    def parse(self, response:HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        vacancies_links = response.xpath("//a[@class ='serp-item__title']/@href").getall()
        for link in vacancies_links:
            yield response.follow(link, callback=self.parse_vacancy)


    def parse_vacancy(self, response:HtmlResponse):
        vacancy_id = response.url
        vacancy_name = response.css("h1::text").get()
        vacancy_salary = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
        vacancy_url = response.url
        vacancy_min = pr(vacancy_salary)['minim']
        vacancy_max = pr(vacancy_salary)['maxim']
        vacancy_currency = pr(vacancy_salary)['val']
        vacancy_sposob = pr(vacancy_salary)['sps']



        yield ParserJobItem(
            _id = vacancy_id,
            name = vacancy_name,
            url = vacancy_url,
            min_salary = vacancy_min,
            max_salary = vacancy_max,
            currency = vacancy_currency,
            sposob = vacancy_sposob
        )
