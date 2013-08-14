'''
Created on Jul 24, 2013

@author: diana.tzinov
'''


import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers


class TestSystemCreate(WebDriverTestCase):
    
    
    def testSystemCreate(self):
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        do = Helpers()
        do.setUtils(util)
        do.Login()
        do.CreateObject("System")

        
        
if __name__ == "__main__":
    unittest.main()