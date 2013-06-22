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
        if browser == "firefox":
            self.profile = webdriver.firefox.firefox_profile.FirefoxProfile()
            self.profile.native_events_enabled
            self.driver = webdriver.Firefox(self.profile)
            self.profile_path = self.profile.path 
        if browser =="chrome":
            if config.use_remote_webdriver:
                self.driver = RemoteWebDriver(config.remote_webdriver_url, DesiredCapabilities.CHROME);
            else:
                self.driver = webdriver.Chrome(config.chrome_driver_filename)   
        self.base_url =config.url 
        self.driver.get(self.base_url)  
        self.verificationErrors = []
        
        
    def tearDown(self):
        self.driver.quit()
