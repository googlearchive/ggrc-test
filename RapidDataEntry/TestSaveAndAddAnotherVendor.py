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


class TestSaveAndAddAnotherVendor(WebDriverTestCase):
    
    
    def testSaveAndAddAnotherVendor(self):
        self.testname="TestSaveAndAddAnotherVendor"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()
        
        object_1_name = do.generateNameForTheObject("Vendor")
        do.delay(10) # count number does not appear right away, weird
        object_2_name = "Vendor_" + str(do.getRandomNumber())
        
        do.ensureLHNSectionExpanded("Vendor")
        count_before = do.countOfAnyObjectLHS("Vendor")
        do.createObjectSaveAddAnother("Vendor", object_1_name, "unchecked", True, "", False)
        do.createObjectSaveAddAnother("Vendor", object_2_name, "unchecked", False, "", True)
        do.clearSearchBoxOnLHS() #clear any text so total count displays
        do.ensureLHNSectionExpanded("Vendor")
        count_after = do.countOfAnyObjectLHS("Vendor")
              
        do.assertEqual(count_after, count_before+2, "Count has not incremented by 1 as expected.") 
               
        print "Object 1: "
        object_1_link = do.verifyObjectIsCreatedinLHN("Vendor", object_1_name)
        do.navigateToObjectAndOpenObjectEditWindow("Vendor",object_1_link)
        do.deleteObject()
        
        print "Object 2: "
        object_2_link = do.verifyObjectIsCreatedinLHN("Vendor", object_2_name)
        do.navigateToObjectAndOpenObjectEditWindow("Vendor",object_2_link)
        do.deleteObject()        
       
        
if __name__ == "__main__":
    unittest.main()

