'''
Created on Jul 16, 2013

@author: ukyo.duong
'''

import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers

class TestMapSystemToPeople(WebDriverTestCase):
    
    def testMapSystemToPeople(self):
        self.testname="TestMapSystemToPeople"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()

        aEmail = "auto_email_" + str(do.getRandomNumber()) + "@gmail.com"
        aName = do.getUniqueString("name")
        aCompany = do.getUniqueString("company")
        
        titleSys = do.getUniqueString("system")        
        do.createObject("System", titleSys)
        
        do.createPersonLHN(aName, aEmail, aCompany)
        do.mapAObjectLHN("System", titleSys)
        
if __name__ == "__main__":
    unittest.main()
