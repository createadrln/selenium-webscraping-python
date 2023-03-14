from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import csv

import utils.loadBrowser
import utils.articleData
import utils.cleantext

# Chromedriver
browser = utils.loadBrowser.browser
site_url = 'https://www.sidehustlenation.com/blog/'
utils.loadBrowser.get_browser_loaded(
    site_url,
    '//div[@class="site-logo"]/a/img', browser)

# Articles
article_data = []

# Titles
article_titles_xpath = '//h2[@class="entry-title"]/a'
article_titles_element = utils.articleData.get_article_xpath_element(
    article_titles_xpath, browser)
article_titles = utils.articleData.get_article_titles(article_titles_element)
article_titles_href = utils.articleData.get_article_titles_href(
    article_titles_element)

# Dates
article_dates = []
article_dates_xpath = '//time[@class="entry-date published"]'
article_dates_element = utils.articleData.get_article_xpath_element(
    article_dates_xpath, browser)
for x in article_dates_element:
    date = utils.cleantext.clean_date_text(x.text)
    formatted_date = utils.articleData.format_dates(date)
    article_dates.append(formatted_date)

# File
file_name = "data-files/financial-blogs-data/side-hustle-nation.csv"
header = utils.articleData.header

with open(file_name, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    timeout = utils.loadBrowser.timeout
    for title, date, href in zip(article_titles, article_dates, article_titles_href):
        if utils.articleData.check_date_range(date):
            browser.get(href)
            try:
                WebDriverWait(browser, timeout).until(
                    EC.visibility_of_element_located((
                        By.XPATH,
                        "//div[@class='site-logo']/a/img"
                    )))
            except TimeoutException:
                print("Timed out waiting for page to load")
                browser.quit()

            article_content_xpath = '//div[@class="entry-content"]/p'
            article_content_element = utils.articleData.get_article_xpath_element(
                article_content_xpath, browser)
            article_content = [
                x.text for x in article_content_element if x.text != '']

            article_data = [title, href, date, article_content]
            writer.writerow(article_data)
