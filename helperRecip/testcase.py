from datetime import datetime
import json
import os, sys, re
from time import strftime, time

from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
import unittest
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


def base_metrics_dir():
    THIS_ABS_PATH = abspath(dirname(__file__))
    ROOT_PATH = abspath(join(THIS_ABS_PATH, '../'))
    relative_dir = os.getenv('METRICS_DIR', 'Benchmarks')
    return join(ROOT_PATH, relative_dir)


def base_diagnostics_dir():
    THIS_ABS_PATH = abspath(dirname(__file__))
    ROOT_PATH = abspath(join(THIS_ABS_PATH, '../'))
    relative_dir = os.getenv('DIAGNOSTICS_DIR', 'Diagnostics')
    return join(ROOT_PATH, relative_dir)


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
                print "ukyo chrome: checkpoint1"
                self.driver = webdriver.Chrome(config.chrome_driver_filename)
        self.base_url =config.jasmine_url
        self.driver.get(self.base_url)
        self.verificationErrors = []

    def output_file_name(self):
        return "{0}_{1}".format(self.benchmarks.get('name'), self.benchmarks.get('timestamp'))

    def diagnostic_file_path(self, identifier):
        """returns an absolute path to a new file to the diagnostics directory with the name _identifier_, prepended by the timestamp; the time stamp is obtained from the benchmarks dir; if there is none, one is generated
        """
        timestamp = self.benchmarks.get('timestamp', str(int(time())))
        filename = "{0}_{1}".format(timestamp, identifier)
        return join(base_diagnostics_dir(), filename)

    def browser_log_string(self):
        output = u""
        for x in self.driver.log_types:
            output += u"====\n{} log\n====\n".format(x)
            output += unicode(self.driver.get_log(x))
            output += u"\n\n"
        return output

    def write_results(self, string):
        outfile = join(base_metrics_dir(), self.output_file_name())
        with open(outfile, "w") as f:
            f.write(string)

    def tearDown(self):
        # collect overall time data
        self.t_end = datetime.now()
        self.t_total = (self.t_end - self.t_start).total_seconds()
        self.benchmarks['results']['overall_time'] = self.t_total
        # report diagnostics in case of failure
        if self._resultForDoCleanups.failures:
            screenshot_file = self.diagnostic_file_path('screenshot.png')
            self.driver.get_screenshot_as_file(screenshot_file)
            js_log_file = self.diagnostic_file_path('js_log.txt')
            with open(js_log_file, "w") as f:
                f.write(self.browser_log_string().encode('utf8'))
            dom_file = self.diagnostic_file_path('dom_file.html')
            with open(dom_file, "w") as f:
                f.write(self.driver.page_source.encode('utf8'))
        # write performance data
        self.write_results(json.dumps(self.benchmarks))
        self.driver.quit()

