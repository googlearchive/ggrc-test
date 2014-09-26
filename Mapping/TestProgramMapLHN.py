'''
Created on Sep 5, 2013

@author: diana.tzinov
'''




import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.GRCObject import GRCObject
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestProgramMapLHN(WebDriverTestCase):

    
    def testProgramMapLHN(self):

        
        self.testname="TestProgramMapLHN"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        grcobject = GRCObject()
        do = Helpers(self)
        do.setUtils(util, "Program")
        do.login()
        program_name = "Program for Auto Mapping from LHN"  +do.getTimeId()

        last_created_object_link = do.createObject("Program", program_name)

        for obj in grcobject.program_map_to_lhn: 
            do.mapAObjectLHN(obj, program_name)
       
        # test unmapping
        for obj in grcobject.program_map_to_lhn: 
            self.assertTrue(do.unmapAObjectFromWidget(obj))
        
if __name__ == "__main__":
    unittest.main()
