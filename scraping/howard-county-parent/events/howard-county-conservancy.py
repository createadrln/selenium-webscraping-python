import csv

from utils import (
    loadBrowser,
    articleData
)

# Chromedriver
browser = loadBrowser.browser
loadBrowser.get_browser_loaded(
    'https://www.howardnature.org/events/',
    '//div[@class="et_pb_menu__logo"]//img', browser
)

# Articles
article_data = []

# Titles
article_title_element_str = '//h3[contains(@class, "tribe-events-calendar-list__event-title")]/a'
article_titles_element = articleData.get_article_xpath_element(
    article_title_element_str, browser)
article_titles = articleData.get_article_titles(article_titles_element)

# Links
article_titles_href = articleData.get_article_titles_href(
    article_titles_element)

# Dates
article_date_element_str = '//span[@class="tribe-event-date-start"]'
article_date_element = articleData.get_article_xpath_element(
    article_date_element_str, browser)
article_dates = []

for element in article_date_element:
    text = element.text.split('@')[0] + ', 2023'
    if text[0].isupper():
        article_dates.append(text)
    
# Descriptions
article_description_element_str = '//div[contains(@class, "tribe-events-calendar-list__event-description")]/p'
article_description_element = articleData.get_article_xpath_element(
    article_description_element_str, browser)
article_descriptions = articleData.get_article_titles(article_description_element)

# File
file_name = "data-files/howard-county-parents-data/howard-county-conservancy.csv"
header = ['title', 'url', 'date', 'content']

with open(file_name, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)

    for title, date, href, description in zip(article_titles, article_dates, article_titles_href, article_descriptions):
        article_data = [title, href, date, description]
        writer.writerow(article_data)
