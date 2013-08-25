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


class TestProjectCreate(WebDriverTestCase):
    
    
    def testProjectCreate(self):
        self.testname="testProjectCreate"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers()
        do.setUtils(util)
        do.Login()
        last_created_object_link =do.CreateObject("Project")
        do.NavigateToObjectAndOpenObjectEditWindow(last_created_object_link)
        do.deleteObject()

        
        
if __name__ == "__main__":
    unittest.main()