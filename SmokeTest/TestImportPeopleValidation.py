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
    
    dupEmail = config.fileDownloadPath + "PEOPLE_DUP_EMAIL.csv"
    wrongType = config.fileDownloadPath + "PEOPLE_WRONG_TYPE.csv"
    noEmail = config.fileDownloadPath + "PEOPLE_NO_EMAIL.csv"
    nonExist = config.fileDownloadPath + "non_exist.csv"
           
    def testImportPeopleValidation(self):
        self.testname="TestImportPeopleValidation"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        do = Helpers(self)
        do.setUtils(util)
        do.login()

        do.selectMenuInTopRight("Admin Dashboard")
        self.assertTrue(do.importFile("People", self.dupEmail, True), "Fail negative test on duplicate email.")   
         
        do.selectMenuInTopRight("Admin Dashboard")  
        self.assertTrue(do.importFile("People", self.noEmail, True), "Fail negative test with email field.") 
        
        do.selectMenuInTopRight("Admin Dashboard")
        self.assertTrue(do.importFile("People", self.wrongType, True), "Fail negative test where type is not people.") 
        
        # THIS ONE FAILS BECAUSE THERE IS A AN ACTUAL BUG !!!  16463790 "Uncaught SecurityError" 
        do.selectMenuInTopRight("Admin Dashboard")
        self.assertTrue(do.importFile("People", self.nonExist, True), "Fail negative test where file does not exist.") 

 
        
        
if __name__ == "__main__":
    unittest.main()
