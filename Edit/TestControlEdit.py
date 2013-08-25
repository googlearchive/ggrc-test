'''
Created on Jul 31, 2013

@author: diana.tzinov
'''



import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers
from helperRecip.GRCObject import GRCObject


class TestControlEdit(WebDriverTestCase):
    
    
    def testControlEdit(self):
        self.testname="testControlEdit"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers()
        grcobject = GRCObject()
        do.setUtils(util)
        do.Login()
        last_created_object_link = do.CreateObject("Control")
        object_name = util.getTextFromXpathString(last_created_object_link)
        do.NavigateToObjectAndOpenObjectEditWindow(last_created_object_link)
        do.PopulateObjectInEditWindow( object_name , grcobject.control_elements, grcobject.control_values)
        do.ShowHiddenValues()
        do.verifyObjectValues( grcobject.control_elements, grcobject.control_values)
        do.deleteObject()
        
        
if __name__ == "__main__":
    unittest.main()