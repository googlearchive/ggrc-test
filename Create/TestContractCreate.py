'''
Created on Jul 17, 2013

@author: diana.tzinov
'''


import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers


class TestContractCreate(WebDriverTestCase):
    
    
    def testContractCreate(self):
        self.testname="TestContractCreate"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()
        last_created_object_link =do.createObject("Contract")
        do.navigateToObjectAndOpenObjectEditWindow("Contract",last_created_object_link)
        do.deleteObject()
       
        
if __name__ == "__main__":
    unittest.main()
