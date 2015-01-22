'''
Created on Jan 21, 2015

@author: ukyo duong
'''


import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestSectionCreate(WebDriverTestCase):
    
    
    def testSectionCreate(self):
        self.testname="TestSectionCreate"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()
        last_created_object_link =do.createObjectSaveAddAnother("Section", "", "unchecked")
        do.navigateToObjectAndOpenObjectEditWindow("Section",last_created_object_link)
        do.deleteObject()
       
        
if __name__ == "__main__":
    unittest.main()
