from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep
import json

option = webdriver.ChromeOptions()
option.add_argument("--incognito")

browser = webdriver.Chrome(executable_path='./chromedriver',
                           chrome_options=option)

browser.get("https://www.financialsamurai.com/")

timeout = 20
try:
    WebDriverWait(browser, timeout).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//h1[@class='site-title']")))
except TimeoutException:
    print("Timed out waiting for page to load")
    browser.quit()

article_data = []

article_titles_element = browser.find_elements(
    By.XPATH,
    "//section[@class='widget featured-content featuredpost']/div/article/header/h2/a"
)
article_titles = [x.text for x in article_titles_element]
article_titles_href = [x.get_attribute('href') for x in article_titles_element]

file_name = "data-files/Financial-Samurai.json"
file = open(file_name, 'wb')

# Pair each title with its corresponding language using zip function and print each pair
for title, href in zip(article_titles, article_titles_href):
    sleep(9)
    browser.get(href)
    try:
        WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//p[@class='site-title']")))
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()

    article_content_element = browser.find_elements(
        By.XPATH, "//div[@class='entry-content']/p")
    article_content = [x.text for x in article_content_element]

    article_date_element = browser.find_elements(
        By.XPATH, "//time[@class='entry-time']")
    article_date = [x.text for x in article_date_element]

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
