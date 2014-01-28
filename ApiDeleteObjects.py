'''
Created on Sep 26, 2013

@author: diana.tzinov
'''
import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers
from helperRecip.GRCObject import GRCObject

from os.path import abspath, dirname, join
THIS_ABS_PATH = abspath(dirname(__file__))
JS_DIR = join(THIS_ABS_PATH, 'JavaScripts/')
DELETE_SCRIPT_FILE = join(JS_DIR, 'delete.js')

with open(DELETE_SCRIPT_FILE, 'r') as f:
    DELETE_SCRIPT = f.read().strip()

SECTIONS = [
             "OrgGroup",
             "Regulation",
             "Contract",
             "Policy",
             "Control",
             "Objective",

             "System",
             "Process",
             "DataAsset",
             "Product",
             "Project",
             "Facility",
             "Market",
             "Program",
]

class TestDeleteObject(WebDriverTestCase):

    def testDeleteObject(self):
        self.testname="deleteObject"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        grcobject = GRCObject()
        do = Helpers()
        do.setUtils(util)
        do.login()
        for x in range(3):
            for section in SECTIONS:
                time.sleep(5)
                delete_script = DELETE_SCRIPT.replace("SECTION", section)
                print section
                util.driver.execute_script(delete_script)
                time.sleep(200)
                util.refreshPage()

if __name__ == "__main__":
    unittest.main()
