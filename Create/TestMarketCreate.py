'''
Created on Jul 23, 2013

@author: diana.tzinov
'''

import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers


class TestMarketCreate(WebDriverTestCase):
    
    
    def testMarketCreate(self):
        self.testname="TestMarketCreate"    
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()
        last_created_object_link =do.createObject("Market")
        do.navigateToObjectAndOpenObjectEditWindow("Market",last_created_object_link)
        do.deleteObject()

        
        
if __name__ == "__main__":
    unittest.main()
