from datetime import datetime
import json
import os, sys, re
from time import strftime

from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
import time, unittest
from os.path import abspath, dirname, expanduser, join

import config


# ON OTHER DEPLOYMENTS, CHANGE THIS to the server user name
SERVER_USER = 'jenkins'

TARGET_FOLDER_DICT = {
    "http://grc-test.appspot.com/": "test",
    "http://grc-dev.appspot.com/": "dev",
    "http://localhost:8080/": "local",
}


# Helper functions for changing behavior based on whether or not
# the program is running on the CI server.
# TODO: Find a better module for these
def is_on_server():
    """Used to decide where the output files go"""
    user = os.path.expanduser('~').split('/')[-1]
    return user == SERVER_USER

# 
def base_metrics_dir():
    THIS_ABS_PATH = abspath(dirname(__file__))
    ROOT_PATH = abspath(join(THIS_ABS_PATH, '../'))
    test_dir_name = ROOT_PATH.split('/')[-1]
    if is_on_server():
        return join(ROOT_PATH, '../../metrics/{}'.format(test_dir_name))
    else:
        return join(ROOT_PATH, 'Benchmarks')

class WebDriverTestCase(TestCase):

    def setup(self):
        # note start time
        self.t_start = datetime.now()
        # initialize benchmark dict first
        self.benchmarks = {'name': self.testname, 'results': {}}
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
        self.driver.set_window_size(1024, 800)
        self.verificationErrors = []
        print "Starting " + self.testname + " at "+strftime("%Y_%m_%d__%H_%M_%S")

    def benchmarks_json(self):
        return json.dumps(self.benchmarks)

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

    def output_file_name(self):
        return "{0}_{1}".format(self.benchmarks.get('name'), self.benchmarks.get('timestamp'))

    def write_results(self, json_str):
        outfile = join(self.base_metrics_dir(), self.output_file_name())
        with open(outfile, "w") as f:
            f.write(json_str)

    def tearDown(self):
        self.t_end = datetime.now()
        self.t_total = (self.t_end - self.t_start).total_seconds()
        self.benchmarks['results']['overall_time'] = self.t_total
        self.write_results(json.dumps(self.benchmarks))
        self.driver.quit()

