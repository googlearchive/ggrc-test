'''
Created on Jan 19, 2015

Description: Has all the related test cases for ProgramReader role on a private program.

@author: uduong
'''
import time
import unittest
import unittest

from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestCreatePrivateProgramReader(WebDriverTestCase):
    
    
    def testCreatePrivateProgramReader(self):
        self.testname="TestCreatePrivateProgramReader"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()

        email = config.reader1
        password = config.same_password
 
        private_prgm_1 = do.createPrivateProgramPermission(email, "", "ProgramReader")       
        print private_prgm_1
 
        # now log out and then log in with the ProgramReader user
        do.selectMenuInTopRight("Logout")          
        do.refresh()          
        # Log in with new user
        do.login(email, password)
        print "Log in as : " + do.whoAmI()      

        do.assertEquals("Reader", do.getRoleLabelInTopRight(), "Label does not says 'Reader'.")
        do.selectMenuInTopRight("My Work")
        
        # verify that user can see program tab and some programs; by seeing counts 
        do.selectInnerNavTab("program")
        count = do.countOfAnyObjectInWidget("Program")
        do.assertGreater(count, 0, "Fail because count is expected to be non-zero if programs indeed exist.")
        
        # and being able to navigate to the expanded program row
        index = do.expandItemWidget("program", private_prgm_1)
        do.clickViewProgram("program", index)
        
        # map link and edit authorization link should not exist
        do.selectInnerNavTab("person")
        do.assertFalse(do.isMapLinkPresent("person"), "Expect map link not present since it's a ProgramReader role.")
        do.assertFalse(do.isEditAuthorizationPresent(), "Expect Edit Authorization link not present since it's a ProgramReader role.")
                
        # go to program info page        
        do.selectInnerNavTab("program")
        do.assertFalse(do.isInfoPageEditLinkPresent(), "Expect Edit link not present since it's a ProgramReader role.") 
        do.assertFalse(do.isSubmitForReviewPresent(), "Expect Submit For Review link not present since it's a ProgramReader role.")         

        # cannot delete of course because reader can't even see Edit link
        
if __name__ == "__main__":
    unittest.main()