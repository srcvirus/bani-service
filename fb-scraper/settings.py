import os
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# User credentials
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

# Required binaries
BROWSER_EXE = "C:\\Program Files\\Mozilla\ Firefox\\firefox.exe"
GECKODRIVER = "C:\\Users\\shiha\\Downloads\\geckodriver-v0.30.0-win64\\geckodriver.exe"
FIREFOX_BINARY = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')

#  Code to disable notifications pop up of Chrome Browser
PROFILE = webdriver.FirefoxProfile()
# PROFILE.DEFAULT_PREFERENCES['frozen']['javascript.enabled'] = False
PROFILE.set_preference("dom.webnotifications.enabled", False)
PROFILE.set_preference("app.update.enabled", False)
PROFILE.update_preferences()
