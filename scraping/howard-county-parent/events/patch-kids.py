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

# urls = [
#     'https://patch.com/maryland/columbia/kids-family',
#     'https://patch.com/maryland/ellicottcity/kids-family'
# ]

# for url in urls:
#     # Run

# Chromedriver
browser = loadBrowser.browser
loadBrowser.get_browser_loaded(
    'https://patch.com/maryland/ellicottcity/kids-family',
    '//img[@class="nav__logo"]', browser
)

# Articles
article_data = []

# Titles
article_title_element_str = '//article//h2/a'
article_titles_element = articleData.get_article_xpath_element(
    article_title_element_str, browser)
article_titles = articleData.get_article_titles(article_titles_element)

# Links
article_titles_href = articleData.get_article_titles_href(
    article_titles_element)

# Dates
article_date_element_str = '//article//h6/time'
article_date_element = articleData.get_article_xpath_element(
    article_date_element_str, browser)
article_dates = [
    articleData.format_dates(x.get_attribute('datetime')) for x in article_date_element]

# File
file_name = "data-files/howard-county-parents-data/patch-kids-ellicott-city.csv"
# file_name = "data-files/howard-county-parents-data/patch-kids-columbia.csv"
header = articleData.header

with open(file_name, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    timeout = loadBrowser.timeout

    for title, date, href in zip(article_titles, article_dates, article_titles_href):
        if articleData.check_date_range(date, 1):
            browser.get(href)
            try:
                WebDriverWait(browser, timeout).until(
                    EC.visibility_of_element_located((
                        By.XPATH,
                        '//img[@class="nav__logo"]'
                    )))
            except TimeoutException:
                print("Timed out waiting for page to load")
                browser.quit()

            article_content_element_str = '//article//p'
            article_content_element = articleData.get_article_xpath_element(
                article_content_element_str, browser)
            article_content = [
                x.text for x in article_content_element if x.text != '']

            article_data = [title, href, date, article_content]
            writer.writerow(article_data)
