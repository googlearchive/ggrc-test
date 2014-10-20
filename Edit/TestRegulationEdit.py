'''
Created on Jul 21, 2013

@author: diana.tzinov
'''


import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers
from helperRecip.GRCObject import GRCObject


class TestRegulationEdit(WebDriverTestCase):
    
    
    def testRegulationEdit(self):
        self.testname="TestRegulationEdit"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        grcobject = GRCObject()
        do.setUtils(util)
        do.login()
        last_created_object_link = do.createObject("Regulation")
        object_name = str(util.getTextFromXpathString(last_created_object_link)).strip()
        do.navigateToObjectAndOpenObjectEditWindow("Regulation",last_created_object_link)
        do.populateObjectInEditWindow( object_name , grcobject.regulation_elements, grcobject.regulation_values)
        do.openObjectEditWindow()
        do.verifyObjectValues(grcobject.regulation_elements, grcobject.regulation_values)
        do.deleteObject()
        
        
if __name__ == "__main__":
    unittest.main()
