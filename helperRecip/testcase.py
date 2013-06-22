import os, sys, re

from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
import time, unittest
from os.path import expanduser 
import config

class WebDriverTestCase(TestCase):

    def setup(self):
        browser = config.browser
        if browser =="chrome":
            self.driver = RemoteWebDriver("http://ci.reciprocitylabs.com:4444/wd/hub", DesiredCapabilities.CHROME);
        self.base_url =config.url 
        self.driver.get(self.base_url)  
        self.verificationErrors = []
        
        
    def tearDown(self):
        self.driver.quit()
