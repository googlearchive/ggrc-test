'''
Created on Aug 10, 2013

@author: diana.tzinov
'''




import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers
from helperRecip.GRCObject import GRCObject


class TestProcessEdit(WebDriverTestCase):
    
    
    def testProcessEdit(self):
        self.testname="testProcessEdit"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers()
        grcobject = GRCObject()
        do.setUtils(util)
        do.Login()
        last_created_object_link = do.CreateObject("Process")
        object_name = str(util.getTextFromXpathString(last_created_object_link)).strip()
        do.NavigateToObjectAndOpenObjectEditWindow(last_created_object_link)
        do.PopulateObjectInEditWindow( object_name , grcobject.process_elements, grcobject.process_values)
        do.OpenObjectEditWindow()
        do.ShowHiddenValues()
        do.verifyObjectValues(grcobject.process_elements, grcobject.process_values)
        do.deleteObject()
        
if __name__ == "__main__":
    unittest.main()