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
import math
from src import birthday
import config_local as cfg
from src import helper

chrome_options = webdriver.ChromeOptions()

prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
browser = webdriver.Chrome()

# open facebook.com using get() method
browser.get(cfg.xingPage1)


element = browser.find_elements_by_xpath('//*[@name="username"]')
element[0].send_keys(cfg.xingUser)

print("Username Entered")

element = browser.find_element_by_xpath('//*[@name="password"]')
element.send_keys(cfg.xingPassword)

print("Password Entered")

# logging in
log_in = browser.find_elements_by_css_selector(
    '.StretchButtonGroup-StretchButtonGroup-stretchButton-87036de4')
log_in[0].click()

print("Login Successfull")

time.sleep(3)
browser.get(cfg.xingPage2)

contentSelector = "#top-of-list div[data-fixed-element='content']"

# get number of persons
numberOfPagesText = browser.find_element_by_css_selector(
    contentSelector + " .list-header__block strong").text
splitText = "von "
index = numberOfPagesText.find(splitText)
print(" index of "+splitText+" is "+str(index))
numberOfEntries = numberOfPagesText[
    index + len(splitText): len(numberOfPagesText)]
numberOfPages = math.ceil(int(numberOfEntries) / 10)
print("pages found: "+str(numberOfPages)+" "+str(numberOfPages))

# parse birthdays
birthdaysS = ""
links = list()
i = 0
while i < numberOfPages:
    elements = browser.find_elements_by_css_selector(
        contentSelector + " ul.item_list li .user-card__block > .media-obj__body")

    for el in elements:
        name = el.find_element_by_css_selector(".user-name").text
        date = el.find_element_by_css_selector(
            ".birthday-item aside .user-card__bday").text

        today = helper.getToday()

        if date == "Morgen":
            date = str(today.day+1) + "." + \
                str(today.month) + "." + str(today.year)
        elif date == "Heute":
            date = str(today.day) + "." + str(today.month) + \
                "." + str(today.year)

        try:
            birthdaysS += name + ";"+date+"\r\n"
            print("name: "+name+" birthday: "+date)
        except:
            print("Birthday of "+name+" could not be extracted")

    if i+1 != numberOfPages:
        nextPage = browser.find_element_by_css_selector(
            "nav .pagination-next a")
        browser.execute_script(
            "arguments[0].scrollIntoView();", nextPage)
        nextPage.click()

    i += 1


# Close the browser
browser.close()

f = open("exports/xing-extract.txt", "w+")
f.write(birthdaysS)
f.close()
