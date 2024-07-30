import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.keys import Keys
import os
import threading
from os import path

username = os.environ.get('BROWSERSTACK_USERNAME')
accessKey = os.environ.get('BROWSERSTACK_ACCESS_KEY')
test_username=os.getenv('TEST_USERNAME')
password=os.getenv('TEST_PASSWORD')

class SimpleAppiumRun(threading.Thread):
    def __init__(self, argument):
        super(SimpleAppiumRun, self).__init__()
        self.argument = argument

    def run(self):
        device_info = self.argument
        bstack_options = {
            "userName": username,
            "accessKey": accessKey
        }
        bstack_options.update(device_info)
        options = ChromeOptions()
        options.set_capability('bstack:options', bstack_options)
        driver = webdriver.Remote(
            command_executor="https://hub.browserstack.com/wd/hub",
            options=options)
        try:
            wait = WebDriverWait(driver, 10)
            driver.get('https://www.bstackdemo.com/')

            # Login to the website
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#signin'))).click()
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="username"]//input'))).send_keys(test_username, Keys.ENTER)
            pword = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]//input'))).send_keys(password, Keys.ENTER)
            wait.until(EC.presence_of_element_located((By.XPATH, '//button[@id="login-btn"]'))).click()
            
            #Filter for samsungs
            wait.until(EC.presence_of_element_located((By.XPATH, '//input[@value="Samsung"]/following-sibling::span'))).click()
            #find and faviorte the Samsung 20+
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@data-sku="samsung-S20+-device-info.png"]//button'))).click()
            fav = driver.find_element(By.CSS_SELECTOR, '#favourites')
            # add to faviortes
            fav.click()
            #Validate the correct phone was added
            el = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@data-sku="samsung-S20+-device-info.png"]//p')))
            #should change to an asseration instead 
            print(el.text)

        finally:
            driver.quit()

#read in the list of devices from json file
CUR_DIR = path.dirname(path.abspath(__file__))
json_data = path.join(CUR_DIR, 'devices.json')
f = open(json_data, 'r')
data = json.load(f)
for device in data['devices']:
    appiumThread = SimpleAppiumRun(device)
    appiumThread.start()