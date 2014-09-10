'''
Created on Jul 17, 2013

@author: ukyo.duong
'''


import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestCreatePersonAuthorizationLogInOut(WebDriverTestCase):
    
    
    def testCreatePersonAuthorizationLogInOut(self):
        self.testname="TestCreatePersonAuthorizationLogInOut"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()

        aEmail = "auto_email_" + str(do.getRandomNumber(65535)) + "@gmail.com"
        aName = do.getUniqueString("name")
        aCompany = do.getUniqueString("company")
 
        do.selectMenuInTopRight("Admin Dashboard")
        do.selectMenuItemInnerNavDashBoard("People") 
        do.addPersonInAdminDB(aName, aEmail, aCompany)
        self.assertTrue(do.searchPersonInAdminDB(aName), "Fail searching for newly created person in Admin Dashboard.")
         
        # edit person authorization
        do.selectMenuItemInnerNavDashBoard("People") # on the roles selection      
        do.clickOnEditAuthorization(aName)
        do.assignUserRole("ProgramCreator")
         
        # now log out and then log in with the new account and try to create a program
        oldEmail = "user@example.com"
        oldName = "Example User"
        absFilePath = expanduser("~") + "/ggrc-core/src/ggrc/login/noop.py"
        do.changeUsernameEmail(oldName, aName, oldEmail, aEmail, absFilePath)
        do.selectMenuInTopRight("Logout")
         
        # Refresh the page
        do.refresh()
         
        # Log back in
        do.login()
        print "Log in as : " + do.whoAmI()
        last_created_object_link = do.createObject("Program")
        object_name = str(do.util.getTextFromXpathString(last_created_object_link)).strip()
        self.assertTrue(do.partialMatch("program-auto-test", object_name), "Fail to match program name.")
        self.assertEqual(do.whoAmI(), aEmail, "Still logged in as old user.")
 
        # Restore old login information
        do.changeUsernameEmail(aName, oldName, aEmail, oldEmail, absFilePath)
        do.selectMenuInTopRight("Logout")   
        
if __name__ == "__main__":
    unittest.main()
