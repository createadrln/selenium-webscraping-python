import praw
import pandas as pd

from selenium import webdriver

# Read-only instance
reddit_read_only = praw.Reddit(
    client_id="bMtuVXTj4NLoEfERzkxJwA",
    client_secret="FoQ3w8v8p369Caobzx9nXSVP_wMiHg",
    user_agent="RMacScraping")

# subreddit = reddit_read_only.subreddit("Maryland")
subreddit = reddit_read_only.subreddit("EllicottCity")

posts_dict = {
    "Title": [],
    # "Author": [],
    # "Post Text": [],
    # "Score": [],
    "Url": [],
}

option = webdriver.ChromeOptions()
option.add_argument("--incognito")

browser = webdriver.Chrome(
    executable_path="./chromedriver",
    chrome_options=option)

timeout = 20

matches = [
    # "best",
    # "kids",
    # "children",
    # "toddlers",
    # "young",
    # "infants",
    # "events",
    # "family",
    # "to do",
    # "activites",
    "event"
]

for post in subreddit.top(time_filter="all", limit=5000):
    if post.author != "AutoModerator" \
            and any([x in post.title.lower() for x in matches]):
        posts_dict["Title"].append(post.title)

        # posts_dict["Author"].append(post.author)
        # posts_dict["Post Text"].append(post.selftext)
        # posts_dict["Score"].append(post.score)
        posts_dict["Url"].append(post.url)

top_posts = pd.DataFrame(posts_dict)
top_posts.to_csv(
    "data-files/howard-county-parents-data/Hot-Posts-r-Maryland.csv", index=True)
