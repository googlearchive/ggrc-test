'''
Created on Sep 22, 2013

@author: diana.tzinov
'''


import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers
from helperRecip.GRCObject import GRCObject


class TestControlMapLHN(WebDriverTestCase):

    
    def testControlMapLHN(self):
        self.testname="TestControlMapLHN"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        grcobject = GRCObject()
        do = Helpers(self)
        do.setUtils(util, "Control")
        do.login()
        
#         # Uncomment these when run this test by itself in standalone or troubleshoot session   
#         # Objects must exist before mapping can be done 
#         do.createObject("Program")
#         do.createObject("System")
#         do.createObject("Process")
#         do.createObject("Data")             
#         do.createObject("Product")
#         do.createObject("Project")           
#         do.createObject("Facility")
#         do.createObject("Market")
#         do.createObject("Group")   

        
        control_name = "Control for Auto Mapping from LHN"  +do.getTimeId()
        last_created_object_link = do.createObject("Control", control_name)

        for obj in grcobject.control_map_to_lhn: 
            do.mapAObjectLHN(obj)
            #util.refreshPage()
       

        
if __name__ == "__main__":
    unittest.main()
