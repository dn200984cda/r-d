# Ваше завдання — написати парсер, використовуючи Selenium для сайту https://jobs.marksandspencer.com/job-search 
# Потрібно для перших 2(!) сторінок зібрати назву і посилання вакансії.
# На виході у вас має бути JSON-формат:

# [
# {
# “title”: “Customer Assistant - Foods - Vangarde, York”,
# “url”: “https://jobs.marksandspencer.com/job-search/in-store/york-north-yorkshire/customer-assistant-foods-vangarde-york/300003726976573”
# },
# {...} x 19
# ]

import json
from time import time, sleep

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests

def parse():
    driver = webdriver.Chrome()
    max_page = 3

    wait = WebDriverWait(driver, 10)

    result = []

    for page in range(1, max_page):
        driver.get(f'https://jobs.marksandspencer.com/job-search?page={page}')
        wait.until(EC.presence_of_element_located((By.XPATH, '//a[@data-track-url]')))

        # 
        # title //div[contains(@class, 'ais-Hits')]//li//h3
        # url //a[@data-track-url]
        jobs = driver.find_elements(By.CLASS_NAME,"ais-Hits-item")
        #print(jobs.__len__())
        for job in jobs:
            url = job.find_element(By.CSS_SELECTOR, '[data-track-url]').get_attribute('href')
            title = job.find_element(By.TAG_NAME, 'h3').text
            #print(job)

            result.append({
              'title': title,
                'url': url

            })

    driver.quit()

    with open('result.json', 'w') as f:
        json.dump(result, f, indent=4)


if __name__ == '__main__':
    parse()