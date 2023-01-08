from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import json

option = webdriver.ChromeOptions()
option.add_argument("--incognito")

browser = webdriver.Chrome(executable_path='./chromedriver',
                           chrome_options=option)

browser.get("https://www.sidehustlenation.com/blog/")

timeout = 20
try:
    WebDriverWait(browser, timeout).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[@class='site-logo']/a/img")))
except TimeoutException:
    print("Timed out waiting for page to load")
    browser.quit()

article_data = []

article_titles_element = browser.find_elements(
    By.XPATH, "//h2[@class='entry-title']/a")
article_titles = [x.text for x in article_titles_element]
article_titles_href = [x.get_attribute('href') for x in article_titles_element]

article_dates_element = browser.find_elements(
    By.XPATH, "//time[@class='entry-date published']")
article_dates = [x.text for x in article_dates_element]

file_name = "data-files/Side-Hustle-Nation.json"
file = open(file_name, 'wb')

# Pair each title with its corresponding language using zip function and print each pair
for title, date, href in zip(article_titles, article_dates,
                             article_titles_href):
    browser.get(href)
    try:
        WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@class='site-logo']/a/img")))
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()

    article_content_element = browser.find_elements(
        By.XPATH, "//div[@class='entry-content']/p")
    article_content = [x.text for x in article_content_element]

    article_data.append({
        'title': title,
        'url': href,
        'date': date,
        'content': article_content
    })

json_string = json.dumps(article_data)
file.write(json_string.encode())
file.close()

