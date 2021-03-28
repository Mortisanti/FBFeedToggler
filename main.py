from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from secrets import A_USER, A_PASS
import os
import time
import schedule

# Dealer to switch to
# TODO Check if already on dealer account
goto_dealer_id = str(14393)
xpath_fbexport = '//*[@data-exportid="960"]/div/div[7]/span'
xpath_dealer_id = '//*[@id="DealerName"]/span[2]'
chromedriver = r'F:\Users\Michael\Documents\Programming\Python\chromedriver.exe'
browser_options = webdriver.ChromeOptions()
browser_options.add_experimental_option('excludeSwitches', ['enable-logging'])
# browser_options.add_argument('--headless')
# browser_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=browser_options, executable_path=chromedriver)
wait = WebDriverWait(driver, 10)

# Navigate to Auction123 login page, enter credentials, log in
driver.get('https://my.auction123.com/login.aspx?ReturnUrl=%2f')
field_user = driver.find_element_by_name('ctl00$BodyPlaceHolder$userName').send_keys(A_USER)
field_pass = driver.find_element_by_name('ctl00$BodyPlaceHolder$password').send_keys(A_PASS)
driver.find_element_by_name('ctl00$BodyPlaceHolder$SignInButton').click()

# Switch to iframe, store sidebar and inner frame elements, switch to inner frame
iframe = driver.find_element_by_tag_name('iframe')
driver.switch_to.frame(iframe)
frame_inner = driver.find_element_by_id('listContent')
driver.switch_to.frame(frame_inner)

# Get dealer ID and check if equal to provided ID; if not, switch to provided dealer ID

check_dealer_id = driver.find_element_by_xpath(xpath_dealer_id)
dealer_id = check_dealer_id.text.replace('(', '').replace(')', '')

# Switch to supplied dealer ID, if not already in the account
if goto_dealer_id != dealer_id:
    driver.get(f'https://my.auction123.com/DealerRedirect.aspx?dealer_id={goto_dealer_id}')
    iframe = driver.find_element_by_tag_name('iframe')
else:
    driver.switch_to.default_content()

# Locate and switch to the sidebar (aka menuBar), then click into the Feeds page
driver.switch_to.frame(iframe)
frame_sidebar = driver.find_element_by_name('menuBar')
driver.switch_to.frame(frame_sidebar)
driver.find_element_by_link_text('Feeds').click()

# Switch back to the main page (to back out of the menuBar frame)
driver.switch_to.default_content()

# Switch back into the iframe, enter the inner content's frame, and click into Export Sites
driver.switch_to.frame(iframe)
frame_inner = driver.find_element_by_id('listContent')
driver.switch_to.frame(frame_inner)
driver.find_element_by_link_text('Export Sites').click()

"""
# Locate feed toggle button, wait until clickable, and click it
button_toggle = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_fbexport)))
button_toggle.click()
"""