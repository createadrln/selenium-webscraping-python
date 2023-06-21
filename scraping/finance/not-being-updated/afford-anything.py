from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import csv

url = "https://affordanything.com/blog/"
file_name = "data-files/financial-blogs-data/Afford-Anything.csv"
source = "Afford Anything"
header = ['title', 'url', 'date', 'publication', 'content']
site_loaded_xpath = "//p[@class='site-title']"
title_xpath = "//h2[@class='entry-title']/a"

def scrape_page(url, file_name, source, header, site_loaded_xpath, title_xpath):
    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")

    browser = webdriver.Chrome(
        executable_path='./chromedriver', chrome_options=option)
    browser.get(url)

    timeout = 20
    try:
        WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located(
                (By.XPATH, site_loaded_xpath)))
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()

    article_data = []
    article_titles_element = browser.find_elements(
        By.XPATH, title_xpath)
    article_titles = [x.text for x in article_titles_element]
    article_titles_href = [x.get_attribute(
        'href') for x in article_titles_element]
    article_dates_element = browser.find_elements(
        By.XPATH, "//time[@class='entry-time']")
    article_dates = [x.text for x in article_dates_element]

    with open(file_name, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        for title, date, href in zip(article_titles, article_dates, article_titles_href):
            browser.get(href)
            try:
                WebDriverWait(browser, timeout).until(
                    EC.visibility_of_element_located((By.XPATH, "//p[@class='site-title']")))
            except TimeoutException:
                print("Timed out waiting for page to load")
                browser.quit()

            article_content_element = browser.find_elements(
                By.XPATH, "//div[@class='entry-content']/p")
            article_content = [x.text for x in article_content_element]
            article_data = [
                title,
                href,
                date,
                source,
                article_content
            ]
            writer.writerow(article_data)


scrape_page(url, file_name, source, header, site_loaded_xpath, title_xpath)
