'''
Created on Jan 15, 2015

Description:  This class tests that you can create multiple objects via using the "Save & Add Another" button.

@author: uduong
'''

import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestSaveAndAddAnotherContract(WebDriverTestCase):
    
    
    def testSaveAndAddAnotherContract(self):
        self.testname="TestSaveAndAddAnotherContract"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()
        
        object_1_name = do.generateNameForTheObject("Contract")
        do.delay(10) # count number does not appear right away, weird
        object_2_name = "Contract_" + str(do.getRandomNumber())
        
        count_before = do.countOfAnyObjectLHS("Contract")
        do.createObjectSaveAddAnother("Contract", object_1_name, "unchecked", True, "", False)
        do.createObjectSaveAddAnother("Contract", object_2_name, "unchecked", False, "", True)
        count_after = do.countOfAnyObjectLHS("Contract")
              
        do.assertEqual(count_after, count_before+2, "Count has not incremented by 1 as expected.") 
               
        print "Object 1: "
        object_1_link = do.verifyObjectIsCreatedinLHN("Contract", object_1_name)
        do.navigateToObjectAndOpenObjectEditWindow("Contract",object_1_link)
        do.deleteObject()
        
        print "Object 2: "
        object_2_link = do.verifyObjectIsCreatedinLHN("Contract", object_2_name)
        do.navigateToObjectAndOpenObjectEditWindow("Contract",object_2_link)
        do.deleteObject()        
       
        
if __name__ == "__main__":
    unittest.main()
