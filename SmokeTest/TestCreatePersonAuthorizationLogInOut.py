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

        aEmail = "user44world@gmail.com"
        aName = do.getUniqueString("name")
        aCompany = do.getUniqueString("company")
        role = "ProgramCreator"
  
        do.selectMenuInTopRight("Admin Dashboard")
        
        # verify people tab
        do.selectMenuItemInnerNavDashBoard("People")
        
        # SETUP: if that email is already used change it to something else
        do.zeroizeThePersonEmail(aEmail)
         
        # you can add a person 
        do.addPersonInAdminDB(aName, aEmail, aCompany)
         
        # the Next and PREVIOUS page buttons work
        self.assertTrue(do.verifyPrevNextOperation("people"), "Fail verifying Prev and Next buttons.")
        
        # search or filter works
        self.assertTrue(do.searchPersonInAdminDB(aName), "Fail searching for newly created person in Admin Dashboard.")
          
        # edit person authorization    
        do.clickOnEditAuthorization(aName)
        do.assignUserRole(role)
        
        # at this point, 2nd tier is expanded and it's the only row displayed...
        do.verifyPersonInfoOnSecondTier(aName, aEmail, aCompany, role)

        if 'local' not in config.url:
            do.selectMenuInTopRight("Logout")
            do.refresh()
            do.login(aEmail, config.password)
            self.assertEqual(aEmail, do.whoAmI(), "Expect: " + aEmail + ", but see: " + do.whoAmI())
            
        # I can test login with the new user locally but not on on grc-test.appspot.com because it requires actual email
        # and that email has to be unique.  I can't automatically create new fake email account with google that's fraud            
        else:
            oldEmail = "user@example.com"
            oldName = "Example User"
            absFilePath = expanduser("~") + "/ggrc-core/src/ggrc/login/noop.py"
            do.changeUsernameEmail(oldName, aName, oldEmail, aEmail, absFilePath)            
            
            # now log out and then log in with the new account and try to create a program
            do.selectMenuInTopRight("Logout")
            
            # Refresh the page
            do.refresh()
              
            # Log back in
            do.login()
            print "Log in as : " + do.whoAmI()
            last_created_object_link = do.createObject("Program")
            object_name = str(do.util.getTextFromXpathString(last_created_object_link)).strip()
            self.assertTrue(do.partialMatch("program-auto-test", object_name), "Fail to match program name.")
            self.assertEqual(do.whoAmI(), aEmail, "Mismatched. I am: " + do.whoAmI() + ", " + "aEmail: " + aEmail)
            do.selectMenuInTopRight("Logout") 
     
            # Restore old login information
            do.changeUsernameEmail(aName, oldName, aEmail, oldEmail, absFilePath)
          
        
if __name__ == "__main__":
    unittest.main()
