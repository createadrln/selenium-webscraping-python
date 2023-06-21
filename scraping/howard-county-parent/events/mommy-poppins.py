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
    'https://mommypoppins.com/events/1500/washington-dc/1667/events/all/age/all/all/all/type/deals/0/near/0/0',
    '//img[@id="logo"]', browser
)

# Articles
article_data = []

# Titles
article_title_element_str = '//div[@class="content-details"]/h2'
article_titles_element = articleData.get_article_xpath_element(
    article_title_element_str, browser)
article_titles = articleData.get_article_titles(article_titles_element)

# Links
article_href_element_str = '//div[@class="list-item event"]/a'
article_href_element = articleData.get_article_xpath_element(
    article_href_element_str, browser)
article_href = articleData.get_article_titles_href(article_href_element)

# Dates
article_date_element_str = '//div[@class="content-date-and-links"]//div[@class="times-label"]'
article_date_element = articleData.get_article_xpath_element(
    article_date_element_str, browser)
article_dates = [x.text for x in article_date_element]

# File
file_name = "data-files/howard-county-parents-data/mommy-poppins.csv"
header = articleData.header

with open(file_name, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    timeout = loadBrowser.timeout

    for title, date, href in zip(article_titles, article_dates, article_href):
        browser.get(href)
        try:
            WebDriverWait(browser, timeout).until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    '//img[@id="logo"]'
                )))
        except TimeoutException:
            print("Timed out waiting for page to load")
            browser.quit()

        article_content_element_str = '//div[@class="event-body-container body"]//p'
        article_content_element = articleData.get_article_xpath_element(
            article_content_element_str, browser)
        article_content = [
            x.text for x in article_content_element if x.text != '']

        article_data = [title, href, date, article_content]
        writer.writerow(article_data)
