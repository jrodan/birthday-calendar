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

chrome_options = webdriver.ChromeOptions()

prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
browser = webdriver.Chrome()

# open facebook.com using get() method
browser.get(cfg.confluencePage1)


element = browser.find_elements_by_xpath('//*[@id ="os_username"]')
element[0].send_keys(cfg.confluenceUser)

print("Username Entered")

element = browser.find_element_by_xpath('//*[@id ="os_password"]')
element.send_keys(cfg.confluencePassword)

print("Password Entered")

# logging in
log_in = browser.find_elements_by_id('loginButton')
log_in[0].click()

print("Login Successfull")

browser.get(
    cfg.confluencePage2)

element = browser.find_elements_by_css_selector(
    "#child_ul16361-0 li .plugin_pagetree_children_content a")

birthdaysS = ""
links = list()

for el in element:
    links.append(el.get_attribute("href"))

for link in links:

    browser.get(link)
    name = browser.find_element_by_css_selector("#title-text a").text

    try:
        p = browser.find_element_by_xpath(
            "//*[contains(text(), 'Geburtsdatum')]")
        pBirthday = p.find_element_by_xpath('..').find_element_by_xpath(
            '..').find_element_by_css_selector("td p")
        date = pBirthday.text.replace("-", ".")
        birthdaysS += name + ";"+date+"\r\n"
        print("name: "+name+" birthday: "+date)
    except:
        print("Birthday of "+name+" could not be extracted")

# Close the browser
browser.close()

f = open("exports/confluence-extract.txt", "w+")
f.write(birthdaysS)
f.close()
