'''
Created on Sep 21, 2013

@author: diana.tzinov
'''


import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers


class TestObjectiveCreate(WebDriverTestCase):
    
    
    def testObjectiveCreate(self):
        self.testname="testObjectiveCreate"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers()
        do.setUtils(util)
        do.login()
        last_created_object_link =do.createObject("Objective")
        do.navigateToObjectAndOpenObjectEditWindow("Objective",last_created_object_link)
        do.deleteObject()

        
        
if __name__ == "__main__":
    unittest.main()