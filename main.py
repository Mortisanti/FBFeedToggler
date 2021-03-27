from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from secrets import A_USER, A_PASS
import os
import time
import schedule

# Dealer to switch to
# TODO Check if already on dealer account
dealer_id = str(15414)
chromedriver = r'F:\Users\Michael\Documents\Programming\Python\chromedriver.exe'

browser_options = webdriver.ChromeOptions()
browser_options.add_experimental_option('excludeSwitches', ['enable-logging'])
# browser_options.add_argument('--headless')
# browser_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=browser_options, executable_path=chromedriver)

# Navigate to Auction123 login page, enter credentials, log in
driver.get('https://my.auction123.com/login.aspx?ReturnUrl=%2f')
field_user = driver.find_element_by_name('ctl00$BodyPlaceHolder$userName')
field_user.send_keys(A_USER)
field_pass = driver.find_element_by_name('ctl00$BodyPlaceHolder$password')
field_pass.send_keys(A_PASS)
button_submit = driver.find_element_by_name('ctl00$BodyPlaceHolder$SignInButton')
button_submit.click()
# Switch to provided dealer ID
driver.get(f'https://my.auction123.com/DealerRedirect.aspx?dealer_id={dealer_id}')

# driver.implicitly_wait(5)
iframe = driver.find_element_by_tag_name('iframe')
driver.switch_to.frame(iframe)
testing = driver.find_element_by_xpath('//*[@id="InventoryBulkImportLink"]/a')
print(testing)