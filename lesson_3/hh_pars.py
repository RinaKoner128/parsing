import requests
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

#Метод для преобразования предпологаемой зарплаты в три поля: минимальная и максимальная и валюта.
def pr(sice):
 salary = {'minim': 0, 'maxim': 0, 'val': ''}
 if sice != '':
  sice = str(sice).split(' ')
  for s in sice:
   if s == 'от':
    salary['minim'] = int(sice[sice.index(s) + 1].replace('\u202f', ''))
   if s == 'до':
    salary['maxim'] = int(sice[sice.index(s) + 1].replace('\u202f', ''))
   if s == '–':
    salary['minim'] = int(sice[sice.index(s) - 1].replace('\u202f', ''))
    salary['maxim'] = int(sice[sice.index(s) + 1].replace('\u202f', ''))
  salary['val'] = sice[-1]
 else:
  salary['val'] = 'Не указано'
 return salary

#Запрашиваем данные для парсинга
prof = str(input("Профессия, должность или компания: "))
page = int(input("Количество страниц данных: "))

names = []
min_salary = []
max_salary = []
currency = []
links = []
sites = []
url = 'https://hh.ru/search/vacancy'

headers = {
 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.11.2.807 Yowser/2.5 Safari/537.36'
}
params = {
'text': prof,
'page' : page
}

# Проходимся по страницам сайта, собираем данные.
for i in range(params['page']):
 respons = requests.get(url, headers=headers, params={'text': prof, 'page' : str(i)})
 dom = bs(respons.text, 'html.parser')
 #Выбираем часть сайта, которая содержит нужную нам информацию о вакансиях
 res = dom.find('div',{'data-qa':'vacancy-serp__results'})

 for r in res.find_all('div', {'class':'serp-item'}):
  names.append(r.find_all('h3', {'class':'bloko-header-section-3'})[0].text) #Собираем список наименований вакансий
  links.append(r.find_all('a', {'class':'serp-item__title'})[0]['href'])#Собираем список ссылок на вакансии
  sites.append(url) #Указываем на каком сайте нашли вакансии
  # Собираем список предпологаемых зарплат и разносим их по 3 столбцам
  try:
   min_salary.append(pr(r.find_all('span', {'class':'bloko-header-section-3'})[0].text)['minim'])
   max_salary.append(pr(r.find_all('span', {'class':'bloko-header-section-3'})[0].text)['maxim'])
   currency.append(pr(r.find_all('span', {'class':'bloko-header-section-3'})[0].text)['val'])
  except IndexError:
   min_salary.append(pr('')['minim'])
   max_salary.append(pr('')['maxim'])
   currency.append(pr('')['val'])
 time.sleep(3)

# Формируем DataFrame с данными и записываем их в csv файл
df = pd.DataFrame(list(zip(names, links, min_salary, max_salary, currency, sites)),
                    columns=['names', 'links', 'min_salary', 'max_salary', 'currency', 'site'])
df.to_csv('hh.csv', index=False, encoding='utf-8')




