'''
Created on Jul 17, 2013

@author: diana.tzinov
'''


import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.GRCObject import GRCObject
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestEventLog(WebDriverTestCase):
    
    
    def testEventLog(self):
        self.testname="TestEventLog"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        grcobject = GRCObject()
        do = Helpers(self)
        do.setUtils(util)
        do.login()

        # CREATE PROGRAM
        program_name = "Program_created_from_LHN"  + do.getTimeId()
        object_list = ["Regulation", "Contract", "Policy", "Standard"]
          
        last_created_object_link = do.createObject("Program", program_name)
  
        # MAP SOME OBJECTS
        for obj in object_list: 
            do.mapAObjectLHN(obj, program_name)      
          
        do.selectInnerTabWhichAlreadyPresent("info")        
        do.openObjectEditWindow()
        do.deleteObject()
                
        do.selectMenuInTopRight("Admin Dashboard")
        do.selectMenuItemInnerNavDashBoard("Events")
        
        # when delete an object that has mapping, it automatically unmap and then delete
        self.assertTrue(do.verifyInfoInEventLogTable("unmapped from", 1), "Cannot find 'unmapped from Program' in the Event Log table.")
       
        # 4 times
        # 4 lines of "mapped to" because oothere are 4 mappings from the top
        self.assertTrue(do.verifyInfoInEventLogTable("mapped to", 2), "Cannot find 'map to:row2' in the Event Log table.")
        self.assertTrue(do.verifyInfoInEventLogTable("mapped to", 3), "Cannot find 'map to:row3' in the Event Log table.")
        self.assertTrue(do.verifyInfoInEventLogTable("mapped to", 4), "Cannot find 'map to:row4' in the Event Log table.")
        self.assertTrue(do.verifyInfoInEventLogTable("mapped to", 5), "Cannot find 'map to:row5' in the Event Log table.")
        
        # tests the "by whom" and "when at" fields
        self.assertTrue(do.verifyInfoInEventLogTable("whom", 2), "Cannot find 'whom' in the Event Log table.")
        self.assertTrue(do.verifyInfoInEventLogTable("when", 2), "Cannot find 'when' in the Event Log table.")
        
        # the program created should be logged
        self.assertTrue(do.verifyInfoInEventLogTable(program_name, 6), "Cannot find 'create program' in the Event Log table.")
        
        # verify that Prev and Next buttons work
        self.assertTrue(do.verifyPrevNextOperation(), "Fail verifying Prev and Next buttons.")
        
        
        # CORE-727
        self.assertTrue(do.verifyInfoInEventLogTable("deleted", 1, 5), "Cannot find 'deleted' in the Event Log table.")        

if __name__ == "__main__":
    unittest.main()
