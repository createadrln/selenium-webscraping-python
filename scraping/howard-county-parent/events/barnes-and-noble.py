import csv

from utils import (
    loadBrowser,
    articleData
)

# Chromedriver
browser = loadBrowser.browser
loadBrowser.get_browser_loaded(
    'https://stores.barnesandnoble.com/store/2831',
    '//a[@class="logo-img "]', browser
)

# Articles
article_data = []

# Titles
article_title_element_str = '//a[contains(@class, "eventTitle")]'
article_titles_element = articleData.get_article_xpath_element(
    article_title_element_str, browser)
article_titles = articleData.get_article_titles(article_titles_element)

# Links
article_titles_href = articleData.get_article_titles_href(
    article_titles_element)

# Dates
article_date_element_str = '//div[@class="eventDate"]'
article_date_element = articleData.get_article_xpath_element(
    article_date_element_str, browser)
article_dates = [x.text for x in article_date_element]

# File
file_name = "data-files/howard-county-parents-data/barnes-and-noble.csv"
header = articleData.header

with open(file_name, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    timeout = loadBrowser.timeout

    for title, date, href in zip(article_titles, article_dates, article_titles_href):
        browser.get(href)
        loadBrowser.get_browser_loaded(
            href, '//a[@class="logo-img "]', browser
        )

        article_content_element_str = '//div[contains(@class, "detailWrap")]//span[@class="MuiTypography-body1"]/div'
        article_content_element = articleData.get_article_xpath_element(
            article_content_element_str, browser)
        article_content = [
            x.text for x in article_content_element if x.text != '']

        # article_data = [title, href, date, article_content]
        article_data = [
            f'<h3>{title}</h3>',
            date,
            '<div>Barnes and Noble</div>',
            str(f'<article>{article_content}</article>'),
            f'<div>{href}</div>',
        ]

        writer.writerow(article_data)
