'''
Created on Feb 11, 2013

@author: diana.tzinov
'''
from os.path import expanduser 
# the possible environment values are "STAGE", "USER"   "PRODUCTION","INTEGRATION",

url = " http://grc-dev.appspot.com/"
environment = ""
user = ""
browser = "chrome"
#browser = "firefox"
username ="testrecip@gmail.com"
password = "testrecip1"
use_remote_webdriver = True
remote_webdriver_url = "http://ci.reciprocitylabs.com:4444/wd/hub"
jasmine_url = "file:///Users/diana.tzinov/Downloads/jasmine/jasmine-all-good.htm"
chrome_driver_filename = expanduser("~") + "/bin/chromedriver"