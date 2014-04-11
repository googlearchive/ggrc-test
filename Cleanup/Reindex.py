'''
Created on Jan 24, 2014

@author: silas@reciprocitylabs.com
'''
import unittest
import time
from helperRecip.testcase import *
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers

from os.path import abspath, dirname, join
THIS_ABS_PATH = abspath(dirname(__file__))
JS_DIR = join(THIS_ABS_PATH, '../JavaScripts/')
REINDEX_SCRIPT_FILE = join(JS_DIR, 'reindex.js')

with open(REINDEX_SCRIPT_FILE, 'r') as f:
    REINDEX_SCRIPT = f.read().strip()

SECTIONS = [
             "Program",
             "OrgGroup",
             "Regulation",
             "Contract",
             "Policy",
             "Control",
             "Objective",
             "Standard",

             "System",
             "Process",
             "DataAsset",
             "Product",
             "Project",
             "Facility",
             "Market",
]

class TestReindex(WebDriverTestCase):

    def testReindex(self):
        self.testname="deleteObject"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        do = Helpers(self)
        do.setUtils(util)
        do.login()
        util.driver.execute_script(REINDEX_SCRIPT)
        time.sleep(90)

if __name__ == "__main__":
    unittest.main()
