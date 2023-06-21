from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime

import csv

from utils import (
    loadBrowser,
    articleData
)

# Chromedriver
browser = loadBrowser.browser
loadBrowser.get_browser_loaded(
    'https://www.howardcountymd.gov/events?f%5B0%5D=department%3A2898',
    '//a[@class="block--branding__logo"]/img', browser)

# Articles
article_data = []

# Titles
article_titles_element = articleData.get_article_xpath_element(
    '//div[@class="node--event--upcoming__title"]', browser)
article_titles = articleData.get_article_titles(article_titles_element)

# Url
article_href_element = articleData.get_article_xpath_element(
    '//a[@class="node--event--upcoming__container"]', browser)
article_href = articleData.get_article_titles_href(
    article_href_element)

# Dates
article_dates = []
article_date_element = articleData.get_article_xpath_element(
    '//div[@class="node--event--upcoming__date"]', browser)
for date in article_date_element:
    formatted_date = articleData.format_dates(date.text)
    article_dates.append(formatted_date)

# File
file_name = "data-files/howard-county-parents-data/robinson-nature-center.csv"
header = articleData.header

with open(file_name, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    timeout = loadBrowser.timeout

    for title, date, href in zip(article_titles, article_dates, article_href):
        if datetime.strptime(date, '%Y-%m-%d') > datetime.today():
            loadBrowser.get_browser_loaded(
                href, '//a[@class="block--branding__logo"]/img', browser)

            article_content_element = articleData.get_article_xpath_element(
                '//div[contains(@class, "field--name-field-content")]', browser)
            article_content = [
                x.text for x in article_content_element if x.text != '']

        article_data = [title, href, date, article_content]
        writer.writerow(article_data)
