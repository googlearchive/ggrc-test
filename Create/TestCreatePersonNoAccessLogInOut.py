'''
Created on Aug 7, 2014

@author: uduong

Description: No-access role cannot create any object including new workflow

'''

import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestCreatePersonNoAccessLogInOut(WebDriverTestCase):
    
    
    def testCreatePersonNoAccessLogInOut(self):
        self.testname="TestCreatePersonNoAccessLogInOut"
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
        do.assignUserRole("No access")
           
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
                
        object_list = ["Program", "Task", "Audit", "Regulation", "Policy", "Standard", "Contract", "Clause", 
                       "Section", "Objective", "Control", "Person", "OrgGroup", "System","Process", "DataAsset",
                       "Product", "Project", "Facility", "Market"]
        
        # no Create New occurs
        for object in object_list:           
            do.navigateLHSMenu4NoAccess(object)
            do.assertFalse(do.doesThisElementExist(str(Elements.left_nav_object_section_add_button).replace("OBJECT", object), 8))
       
        # Restore old login information
        do.changeUsernameEmail(aName, oldName, aEmail, oldEmail, absFilePath)   
        
if __name__ == "__main__":
    unittest.main()