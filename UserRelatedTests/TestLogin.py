'''
Created on Jun 17, 2013

@author: diana.tzinov
'''
import unittest
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers


class TestLogin(WebDriverTestCase):
    
    
    def testLogin(self):
        self.testname="testLogin"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers()
        do.setUtils(util)
        do.Login()
        self.assertTrue(util.isElementPresent(element.dashboard_title), "no dashboard page found")
        
if __name__ == "__main__":
    unittest.main()