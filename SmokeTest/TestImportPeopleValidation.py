'''
Created on Jul 21, 2013

@author: ukyo.duong

Description:  Validate import file, have more than one the same emails to violate email uniqueness

'''

import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestImportPeopleValidation(WebDriverTestCase):
    
    dupEmail = config.test_db + "PEOPLE_DUP_EMAIL.csv"
    wrongType = config.test_db + "PEOPLE_WRONG_TYPE.csv"
    noEmail = config.test_db + "PEOPLE_NO_EMAIL.csv"
    nonExist = config.test_db + "non_exist.csv"
           
    def testImportPeopleValidation(self):
        self.testname="TestImportPeopleValidation"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        do = Helpers(self)
        do.setUtils(util)
        do.login()

        do.selectMenuInTopRight("Admin Dashboard")
        self.assertFalse(do.importFile("People", self.dupEmail, False, "Error"), "Fail negative test on duplicate email.")   
          
        do.selectMenuInTopRight("Admin Dashboard")  
        self.assertFalse(do.importFile("People", self.noEmail, False, "Error"), "Fail negative test with email field.") 
         
        do.selectMenuInTopRight("Admin Dashboard")
        self.assertFalse(do.importFile("People", self.wrongType, False, "Error"), "Fail negative test where type is not people.") 
        
        # THIS ONE FAILS BECAUSE THERE IS A AN ACTUAL BUG !!!  16463790 "Uncaught SecurityError" 
        print ("THIS ONE FAILS BECAUSE THERE IS A AN ACTUAL BUG !!!  16463790 'Uncaught SecurityError.' ")
        print ("Need to uncomment when it's fixed.")
        #do.selectMenuInTopRight("Admin Dashboard")
        #self.assertFalse(do.importFile("People", self.nonExist, False), "Fail negative test where file does not exist.")       
        
if __name__ == "__main__":
    unittest.main()
