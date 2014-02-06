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
        do = Helpers()
        do.setUtils(util, "Program")
        do.login()
        program_name = "Program for Auto Mapping from LHN"  +do.getTimeId()
        last_created_object_link = do.createObject("Program", program_name)
        #object_name = str(util.getTextFromXpathString(last_created_object_link)).strip() 
        do.navigateToObject("Program",last_created_object_link)
        for obj in grcobject.program_map_to_lhn: 
            do.mapAObjectLHN(obj)
            #util.refreshPage()
       

        
if __name__ == "__main__":
    unittest.main()
