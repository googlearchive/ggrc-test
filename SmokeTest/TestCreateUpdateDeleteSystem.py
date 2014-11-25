'''
Created on Jul 14, 2014

@author: uduong
'''

import unittest

from helperRecip.Elements import Elements
from helperRecip.GRCObject import GRCObject
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *
import time

class TestCreateUpdateDeleteSystem(WebDriverTestCase):

    def testCreateUpdateDeleteSystem(self):
        self.testname="TestCreateUpdateDeleteSystem"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        grcobject = GRCObject()
        do = Helpers(self)
        do.setUtils(util)
        myUtil = do.getUtils()
        do.login()
        
        aEmail = "testrecip@gmail.com" #already exists in the database
        
        last_created_object_link = do.createObject("System")
        object_name = str(do.util.getTextFromXpathString(last_created_object_link)).strip()
        do.navigateToObjectAndOpenObjectEditWindow("System", last_created_object_link)
        do.populateObjectInEditWindow(object_name , grcobject.system_elements, grcobject.system_values, aEmail)
        do.openObjectEditWindow()
        do.verifyObjectValues(grcobject.system_elements, grcobject.system_values)
        do.deleteObject()

if __name__ == "__main__":
    unittest.main()