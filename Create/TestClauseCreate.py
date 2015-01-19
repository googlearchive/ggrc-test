'''
Created on Jan 16, 2015

@author: ukyo duong
'''


import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers


class TestClauseCreate(WebDriverTestCase):
    
    
    def testClauseCreate(self):
        self.testname="TestClauseCreate"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()
        last_created_object_link =do.createObject("Clause")
        do.navigateToObjectAndOpenObjectEditWindow("Clause",last_created_object_link)
        do.deleteObject()
        
        
if __name__ == "__main__":
    unittest.main()
