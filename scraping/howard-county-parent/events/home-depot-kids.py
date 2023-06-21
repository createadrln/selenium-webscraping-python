# https://www.homedepot.com/c/kids

import csv

from utils import (
    loadBrowser,
    articleData
)

# Chromedriver
browser = loadBrowser.browser
loadBrowser.get_browser_loaded(
    'https://www.homedepot.com/c/kids',
    '//svg[@class="HeaderLogo"]', browser
)

# Articles
article_data = []

# Titles
article_title_element_str = '//div[@class="grid-center"]//p[@class="visualNav__title-center"]'
article_titles_element = articleData.get_article_xpath_element(
    article_title_element_str, browser)
article_titles = articleData.get_article_titles(article_titles_element)

# File
file_name = "data-files/howard-county-parents-data/home-depot-kids-events.csv"
header = articleData.header

with open(file_name, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)

    for title in zip(article_titles):
        article_data = [title]
        writer.writerow(article_data)
