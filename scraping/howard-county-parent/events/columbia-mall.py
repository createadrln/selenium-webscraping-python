# https://www.themallincolumbia.com/en/events.html

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
    'https://www.themallincolumbia.com/en/events.html',
    '//div[@class="ggp-featured-event"]//div[@class="card-image"]//img', browser)

# Articles
article_data = []

# Titles
article_titles_element = articleData.get_article_xpath_element(
    '//div[@class="ggp-featured-event"]//h4/a', browser)
article_titles = articleData.get_article_titles(article_titles_element)
article_titles_href = articleData.get_article_titles_href(
    article_titles_element)

# Dates
article_date_element = articleData.get_article_xpath_element(
    '//div[@class="ggp-featured-event"]//p[@class="date"]/span', browser)
article_dates = [x.text for x in article_date_element]

# File
file_name = 'data-files/howard-county-parents-data/columbia-mall.csv'
header = articleData.header

with open(file_name, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    timeout = loadBrowser.timeout

    for title, date, href in zip(article_titles, article_dates, article_titles_href):
        browser.get(href)
        try:
            WebDriverWait(browser, timeout).until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    '//a[@class="brand-logo common-logo"]'
                )))
        except TimeoutException:
            print("Timed out waiting for page to load")
            browser.quit()

        article_content_element = articleData.get_article_xpath_element(
            '//div[@class="card-content"]//p', browser)
        article_content = [
            x.text for x in article_content_element if x.text != '']

        article_data = [title, href, date, article_content]
        writer.writerow(article_data)
