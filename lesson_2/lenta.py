import requests
from lxml import html
from pprint import pprint

url = 'https://lenta.ru/parts/news/'

headers = {
 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.11.2.807 Yowser/2.5 Safari/537.36'
}


respons = requests.get(url, headers=headers)
dom = html.fromstring(respons.text)
# Выделяем общий блок, в котором нужная нам информация
news_names = dom.xpath("//li/a[@class='card-full-news _parts-news']")

def create_dict_news():
 news_dict = {}
 for new in news_names:
  names = new.xpath("./h3/text()")[0] #Получаем наименование новости
  times = new.xpath("./div/time/text()")[0]#Получаем дату публикации
  # Ряд источников - ссылка-изображение без наименования, обозначим такие источники как "image"
  try:
   source = new.xpath("./div/span/text()")[0]#Получаем название источника
  except IndexError:
   source = "image"

  # Отсортировываем внешние ссылки. Для внутренних ссылок lenta.ru дописываем их.
  if str(new.xpath("./@href")[0]).count("https://") != 0:
   links = new.xpath("./@href")[0]
  else:
   links = url + new.xpath("./@href")[0]
  # Формируем словарь с данными
  news_dict[names] ={
   'source':source,
   'time':times,
   'link':links
  }
 return news_dict

#Выводим словарь
pprint(create_dict_news())