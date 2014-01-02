import os, sys, re

from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
import time, unittest
from os.path import expanduser 
import config
from time import strftime

class WebDriverTestCase(TestCase):

    def setup(self):
        browser = config.browser
        if browser == "firefox":
            self.profile = FirefoxProfile()
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
        print "Starting " + self.testname + " at "+strftime("%Y_%m_%d__%H_%M_%S")
        
    def setup_jasmine(self):
        browser = config.browser
        if browser == "firefox":
            self.profile = FirefoxProfile()
            self.profile.native_events_enabled
            self.driver = webdriver.Firefox(self.profile)
            self.profile_path = self.profile.path 
        if browser =="chrome":
            if config.use_remote_webdriver:
                self.driver = RemoteWebDriver(config.remote_webdriver_url, DesiredCapabilities.CHROME);
            else:
                self.driver = webdriver.Chrome(config.chrome_driver_filename)   
        self.base_url =config.jasmine_url 
        self.driver.get(self.base_url)  
        self.verificationErrors = []
        
    def tearDown(self):
        # pass
        self.driver.quit()
