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


class TestMarketEdit(WebDriverTestCase):
    
    
    def testMarketEdit(self):
        self.testname="testMarketEdit"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers()
        grcobject = GRCObject()
        do.setUtils(util)
        do.Login()
        last_created_object_link = do.CreateObject("Market")
        object_name = str(util.getTextFromXpathString(last_created_object_link)).strip()
        do.NavigateToObjectAndOpenObjectEditWindow(last_created_object_link)
        do.PopulateObjectInEditWindow( object_name , grcobject.market_elements, grcobject.market_values)
        do.OpenObjectEditWindow()
        do.ShowHiddenValues()
        do.verifyObjectValues(grcobject.market_elements, grcobject.market_values)
        do.deleteObject()
        
if __name__ == "__main__":
    unittest.main()