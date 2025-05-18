from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import json

def login(driver, cookies):
    driver.get('https://www.tiktok.com/')
    wait = WebDriverWait(driver, 10)
    driver.delete_all_cookies()
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
    time.sleep(5)  # Wait for the dashboard to load

def report_user(driver, user_id):
    driver.get(f'https://www.tiktok.com/@{user_id}')
    time.sleep(3)  # Wait for the profile to load
    report_button = driver.find_element(By.CSS_SELECTOR, 'button[data-e2e=more-vertical-menu-action-reason-report]')
    report_button.click()
    reason_select = driver.find_element(By.CSS_SELECTOR, 'select[data-e2e=report-reason-select]')
    reason_select.send_keys('Spam')
    submit_button = driver.find_element(By.CSS_SELECTOR, 'button[data-e2e=report-submit-button]')
    submit_button.click()
    time.sleep(3)  # Wait for the report confirmation
    print(f"Reported user: {user_id}")

def main():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run browser in background
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    # Load the target user's cookies from a JSON file
    with open('cookies.json', 'r') as f:
        cookies = json.load(f)

    login(driver, cookies)

    # Load the list of users to report from a CSV file
    users_df = pd.read_csv('users_to_report.csv')
    users_to_report = users_df['user_id'].tolist()

    for user_id in users_to_report:
        report_user(driver, user_id)
        time.sleep(5)  # Add a delay between reports to avoid detection

if __name__ == '__main__':
    main()

