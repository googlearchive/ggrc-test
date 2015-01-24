'''
Created on July 14, 2014

@author: ukyo.duong

Notes:  the possible environment values are "STAGE", "USER"   "PRODUCTION","INTEGRATION"

'''
from os.path import expanduser 
import sys, os

url = os.getenv('TEST_SITE_URL', "http://localhost:8080")
remote_webdriver_url = os.getenv('REMOTE_WEBDRIVER_URL', "http://ci.reciprocitylabs.com:4444/wd/hub")
use_remote_webdriver = bool(remote_webdriver_url)
chrome_driver_filename = os.getenv('CHROME_DRIVER_PATH', "/usr/bin/chromedriver")
path = expanduser("~") + "/Downloads/"
file_download_path = os.getenv('FILE_DOWNLOAD_PATH', path)
default_db_path = expanduser("~") + "/test_db/"
test_db = os.getenv('TEST_DB_PATH', default_db_path)
username = os.getenv('TEST_SITE_USERNAME', "")
password = os.getenv('TEST_SITE_PASSWORD', "")
browser = "chrome"
environment = ""
user = ""
jasmine_url = ""
same_password = "ask911$$"
no_access1 = "user1world@gmail.com"
no_access2 = "user11world@gmail.com"
reader1 = "user2world@gmail.com"
reader2 = "user22world@gmail.com"
creator1 = "user3world@gmail.com"
creator2 = "user33world@gmail.com"
editor1 = "user4world@gmail.com"
editor2 = "user44world@gmail.com"