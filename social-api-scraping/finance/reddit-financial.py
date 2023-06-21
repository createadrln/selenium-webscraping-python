# https://www.geeksforgeeks.org/scraping-reddit-using-python/
import praw
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Read-only instance
reddit_read_only = praw.Reddit(client_id="bMtuVXTj4NLoEfERzkxJwA",
                               client_secret="FoQ3w8v8p369Caobzx9nXSVP_wMiHg",
                               user_agent="RMacScraping")

subreddit = reddit_read_only.subreddit("Finance")

posts_dict = {
    "Title": [],
    "Post Text": [],
    "Score": [],
    "Url": [],
}

option = webdriver.ChromeOptions()
option.add_argument("--incognito")

browser = webdriver.Chrome(executable_path='./chromedriver',
                           chrome_options=option)

timeout = 20

for post in subreddit.hot(limit=50):
    if "This is your safe place" not in post.selftext:
        posts_dict["Title"].append(post.title)
        posts_dict["Post Text"].append(post.selftext)
        posts_dict["Score"].append(post.score)
        posts_dict["Url"].append(post.url)

        if "ft.com" not in post.url and "reuters.com" not in post.url and "wsj.com" not in post.url and "nytimes.com" not in post.url and "bloomberg.com" not in post.url:
            browser.get(post.url)
            # try:
            #     WebDriverWait(browser, timeout).until(
            #         EC.visibility_of_element_located((By.XPATH, "//div/img")))
            # except TimeoutException:
            #     print("Timed out waiting for page to load")
            #     browser.quit()

            article_content_element = browser.find_elements(
                By.XPATH,
                "//div[@class='entry-content']/p") or browser.find_elements(
                    By.XPATH, "//div[@class='article__content-body']/p"
                ) or browser.find_elements(
                    By.XPATH, "//div[@class='rawHtml-content']/p"
                ) or browser.find_elements(
                    By.XPATH,
                    "//div[@class='caas-body']/p") or browser.find_elements(
                        By.XPATH, "//div[@class='c-entry-content ']/p")

            article_content = [x.text for x in article_content_element]

top_posts = pd.DataFrame(posts_dict)
top_posts.to_csv("data-files/financial-social-data/Hot-Posts-r-Finance.csv", index=True)

# TODO remove promoted posts
# TODO change format to JSON?
# TODO change API info to .env variables
# TODO get comments?
# TODO remove duplicates from Matt's blogs