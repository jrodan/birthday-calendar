# importing necessary classes
# from different modules
#from .. import config_local as cfg
import sys, os
sys.path.insert(0, os.path.abspath('..'))
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
import datetime
from src import birthday
import config_local as cfg

chrome_options = Options()
chrome_options.add_argument("--headless")
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
browser = webdriver.Chrome(options=chrome_options)

browser.get(cfg.linkedInURLPage1)

el = browser.find_element_by_xpath(
    "//input[@name='session_key']")
el.send_keys(cfg.linkedInUser)

el = browser.find_element_by_xpath(
    "//input[@name='session_password']")
el.send_keys(cfg.linkedInPassword)

log_in = browser.find_elements_by_css_selector(
    '.login__form_action_container button')
log_in[0].click()

browser.get(cfg.linkedInURLPage2)


element = browser.find_elements_by_css_selector(
    ".nt-card__occlusion-wrapper article .nt-card__core-rail a .visually-hidden")

birthdayList = list()

cnt = 0
birthdaysS = ""
prefix = "Gratulieren Sie "
suffix = " zum Geburtstag (heute)"

for el in element:

    value = el.text
    now = datetime.datetime.now()

    if(value.find(suffix) > -1):
        date = now.strftime("%d.%m.%Y")
        name = value.replace(prefix, "").replace(suffix, "")

        row = name + ";"+date+"\r\n"
        if(birthdaysS.find(row) == -1):
            birthdaysS += name + ";"+date+"\r\n"
        print("name: "+name+" birthday: "+date)

# Close the browser
browser.close()


f = open("exports/linkedin-extract.txt", "w+")
f.write(birthdaysS)
f.close()
