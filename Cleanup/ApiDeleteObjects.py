'''
Created on Jan 24, 2014

@author: silas@reciprocitylabs.com
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
JS_DIR = join(THIS_ABS_PATH, '../JavaScripts/')
DELETE_SCRIPT_FILE = join(JS_DIR, 'delete.js')

with open(DELETE_SCRIPT_FILE, 'r') as f:
    DELETE_SCRIPT = f.read().strip()

SECTIONS = [
             #"Audit",
             "Program",
             #"OrgGroup",
             #"Regulation",
             #"Contract",
             #"Policy",
             #"Control",
             #"Objective",
             #Standard",

             #"System",
             #"Process",
             #"DataAsset",
             #"Product",
             #"Project",
             #"Facility",
             #"Market",
]

class TestApiDeleteObject(WebDriverTestCase):

    def testDeleteObject(self):
        self.testname="deleteObject"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        grcobject = GRCObject()
        do = Helpers(self)
        do.setUtils(util)
        do.login()
        for x in range(2):
            for section in SECTIONS:
                do.uncheckMyWorkBox()
                time.sleep(5)
                delete_script = DELETE_SCRIPT.replace("SECTION", section)
                # we don't want it to remove testrecip
                # (once the search works correctly)
                if section in ["Person", "OrgGroup"]:
                    delete_script = delete_script.replace(
                        "DELETE_REGEX", r"/(A|a)uto/"
                    )
                else:
                    delete_script = delete_script.replace(
                        "DELETE_REGEX", r"/(A|a)uto|(T|t)est/"
                    )
                print section
                util.driver.execute_script(delete_script)
                time.sleep(180)
                # refresh to dashboard
                self.driver.get(self.base_url + "/dashboard")

if __name__ == "__main__":
    unittest.main()
