# TODO Implement ability to provide multiple dealers
# TODO Catch exceptions for non-existent/cancelled dealer IDs
# TODO Check current feed status on the off-chance that it's already disabled, if necessary
# TODO Consider sending requests instead https://my.auction123.com/Inventory/updateexportsites.aspx?disablesite=true&siteid=960&mapid=117853288275809

import argparse
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# Supply a secrets.py file with variables for dashboard login credentials
from secrets import A_USER, A_PASS

start_time = time.time()

# Initialize argument parser and create positional and optional arguments
parser = argparse.ArgumentParser(description="This program will navigate to the specified dealer's Exports page and, if specified, toggle the Facebook feed status.")
parser.add_argument('dealer_id', type=int, help="dealer whose facebook feed status you wish to view/toggle")
parser.add_argument('-t', '--toggle', action='store_true', help="specify to toggle the facebook feed status")
parser.add_argument('--headless', action='store_true', help="run the browser in headless mode (invisible)")
args = parser.parse_args()

goto_dealer_id = args.dealer_id
toggle_mode = args.toggle
headless_mode = args.headless
xpath_fbexport = '//*[@data-exportid="960"]/div/div[7]/span'
xpath_dealer_id = '//*[@id="DealerName"]/span[2]'

# I used to have a full path here, hence raw string literal. Changed it to search for the driver in the root folder
chromedriver = r'chromedriver.exe'

# Browser options
browser_options = webdriver.ChromeOptions()
browser_options.add_experimental_option('excludeSwitches', ['enable-logging'])
if headless_mode:
    browser_options.add_argument('--headless')
    # If both in "toggle" mode and "headless" mode, Selenium times out
    # Ironically, setting a window size is a workaround for this issue. Seems to happen with responsive pages
    browser_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=browser_options, executable_path=chromedriver)
driver.maximize_window()
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
if str(goto_dealer_id) != dealer_id:
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

if toggle_mode:
    # Locate feed toggle button, wait until clickable, and click it
    button_toggle = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_fbexport)))
    button_toggle.click()
    print(f"{goto_dealer_id} - Facebook feed status has been toggled.")
else:
    print("Navigation complete.")

end_time = (round(time.time() - start_time, 2))
print(f"Process time: {end_time}")