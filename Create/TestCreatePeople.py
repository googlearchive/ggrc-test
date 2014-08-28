'''
Created on Aug 14, 2013

@author: ukyo.duong

Description: uduong and testrecip are the two users needed when running from local machine
             because those "Edit" test scripts use these them

'''


import time
import unittest
import datetime
from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestCreatePeople(WebDriverTestCase):
       
    def testCreatePeople(self):
        self.testname="TestCreatePeople"
        self.setup()
        
        if 'localhost' in config.url:
        
            util = WebdriverUtilities()
            util.setDriver(self.driver)
            element = Elements()
            do = Helpers(self)
            do.setUtils(util)
            do.login()
    
            entity = "testrecip@gmail.com"
    
            do.selectMenuInTopRight("Admin Dashboard")
            do.selectMenuItemInnerNavDashBoard("People") 
    
            for x in range(3):
    
                if x==1:
                    entity = "uduong@google.com"
                elif x==2:
                    entity = "adam@google.com"
                try:                         
                    self.assertTrue(do.addPersonInAdminDB(entity, entity, entity), "Fail to add person or person already exists")
                    do.refresh()
                    self.assertTrue(do.searchPersonInAdminDB(entity), "Fail searching for newly created person in Admin Dashboard.")
                 
                    # edit person authorization
                    do.selectMenuItemInnerNavDashBoard("People") # on the roles selection      
                    do.clickOnEditAuthorization(entity)
                    do.assignUserRole("gGRC Admin")
                except:
                    do.clickCancelButtonOnAddPersonModal()
                    continue # if it already exist then fine  
        
if __name__ == "__main__":
    unittest.main()
