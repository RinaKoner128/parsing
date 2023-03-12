import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


from datetime import date, timedelta

# ИНИЦИАЛИЗАЦИЯ
driver = webdriver.Chrome()
driver.get('https://e.mail.ru/login')
driver.maximize_window()
# print(driver.title)
# assert "No results found." not in driver.page_source


auth_form = driver.find_element(By.ID, 'auth-form')
iframe = auth_form.find_element(By.TAG_NAME, 'iframe')
driver.switch_to.frame(iframe)


username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
username.send_keys("renko.nira@mail.ru", Keys.ENTER)
password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'password')))
driver.implicitly_wait(1)
password.send_keys("b1h2b3y4f", Keys.ENTER)

driver.switch_to.default_content()
driver.implicitly_wait(10)

# ОСНОВНОЙ ЦИКЛ - ОБРАБОТКА ПОЧТЫ
letters_container = driver.find_element(By.CSS_SELECTOR, "div.dataset-letters")

letter_urls = set()
last_len = 0
#получение всех ссылок
while True:
    letters = letters_container.find_elements(By.CSS_SELECTOR,'a.llc_normal')
    letter_urls.update(letter.get_attribute("href") for letter in letters)
    if last_len == len(letter_urls):
        break

    last_len = len(letter_urls)

    actions = ActionChains(driver)
    actions.move_to_element(letters[-1])
    actions.perform()
    time.sleep(1)

result_items = []

for letter_url in letter_urls:
    item ={}
    driver.get(letter_url)
    item["url"] = letter_url
    item["title"] = driver.find_element(By.XPATH, "//h2").text
    container = driver.find_element(By.XPATH, "//div[contains(@class, 'thread__letter')][1]")


    item["from"] = container.find_element(By.XPATH, ".//div[contains(@class, 'letter__author')]//span[contains(@class, 'letter-contact')]").get_attribute('title')
    item["date"] = container.find_element(By.XPATH, ".//div[contains(@class, 'letter__author')]//div[contains(@class, 'letter__date')]").text
    if 'сегодня' in item["date"]:
        item["date"] = item["date"].replace("сегодня", date.today())
    if 'вчера' in item["date"]:
        item["date"] = item["date"].replace("вчера", date.today() - timedelta(days=1))

    result_items.append(item)

driver.close()

# СЛОЖИТЬ ВСЮ ПОЧТУ В БД
from pymongo import MongoClient
client = MongoClient('127.0.0.1', 27017)
db = client['mails_db']
mails_db = db.mails

for item in result_items:
    mails_db.update_one({'link': item['url']}, {'$set': item}, upsert=True)