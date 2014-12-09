'''
Created on Dec 8, 2014

@author: uduong
'''


import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers
from helperRecip.GRCObject import GRCObject


class TestVendorEdit(WebDriverTestCase):
    
    
    def testVendorEdit(self):
        self.testname="TestVendorEdit"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        grcobject = GRCObject()
        do.setUtils(util)
        do.login()
        last_created_object_link = do.createObject("Vendor")
        object_name = str(util.getTextFromXpathString(last_created_object_link)).strip()
        do.navigateToObjectAndOpenObjectEditWindow("Vendor",last_created_object_link)
        do.populateObjectInEditWindow( object_name , grcobject.vendor_elements, grcobject.vendor_values)
        do.openObjectEditWindow()
        do.verifyObjectValues(grcobject.vendor_elements, grcobject.vendor_values)
        do.deleteObject()
        
        
if __name__ == "__main__":
    unittest.main()