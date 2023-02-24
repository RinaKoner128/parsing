from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup as bs
import time
from pprint import pprint

# Подключаем MongoDB и создаем таблицу
client = MongoClient('localhost',27017)
db = client['hh_vac']

# Получаем от пользователя данные
prof = str(input("Профессия, должность или компания: "))
page = int(input("Количество страниц данных: "))
min_s = int(input("Желаемая минимальная зарплата: "))
min_salary = 0
max_salary = 0
currency = 0


url = 'https://hh.ru/search/vacancy'
headers = {
 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.11.2.807 Yowser/2.5 Safari/537.36'
}
params = {
'text': prof,
'page' : page
}

#Метод для преобразования предпологаемой зарплаты в три поля: минимальная и максимальная и валюта.
def pr(sice):
 salary = {'minim': 0, 'maxim': 0, 'val': ''}
 if sice != '':
  sice = str(sice).split(' ')
  salary['val'] = sice[-1]
  for s in sice:
   if s == 'от':
    salary['minim'] = int(sice[sice.index(s) + 1].replace('\u202f', ''))
   if s == 'до':
    salary['maxim'] = int(sice[sice.index(s) + 1].replace('\u202f', ''))
   if s == '–':
    salary['minim'] = int(sice[sice.index(s) - 1].replace('\u202f', ''))
    salary['maxim'] = int(sice[sice.index(s) + 1].replace('\u202f', ''))
 else:
  salary['val'] = 'Не указано'
 return salary

# Проходимся по страницам сайта, собираем данные.
for i in range(params['page']):
    respons = requests.get(url, headers=headers, params={'text': prof, 'page' : str(i)})
    dom = bs(respons.text, 'html.parser')
    #Выбираем часть сайта, которая содержит нужную нам информацию о вакансиях
    res = dom.find('div',{'data-qa':'vacancy-serp__results'})

    for r in res.find_all('div', {'class':'serp-item'}):
        try:
            min_salary = pr(r.find_all('span', {'class': 'bloko-header-section-3'})[0].text)['minim']
            max_salary = pr(r.find_all('span', {'class': 'bloko-header-section-3'})[0].text)['maxim']
            currency = pr(r.find_all('span', {'class': 'bloko-header-section-3'})[0].text)['val']
        except IndexError:
            min_salary = pr('')['minim']
            max_salary = pr('')['maxim']
            currency = pr('')['val']
        # Загружаем по одному вакансии. В качесте id используем ссылку на вакансию, как уникальное значение. Тем самым в базу данных
        # попадают только новые вакансии.
        try:
            db.vacancy.insert_one({
                '_id' : r.find_all('a', {'class':'serp-item__title'})[0]['href'],
                'name' : r.find_all('h3', {'class':'bloko-header-section-3'})[0].text,
                'link' : r.find_all('a', {'class':'serp-item__title'})[0]['href'],
                'minim' : min_salary,
                'maxim': max_salary,
                'currency' : currency,
                'site' : url
            })
        except Exception:
            time.sleep(1)
    time.sleep(3)

# Выводим на экран вакансии с заработной платой больше введённой пользователем суммы
def dict_vac(min_s):
    for doc in db.vacancy.find({"$or":[ {'minim':{'$gte' : min_s}}, {'maxim':{'$gte' : min_s}}]}):
        pprint(doc)

dict_vac(min_s)

