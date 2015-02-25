'''
Created on Jan 16, 2015

@author: uduong
'''
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


class TestSaveAndAddAnotherWorkflow(WebDriverTestCase):
    
    
    def testSaveAndAddAnotherWorkflow(self):
        self.testname="TestSaveAndAddAnotherWorkflow"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()
        
        object_1_name = do.generateNameForTheObject("Workflow")
        do.delay(10) # count number does not appear right away, weird
        object_2_name = "Workflow_" + str(do.getRandomNumber())
        
        do.ensureLHNSectionExpanded("Workflow")
        count_before = do.countOfAnyObjectLHS("Workflow")
        do.createObjectSaveAddAnother("Workflow", object_1_name, "unchecked", True, "", False)
        do.createObjectSaveAddAnother("Workflow", object_2_name, "unchecked", False, "", True)
        do.clearSearchBoxOnLHS() #clear any text so total count displays
        do.ensureLHNSectionExpanded("Workflow")
        count_after = do.countOfAnyObjectLHS("Workflow")
              
        do.assertEqual(count_after, count_before+2, "Count has not incremented by 1 as expected.") 
               
        print "Object 1: "
        object_1_link = do.verifyObjectIsCreatedinLHN("Workflow", object_1_name)
        do.navigateToObjectAndOpenObjectEditWindow("Workflow",object_1_link)
        do.deleteObject()
        
        print "Object 2: "
        object_2_link = do.verifyObjectIsCreatedinLHN("Workflow", object_2_name)
        do.navigateToObjectAndOpenObjectEditWindow("Workflow",object_2_link)
        do.deleteObject()        
       
        
if __name__ == "__main__":
    unittest.main()
