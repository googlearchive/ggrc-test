'''
Created on Jul 17, 2013

@author: diana.tzinov
'''


import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestEventLog(WebDriverTestCase):
    
    
    def testEventLog(self):
        self.testname="TestEventLog"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()

        xpath = do.createObject("Program")
        title = util.getTextFromXpathString(xpath)
        
        do.selectMenuInTopRight("Admin Dashboard")
        do.selectMenuItemInnerNavDashBoard("Events")
        self.assertTrue(do.verifyInfoInEventLogTable(title, 1), "Cannot find it in the Event Log table.")


if __name__ == "__main__":
    unittest.main()
