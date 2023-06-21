from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

option = webdriver.ChromeOptions().add_argument('--incognito')

browser = webdriver.Chrome(
    executable_path='./config/chromedriver', chrome_options=option)
timeout = 20


def get_browser_loaded(url, xpath, browser):
    browser.get(url)
    try:
        WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located((
                By.XPATH, xpath
            )))
    except TimeoutException:
        print('Timed out waiting for page to load')
        browser.quit()
