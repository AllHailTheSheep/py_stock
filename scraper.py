from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.add_argument('--allow-running-insecure-content')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)


def get_price(stock):
    URL = 'https://www.nasdaq.com/market-activity/stocks/' + stock + '/real-time'
    driver.get(URL)
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content, "html.parser")
    last_price = soup.find(class_='symbol-page-header__pricing-price')
    final = last_price.text
    return final.strip('$')
