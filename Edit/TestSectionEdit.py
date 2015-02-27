'''
Created on Jan 22, 2015

@author: uduong
'''

import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers
from helperRecip.GRCObject import GRCObject


class TestSectionEdit(WebDriverTestCase):
    
    
    def testSectionEdit(self):
        self.testname="TestSectionEdit"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        grcobject = GRCObject()
        do.setUtils(util)
        do.login()
        object_name = "Auto_Section_" + do.getTimeId() + str(do.getRandomNumber())
        last_created_object_link = do.createObjectSaveAddAnother("Section", object_name, "unchecked")
        #object_name = str(util.getTextFromXpathString(last_created_object_link)).strip()
        do.navigateToObjectAndOpenObjectEditWindow("Section",last_created_object_link)
        do.populateObjectInEditWindow( object_name , grcobject.section_elements, grcobject.section_values)
        do.openObjectEditWindow()
        do.verifyObjectValues(grcobject.section_elements, grcobject.section_values)
        do.deleteObject()
        
if __name__ == "__main__":
    unittest.main()
