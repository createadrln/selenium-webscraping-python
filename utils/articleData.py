from selenium.webdriver.common.by import By
from dateutil import parser
from datetime import datetime
from dateutil.relativedelta import relativedelta

header = ['title', 'url', 'date', 'content']

def get_article_xpath_element(xpath, browser):
    return browser.find_elements(By.XPATH, xpath)


def get_article_titles(article_titles_element):
    return [x.text for x in article_titles_element]


def get_article_titles_href(article_titles_element):
    return [x.get_attribute('href') for x in article_titles_element]


def format_dates(date_text):
    d = parser.parse(date_text)
    return d.strftime('%Y-%m-%d')

def check_date_range(article_date, allowed_date_range = 6):
    current_date = datetime.today()
    article_date = datetime.strptime(article_date, '%Y-%m-%d')
    return current_date - relativedelta(months=allowed_date_range) < article_date
