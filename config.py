'''
Created on Feb 11, 2013

@author: diana.tzinov
'''
from os.path import expanduser 
import sys, os

# the possible environment values are "STAGE", "USER"   "PRODUCTION","INTEGRATION",

#print os.environ['PYTHONPATH'].split(os.pathsep)

#url= os.getenv('TEST_SITE_URL', "http://grc-test.appspot.com/")
url= os.getenv('TEST_SITE_URL', "http://localhost:8080")
environment = ""
user = ""
browser = "chrome"
#browser = "firefox"
username ="testrecip@gmail.com"
password = "testrecip1"
use_remote_webdriver = False
remote_webdriver_url = "http://ci.reciprocitylabs.com:4444/wd/hub"
jasmine_url = "file:///Users/diana.tzinov/Downloads/jasmine/jasmine-all-good.htm"
#chrome_driver_filename = expanduser("~") + "/bin/chromedriver"
chrome_driver_filename = "/usr/local/bin/chromedriver"