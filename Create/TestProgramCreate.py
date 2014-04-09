'''
Created on Jul 16, 2013

@author: diana.tzinov
'''


import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers


class TestProgramCreate(WebDriverTestCase):
    
    
    def testProgramCreate(self):
        self.testname="TestProgramCreate"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()
        last_created_object_link =do.createObject("Program")
        do.navigateToObjectAndOpenObjectEditWindow("Program",last_created_object_link)
        do.deleteObject()

        
        
if __name__ == "__main__":
    unittest.main()
