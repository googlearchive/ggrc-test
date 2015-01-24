'''
Created on Jan 22, 2015

Description: Has all the related test cases for ProgramOwner role on a private program.

@author: uduong
'''


import time
import unittest
import unittest


from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *
from helperRecip.GRCObject import GRCObject

class TestCreatePrivateProgramOwner(WebDriverTestCase):
    
    
    def testCreatePrivateProgramOwner(self):
        self.testname="TestCreatePrivateProgramOwner"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        grcobject = GRCObject()
        do.setUtils(util)
        do.login()

        email = config.creator1
        password = config.same_password

        private_prgm_1 = do.createPrivateProgramPermission(email, "", "ProgramOwner")       
        print private_prgm_1
        # map any object so that we can check that reader can see
        do.mapAObjectLHN("Contract")
 
        # now log out and then log in with the ProgramEditor user
        do.selectMenuInTopRight("Logout")          
        do.refresh()          
        # Log in with new user
        do.login(email, password)
        print "Log in as : " + do.whoAmI()      
 
        do.assertEquals("ProgramCreator", do.getRoleLabelInTopRight(), "Label does not says 'ProgramCreator'.")
        do.selectMenuInTopRight("My Work")
         
        # verify that user can see program tab and some programs; by seeing counts 
        do.selectInnerNavTab("program")
        count = do.countOfAnyObjectInWidget("Program")
        do.assertGreater(count, 0, "Fail because count is expected to be non-zero if programs indeed exist.")
         
        # and being able to navigate to the expanded program row
        index = do.expandItemWidget("program", private_prgm_1)
        do.clickViewProgram("program", index)
         
        # can see mapped objects
        do.selectInnerNavTab("contract")
        count = do.countOfAnyObjectInWidget("Contract")
        do.assertGreater(count, 0, "Fail because count is expected to be non-zero if programs indeed exist.")         

        # can map an object to program
        do.mapAObjectWidget("Product", "", True, ("Control", "Objective", "System"))

        # map link and edit authorization link should not exist
        do.selectInnerNavTab("person")
        do.assertTrue(do.isMapLinkPresent("person"), "Expect map link present since it's a ProgramOwner role.")
        do.expandItemWidget("Person", email)
        do.assertTrue(do.isEditAuthorizationPresent(), "Expect Edit Authorization link present since it's a ProgramOwner role.")
        
        # can edit info page
        do.selectInnerNavTab("info")
        do.assertTrue(do.isSubmitForReviewPresent(), "Expect Submit For Review link not present since it's a ProgramOwner role.") 
        do.clickOnInfoPageEditLink()
        do.populateObjectInEditWindow(private_prgm_1 , grcobject.program_elements, grcobject.program_values)
        do.openObjectEditWindow()
        do.verifyObjectValues(grcobject.program_elements, grcobject.program_values)   
        do.deleteObject()
   
if __name__ == "__main__":
    unittest.main()