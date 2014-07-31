'''
Created on Jul 11, 2014

@author: uduong

This test script creates a new user and assigns him/her the role of ProgramCreator.
'''

import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestCreateANewUserInLHS(WebDriverTestCase):
       
    def testCreateANewUserInLHS(self):
        self.testname="TestCreateANewUserInLHS"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()
        print "Log in as : " + do.whoAmI()
        
        number = str(do.getRandomNumber())
        aEmail = "auto_email_" + number + "@gmail.com"
        aName = do.getUniqueString("name")
        aCompany = do.getUniqueString("company")      
        do.createPersonLHN(aName, aEmail, aCompany)        
               
if __name__ == "__main__":
    unittest.main()