'''
Created on Sep 5, 2013

@author: diana.tzinov
'''




import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers
from helperRecip.GRCObject import GRCObject


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
          
        # Uncomment these when run this test by itself in standalone or troublshoot session   
        # Objects must exist before mapping can be done 
#         do.createObject("DataAsset")
#         do.createObject("Regulation")
#         do.createObject("Contract")
#         do.createObject("Policy")
#         do.createObject("Standard")
#         do.createObject("Objective")
#         do.createObject("Control")
#         do.createObject("System")
#         do.createObject("Process")              
#         do.createObject("Product")
#         do.createObject("Project")           
#         do.createObject("Facility")
#         do.createObject("Market")
#         do.createObject("Group")            

        last_created_object_link = do.createObject("Program", program_name)
        for obj in grcobject.program_map_to_lhn: 
            do.mapAObjectLHN(obj)
            #util.refreshPage()
       

        
if __name__ == "__main__":
    unittest.main()
