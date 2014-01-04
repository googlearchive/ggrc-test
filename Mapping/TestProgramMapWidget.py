'''
Created on Sep 10, 2013

@author: diana.tzinov
'''




import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers
from helperRecip.GRCObject import GRCObject


class TestProgramMapWidget(WebDriverTestCase):

    
    def testProgramMapWidget(self):
        self.testname="TestProgramMapWidget"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        grcobject = GRCObject()
        do = Helpers()
        do.setUtils(util)
        do.login()
        program_name = "Program for Auto Mapping from Widget"  +do.getTimeId()
        last_created_object_link = do.createObject("Program", program_name)
        #object_name = str(util.getTextFromXpathString(last_created_object_link)).strip() 
        do.navigateToObject("Program",last_created_object_link)
        for obj in grcobject.program_map_to_widget: 
            do.mapAObjectWidget(obj, True, ("Control"))



if __name__ == "__main__":
    unittest.main()