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

browser.get("https://www.kiplinger.com/")

timeout = 20
try:
    WebDriverWait(browser, timeout).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//a[@class='logo__link']")))
except TimeoutException:
    print("Timed out waiting for page to load")
    browser.quit()

article_data = []

article_titles_element = browser.find_elements(
    By.XPATH, "//h2[@class='listing__title']")
article_titles = [x.text for x in article_titles_element]

article_href_element = browser.find_elements(By.XPATH,
                                             "//a[@class='listing__link']")
article_href = [x.get_attribute('href') for x in article_href_element]

file_name = "data-files/Kiplinger.json"
file = open(file_name, 'wb')

# Pair each title with its corresponding language using zip function and print each pair
for title, href in zip(article_titles, article_href):
    browser.get(href)
    try:
        WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//a[@class='logo__link']")))
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()

    article_content_element = browser.find_elements(
        By.XPATH, "//div[@class='article__topcontainer']/p")
    article_content = [x.text for x in article_content_element]

    article_date_element = browser.find_elements(
        By.XPATH, "//time[@class='relative-date']")
    article_date = [x.get_attribute("datetime") for x in article_date_element]

    article_data.append({
        'title': title,
        'url': href,
        'date': article_date,
        'content': article_content
    })

json_string = json.dumps(article_data)
file.write(json_string.encode())
file.close()

# TODO - find other sources we want to use
# TODO - pull from Twitter
# TODO - find some common stuff in the content
# TODO - use near operators to find keywords
# TODO - identify common keywords (wordcloud?)
# TODO - weight by recency
