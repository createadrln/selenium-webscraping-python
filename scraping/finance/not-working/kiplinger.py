from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import csv

import utils.loadBrowser
import utils.articleData

# Chromedriver
browser = utils.loadBrowser.browser
site_url = 'https://www.kiplinger.com/'
utils.loadBrowser.get_browser_loaded(
    site_url,
    '//a[@class="logo__link"]', browser)

# Articles
article_data = []

# Titles
article_titles_xpath = '//h2[@class="listing__title"]'
article_titles_element = utils.articleData.get_article_xpath_element(
    article_titles_xpath, browser)
article_titles = utils.articleData.get_article_titles(article_titles_element)
article_href_xpath = '//a[@class="listing__link"]'
article_href_element = utils.articleData.get_article_xpath_element(
    article_href_xpath, browser)
article_href = [x.get_attribute('href') for x in article_href_element]

# File
file_name = "data-files/financial-blogs-data/kiplingers.csv"
header = utils.articleData.header

with open(file_name, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    timeout = utils.loadBrowser.timeout
    for title, href in zip(article_titles, article_href):
        browser.get(href)
        try:
            WebDriverWait(browser, timeout).until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    "//a[@class='logo__link']"
                )))
        except TimeoutException:
            print("Timed out waiting for page to load")
            browser.quit()

        # TODO -- fix returns dates like "2 days ago"
        article_date_xpath = '//time[@class="relative-date"]'
        article_date_element = utils.articleData.get_article_xpath_element(
            article_date_xpath, browser)
        # article_date = [
        #     utils.articleData.format_dates(x.text) for x in article_date_element if utils.articleData.check_date_range(utils.articleData.format_dates(x.text))]
        article_date = [
            x.text for x in article_date_element if x.text != ''] 
        
        article_content_xpath = '//div[@class="article__topcontainer"]/p'
        article_content_element = utils.articleData.get_article_xpath_element(
            article_content_xpath, browser)
        article_content = [
            x.text for x in article_content_element if x.text != ''] 

        article_data = [title, href, article_date, article_content]
        writer.writerow(article_data)                       
