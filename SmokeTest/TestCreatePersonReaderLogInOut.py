'''
Created on Aug 1, 2014

@author: uduong

Description: Reader can view and work on his assignment but cannot create object or does other admin work.

'''

import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestCreatePersonReaderLogInOut(WebDriverTestCase):
    
    
    def testCreatePersonReaderLogInOut(self):
        self.testname="TestCreatePersonReaderLogInOut"
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
        do.assignUserRole("Reader")
          
        # now log out and then log in with the new account and try to create a program
        oldEmail = "user@example.com"
        oldName = "Example User"
        absFilePath = expanduser("~") + "/ggrc-core/src/ggrc/login/noop.py"
        do.changeUsernameEmail(oldName, aName, oldEmail, aEmail, absFilePath)
        do.selectMenuInTopRight("Logout")
          
        # Refresh the page
        do.refresh()
          
        # Log in with new user
        do.login()
        print "Log in as : " + do.whoAmI()
        
        object_list = ["Program", "Workflow", "Audit", "Regulation", "Policy", "Standard", "Contract", "Clause", 
                       "Section", "Objective", "Control", "Person", "OrgGroup", "System","Process", "DataAsset",
                       "Product", "Project", "Facility", "Market"]
        
        # since it's a reader role, the Create New button won't show
        for object in object_list:
            do.assertFalse(do.doesCreateNewExist(object), "Create New button exists for " + str(object))
 
        print "hi"
        
        # Restore old login information
        do.changeUsernameEmail(aName, oldName, aEmail, oldEmail, absFilePath)   
        
if __name__ == "__main__":
    unittest.main()
