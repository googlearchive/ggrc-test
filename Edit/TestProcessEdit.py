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
        self.testname="TestProcessEdit"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        grcobject = GRCObject()
        do.setUtils(util)
        do.login()
        last_created_object_link = do.createObject("Process")
        object_name = str(util.getTextFromXpathString(last_created_object_link)).strip()
        do.navigateToObjectAndOpenObjectEditWindow("Process",last_created_object_link)
        do.populateObjectInEditWindow( object_name , grcobject.process_elements, grcobject.process_values)
        do.openObjectEditWindow()
        do.verifyObjectValues(grcobject.process_elements, grcobject.process_values)
        do.deleteObject()
        
if __name__ == "__main__":
    unittest.main()
