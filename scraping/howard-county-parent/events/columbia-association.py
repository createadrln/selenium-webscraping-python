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
    'https://columbiaassociation.org/explore-columbia/event-calendar/',
    '//img[@class=" preload-me"]', browser
)

# def get_furthest_date():
#     # Get the furthest date from the data and click next button

# Articles
article_data = []

# Titles
article_title_element_str = '//article//h3/a'
article_titles_element = articleData.get_article_xpath_element(
    article_title_element_str, browser)
article_titles = articleData.get_article_titles(article_titles_element)

# Links
article_titles_href = articleData.get_article_titles_href(
    article_titles_element)

# Dates
article_date_element_str = '//article//time/span[@class="tribe-event-date-start"]'
article_date_element = articleData.get_article_xpath_element(
    article_date_element_str, browser)
article_dates = [x.text for x in article_date_element]

# File
file_name = "data-files/howard-county-parents-data/columbia-association.csv"
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
                    '//img[@class=" preload-me"]'
                )))
        except TimeoutException:
            print("Timed out waiting for page to load")
            browser.quit()

        article_content_element_str = '//div[@class="wprt-container"]/p'
        article_content_element = articleData.get_article_xpath_element(
            article_content_element_str, browser)
        article_content = [
            x.text for x in article_content_element if x.text != '']

        article_data = [title, href, date, article_content]
        writer.writerow(article_data)
