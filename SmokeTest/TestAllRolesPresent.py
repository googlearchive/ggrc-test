'''
Created on Dec 2, 2014

    Verify that different roles exist.

@author: uduong
'''


import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.GRCObject import GRCObject
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestAllRolesPresent(WebDriverTestCase):
    
    
    def testAllRolesPresent(self):
        self.testname="TestAllRolesPresent"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        grcobject = GRCObject()
        do = Helpers(self)
        do.setUtils(util)
        do.login()
               
        do.selectMenuInTopRight("Admin Dashboard")
        do.selectMenuItemInnerNavDashBoard("Roles")
        do.verifyDifferentRolesExist() 

if __name__ == "__main__":
    unittest.main()
