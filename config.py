'''
Created on July 14, 2014

@author: ukyo.duong

Notes:  the possible environment values are "STAGE", "USER"   "PRODUCTION","INTEGRATION"

'''
from os.path import expanduser 
import sys, os

url = os.getenv('TEST_SITE_URL', "http://localhost:8080")
remote_webdriver_url = os.getenv('REMOTE_WEBDRIVER_URL', "")
use_remote_webdriver = bool(remote_webdriver_url)
chrome_driver_filename = os.getenv('CHROME_DRIVER_PATH', "/usr/bin/chromedriver")
path = expanduser("~") + "/Downloads/"
file_download_path = os.getenv('FILE_DOWNLOAD_PATH', path)
test_db = os.getenv('TEST_DB_PATH', "/test_db")
username = os.getenv('TEST_SITE_USERNAME', "")
password = os.getenv('TEST_SITE_PASSWORD', "")
browser = "chrome"
environment = ""
user = ""
jasmine_url = ""