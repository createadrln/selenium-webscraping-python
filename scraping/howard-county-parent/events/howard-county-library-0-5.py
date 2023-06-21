from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import time

import csv

from utils import (
    loadBrowser,
    articleData,
)

# urls = [
#     'https://howardcounty.librarycalendar.com/?age_groups%5B116%5D=116',
#     'https://howardcounty.librarycalendar.com/events/month/2023/04?age_groups%5B116%5D=116',
#     'https://howardcounty.librarycalendar.com/events/month/2023/05?age_groups%5B116%5D=116',
#     'https://howardcounty.librarycalendar.com/events/month/2023/06?age_groups%5B116%5D=116',
#     'https://howardcounty.librarycalendar.com/events/month/2023/07?age_groups%5B116%5D=116',
#     'https://howardcounty.librarycalendar.com/events/month/2023/08?age_groups%5B116%5D=116',
#     'https://howardcounty.librarycalendar.com/events/month/2023/09?age_groups%5B116%5D=116'
# ]

# for url in urls:
#     # Run

# Chromedriver
browser = loadBrowser.browser
loadBrowser.get_browser_loaded(
    'https://howardcounty.librarycalendar.com/events/month/2023/06?age_groups%5B116%5D=116',
    '//div[@class="calendar__day"]//article', browser)

time.sleep(10)

# Articles
article_data = []

# Titles
article_title_element_str = '//section[contains(@class, "calendar--month")]//a[@class="lc-event__link"]'
article_titles_element = articleData.get_article_xpath_element(
    article_title_element_str, browser)

# Links
article_titles_href = articleData.get_article_titles_href(
    article_titles_element)

# File
file_name = "data-files/howard-county-parents-data/howard-county-library-june-2023.csv"
header = ['title', 'link', 'date', 'source', 'content']

with open(file_name, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    timeout = loadBrowser.timeout

    for href in article_titles_href:
        browser.get(href)
        try:
            WebDriverWait(browser, timeout).until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    '//h1/span'
                )))
        except TimeoutException:
            print("Timed out waiting for page to load")
            browser.quit()

        article_title_element = articleData.get_article_xpath_element(
            '//h1/span', browser)
        article_title = [x.text for x in article_title_element]
        article_title_text = article_title[0]

        article_date_element = articleData.get_article_xpath_element(
            '//div[@class="lc-event-info-item lc-event-info-item--date"]', browser)
        article_date = [x.text for x in article_date_element]
        article_date_text = article_date[0]

        article_content_element = articleData.get_article_xpath_element(
            '//section[@class="lc-event-content lc-event__content"]', browser)
        article_content_text = ''

        for article_content in article_content_element:
            article_content_text_stripped = article_content.text.replace(
                '\n', ' ').replace('\r', '')
            article_content_text_stripped = article_content_text_stripped.replace(
                'Remind Me Add To My Calendar Print Share ', '')
            article_content_text_stripped = article_content_text_stripped.replace(
                'Please note you are looking at an event that has already happened. ', '')
            article_content_text_stripped = article_content_text_stripped.replace(
                'Program Description Event Details Families, all ages. ', '')
            article_content_text_stripped = article_content_text_stripped.replace(
                'HCLS is celebrating Pride Month! Please visit bit.ly/hclspride23 to find more classes. ', '')
            article_content_text_stripped = article_content_text_stripped.replace(
                'Program Type: ', '')
            article_content_text = article_content_text_stripped

        article_data = [
            f"<h3>{article_title_text}</h3>",
            f"<a href='{href}'>LINK TO ORIGINAL</a>",
            article_date_text,
            "<div>Howard County Library Ages 0-5</div>",
            f"<article>{article_content_text}</article>",
        ]
        
        # @TODO get location information

        writer.writerow(article_data)
