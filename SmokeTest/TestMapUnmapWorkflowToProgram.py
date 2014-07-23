'''
Created on Jul 14, 2014

@author: uduong
'''

import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestMapUnmapWorkflowToProgram(WebDriverTestCase):

    def testMapUnmapWorkflowToProgram(self):
        self.testname="TestMapUnmapWorkflowToProgram"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()

# map workflow (instead of audit)  to -> program
        titleWF = do.getUniqueString("workflow")
        titlePrgm = do.getUniqueString("program")
        
        do.createObject("Workflow", titleWF)
        do.createObject("Program", titlePrgm)     
        #do.navigateToObjectWithSearch(titlePrgm, "Program")
        do.mapAObjectLHN("Workflow", titleWF)    
 
# unmap workflow <-- from program
        self.assertTrue(do.unmapAObjectFromWidget("workflow"), "Fail unmapping Workflow from Program")
        
if __name__ == "__main__":
    unittest.main()