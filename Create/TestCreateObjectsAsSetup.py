'''
Created on Jul 29, 2014

@author: uduong

This class will create 2 instances of each object type.  Then create 1 instance of each type under other account.  So other tests scripts looking
for objects created by different users can run.

'''

import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *

class TestCreateObjectsAsSetup(WebDriverTestCase):
      
    def testCreateObjectsAsSetup(self):
              
        self.testname="TestCreateObjectsAsSetup"
        self.setup()
           
        object_list = ["Contract","Control","DataAsset","Facility","Market","Objective","OrgGroup","Policy","Process","Product","Program",
                            "Project","Regulation","System","Standard","Clause"]
            
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()
        
        print "First:  Log in as : " + do.whoAmI()    
        for obj in object_list:
            count = 0; #initalize to 0
            currentCount = do.countOfAnyObjectLHS(obj)
            if currentCount < 2:
                count = 2 - currentCount;
                
            while count > 0:
                do.createObject(obj)
                count = count - 1
                
        # now log out and then log in with the new account and try to create a program
        do.selectMenuInTopRight("Logout")
           
        # Refresh the page
        do.refresh()
           
        # Log in with new user and create objects
        # This support other tests scripts checking for objects created by different users, and also object counts update
        do.login(config.creator2, config.same_password)
        print "Second:  Log in as : " + do.whoAmI()
        for obj in object_list:
            do.createObject(obj)
        
        # just create one more to test that contract count differ between "all objects" and "my objects"
        do.createObject("Contract")     
                
                
             
if __name__ == "__main__":
    unittest.main()
