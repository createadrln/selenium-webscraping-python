from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import csv

option = webdriver.ChromeOptions()
option.add_argument("--incognito")

browser = webdriver.Chrome(executable_path='./chromedriver',
                           chrome_options=option)

browser.get("https://www.choosefi.com/read/blog/")

timeout = 20
try:
    WebDriverWait(browser, timeout).until(
        EC.visibility_of_element_located((
            By.XPATH,
            "//img[@title='PNGs_ChooseFI_PrimaryLogo-Mono-WhiteSmallHeader.png']"
        )))
except TimeoutException:
    print("Timed out waiting for page to load")
    browser.quit()

article_data = []

article_titles_element = browser.find_elements(
    By.XPATH, "//h3[@class='elementor-post__title']/a")
article_titles = [x.text for x in article_titles_element]
article_titles_href = [x.get_attribute('href') for x in article_titles_element]

article_dates_element = browser.find_elements(
    By.XPATH, "//span[@class='elementor-post-date']")
article_dates = [x.text for x in article_dates_element]

file_name = "data-files/financial-blogs-data/choose-fi.csv"

header = ['title', 'url', 'date', 'publication', 'content']

with open(file_name, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    
    for title, date, href in zip(article_titles, article_dates,
                                article_titles_href):
        browser.get(href)
        try:
            WebDriverWait(browser, timeout).until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    "//img[@title='PNGs_ChooseFI_PrimaryLogo-Mono-WhiteSmallHeader.png']"
                )))
        except TimeoutException:
            print("Timed out waiting for page to load")
            browser.quit()

        article_content_element = browser.find_elements(
            By.XPATH, "//div[@class='elementor-widget-container']/p")
        article_content = [x.text for x in article_content_element]

        article_data = [title, href, date, 'Choose Fi', article_content]
        writer.writerow(article_data)
