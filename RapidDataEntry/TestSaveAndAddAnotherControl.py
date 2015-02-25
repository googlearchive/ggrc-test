'''
Created on Jan 16, 2015

Description:  This class tests that you can create multiple objects via using the "Save & Add Another" button.

@author: uduong
'''

import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestSaveAndAddAnotherControl(WebDriverTestCase):
    
    
    def testSaveAndAddAnotherControl(self):
        self.testname="TestSaveAndAddAnotherControl"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()
        
        object_1_name = do.generateNameForTheObject("Control")
        do.delay(10) # count number does not appear right away, weird
        object_2_name = "Control_" + str(do.getRandomNumber())
        
        do.ensureLHNSectionExpanded("Control") # need to be expanded to see count
        count_before = do.countOfAnyObjectLHS("Control")
        do.createObjectSaveAddAnother("Control", object_1_name, "unchecked", True, "", False)
        do.createObjectSaveAddAnother("Control", object_2_name, "unchecked", False, "", True)
        do.clearSearchBoxOnLHS() #clear any text so total count displays
        do.ensureLHNSectionExpanded("Control")
        count_after = do.countOfAnyObjectLHS("Control")
              
        do.assertEqual(count_after, count_before+2, "Count has not incremented by 1 as expected.") 
               
        print "Object 1: "
        object_1_link = do.verifyObjectIsCreatedinLHN("Control", object_1_name)
        do.navigateToObjectAndOpenObjectEditWindow("Control",object_1_link)
        do.deleteObject()
        
        print "Object 2: "
        object_2_link = do.verifyObjectIsCreatedinLHN("Control", object_2_name)
        do.navigateToObjectAndOpenObjectEditWindow("Control",object_2_link)
        do.deleteObject()        
       
        
if __name__ == "__main__":
    unittest.main()
