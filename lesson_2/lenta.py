import requests
from lxml import html

url = 'https://lenta.ru/parts/news/'

headers = {
 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.11.2.807 Yowser/2.5 Safari/537.36'
}

respons = requests.get(url, headers=headers)
dom = html.fromstring(respons.text)
news_names = dom.xpath("//li/a[@class='card-full-news _parts-news']")

news_dict = {}
for new in news_names:
 names = new.xpath("./h3/text()")[0]
 times = new.xpath("./div/time/text()")[0]
 try:
  source = new.xpath("./div/span/text()")[0]
 except IndexError:
  source = "image"

 if str(new.xpath("./@href")[0]).count("https://") != 0:
  links = new.xpath("./@href")[0]
 else:
  links = url + new.xpath("./@href")[0]
 news_dict[names] ={
  'source':source,
  'time':times,
  'link':links
 }
print(news_dict)