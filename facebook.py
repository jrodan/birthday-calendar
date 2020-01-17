# importing necessary classes
# from different modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
import birthday
import config_local as cfg


def scrollDown(browser):
    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")
    counter = 0

    while counter < 15:
        # Scroll down to bottom
        browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script(
            "return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        counter += 1


chrome_options = webdriver.ChromeOptions()

prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
browser = webdriver.Chrome()

# open facebook.com using get() method
browser.get('https://www.facebook.com/')

element = browser.find_elements_by_xpath('//*[@id ="email"]')
element[0].send_keys(cfg.facebookUser)

print("Username Entered")

element = browser.find_element_by_xpath('//*[@id ="pass"]')
element.send_keys(cfg.facebookPassword)

print("Password Entered")

# logging in
log_in = browser.find_elements_by_id('loginbutton')
log_in[0].click()

print("Login Successfull")

browser.get('https://www.facebook.com/events/birthdays/')

webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()
scrollDown(browser)

# element = browser.find_element_by_css_selector("._42ef a") # title="Vorname Nachname"
element = browser.find_elements_by_css_selector(
    "._43q7 a")  # data-tooltip-content="Jan Rue (24.1.)"

birthdayList = list()

# birthday.Birthday()


cnt = 0

birthdaysS = ""

for el in element:
    value = el.get_attribute("data-tooltip-content")
    indexBraket = value.find("(")
    date = value[indexBraket+1:len(value)-1]
    name = value[0:indexBraket-1]

    row = name + ";"+date+"\r\n"
    if(birthdaysS.find(row) == -1):
        birthdaysS += name + ";"+date+"\r\n"
    print("name: "+name+" birthday: "+date)

# Close the browser
browser.close()


f = open("exports/facebook-extract.txt", "w+")
f.write(birthdaysS)
f.close()
