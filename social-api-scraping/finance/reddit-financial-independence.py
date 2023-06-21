# https://www.geeksforgeeks.org/scraping-reddit-using-python/
import praw
import pandas as pd

# Read-only instance
reddit_read_only = praw.Reddit(client_id="bMtuVXTj4NLoEfERzkxJwA",
                               client_secret="FoQ3w8v8p369Caobzx9nXSVP_wMiHg",
                               user_agent="RMacScraping")

subreddit = reddit_read_only.subreddit("financialindependence")

posts_dict = {
    "Title": [],
    "Post Text": [],
}

for post in subreddit.hot(limit=100):
    posts_dict["Title"].append(post.title)
    posts_dict["Post Text"].append(post.selftext)

top_posts = pd.DataFrame(posts_dict)
top_posts.to_csv("data-files/financial-social-data/Hot-Posts-r-Finance-Independence.csv", index=True)

# TODO remove promoted posts
# TODO change format to JSON?
# TODO change API info to .env variables
# TODO get comments?
# TODO remove duplicates from Matt's blogs

# TODO how to use data? ideas **identify trends **provide new advice from trends **????