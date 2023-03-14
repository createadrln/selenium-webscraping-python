from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import csv

import utils.loadBrowser
import utils.articleData

# @TODO - this blog is updated 3 times a week. We are capturing the links that are posted on the homepage, but that will only go back a few weeks instead of months

# Chromedriver
browser = utils.loadBrowser.browser
site_url = 'https://esimoney.com/'
utils.loadBrowser.get_browser_loaded(
    site_url,
    '//h1[@class="site-title"]/a', browser)

# Articles
article_data = []

# Titles
article_xpath = '//section[@class="widget widget_recent_entries"]/div/ul/li/a'
article_titles_element = utils.articleData.get_article_xpath_element(
    article_xpath, browser)
article_titles = utils.articleData.get_article_titles(article_titles_element)
article_titles_href = utils.articleData.get_article_titles_href(
    article_titles_element)

file_name = "data-files/financial-blogs-data/esi-money.csv"
header = utils.articleData.header

with open(file_name, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    timeout = utils.loadBrowser.timeout

    for title, href in zip(article_titles, article_titles_href):
        browser.get(href)
        try:
            WebDriverWait(browser, timeout).until(
                EC.visibility_of_element_located((By.XPATH, '//p[@class="site-title"]')))
        except TimeoutException:
            print("Timed out waiting for page to load")
            browser.quit()

        article_date_xpath = '//time[@class="entry-time"]'
        article_date_element = utils.articleData.get_article_xpath_element(
            article_date_xpath, browser)
        article_date = [
            utils.articleData.format_dates(x.text) for x in article_date_element if utils.articleData.check_date_range(utils.articleData.format_dates(x.text))]

        article_content_xpath = '//div[@class="entry-content"]/p'
        article_content_element = utils.articleData.get_article_xpath_element(
            article_content_xpath, browser)
        article_content = [x.text for x in article_content_element]

        article_data = [title, href, article_date, article_content]
        writer.writerow(article_data)
