'''
Created on Jun 24, 2013

@author: diana.tzinov
'''
import unittest
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers


class TestJasmineExample(WebDriverTestCase):
    
    
    def testJasmineExample(self):
        self.setup_jasmine()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers()
        do.setUtils(util)
        util.waitForElementToBePresent(element.jasmine_results)
        self.assertTrue(util.isElementPresent(element.jasmine_results), "no results on the page found")
        
if __name__ == "__main__":
    unittest.main()