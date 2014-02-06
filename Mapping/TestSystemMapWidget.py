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


class TestSystemMapWidget(WebDriverTestCase):

    
    def testSystemMapWidget(self):
        self.testname="TestSystemMapWidget"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        grcobject = GRCObject()
        do = Helpers()
        do.setUtils(util, "System")
        do.login()
        system_name = "System for Auto Mapping from Widget"  +do.getTimeId()
        last_created_object_link = do.createObject("System",system_name)
        #object_name = str(util.getTextFromXpathString(last_created_object_link)).strip() 
        do.navigateToObject("System",last_created_object_link)
        for obj in grcobject.system_map_to_widget: 
            do.mapAObjectWidget(obj)
            #util.refreshPage()
       

        
if __name__ == "__main__":
    unittest.main()