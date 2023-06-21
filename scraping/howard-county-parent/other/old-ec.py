from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime

import csv

import utils.loadBrowser
import utils.articleData

# Chromedriver
browser = utils.loadBrowser.browser
utils.loadBrowser.get_browser_loaded(
    'https://visitoldellicottcity.com/events/',
    '//div[contains(@class, "elementor-location-header")]//div[@class="elementor-image"]//img', browser)

# Articles
article_data = []

# Titles
article_titles_element = utils.articleData.get_article_xpath_element(
    '//h4[@class="mec-event-title"]', browser)
article_titles = utils.articleData.get_article_titles(article_titles_element)

# Url
article_href_element = utils.articleData.get_article_xpath_element(
    '//h4[@class="mec-event-title"]/a', browser)
article_href = utils.articleData.get_article_titles_href(
    article_href_element)

# Dates
article_dates = []
article_date_element = utils.articleData.get_article_xpath_element(
    '//span[@class="mec-start-date-label"]', browser)
for date in article_date_element:
    formatted_date = utils.articleData.format_dates(date.text)
    article_dates.append(formatted_date)

# File
file_name = "data-files/howard-county-parents-data/old-ellicott-city.csv"
header = utils.articleData.header

exclude = [
    'beer',
    # 'axgard',
    # 'pub crawl'
]

with open(file_name, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    timeout = utils.loadBrowser.timeout

    load_more_button_element = browser.find_element_by_xpath(
        '//div[@class="mec-load-more-button"]')

    load_more_button_element.click()
    load_more_button_element.click()
    load_more_button_element.click()
    load_more_button_element.click()
    load_more_button_element.click()

    for title, date, href in zip(article_titles, article_dates, article_href):
        browser.get(href)
        try:
            WebDriverWait(browser, timeout).until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    '//div[contains(@class, "elementor-location-header")]//div[@class="elementor-image"]//img'
                )))
        except TimeoutException:
            print("Timed out waiting for page to load")
            browser.quit()

        article_content_element = utils.articleData.get_article_xpath_element(
            '//div[contains(@class, "mec-single-event-description")]/p', browser)
        article_content = [
            x.text for x in article_content_element if x.text != '']

        article_data = [title, href, date, article_content]
        writer.writerow(article_data)
