'''
Created on Jul 14, 2014

@author: uduong
'''
import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.GRCObject import GRCObject
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestCreateUpdateDeleteProgram(WebDriverTestCase):

    def testCreateUpdateDeleteProgram(self):
        self.testname="TestCreateUpdateDeleteProgram"
        grcobject = GRCObject()
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        time.sleep(4);
        do.login()
        
        last_created_object_link = do.createObject("Program")
        object_name = str(do.util.getTextFromXpathString(last_created_object_link)).strip()
        do.navigateToObjectAndOpenObjectEditWindow("Program", last_created_object_link)
        do.populateObjectInEditWindow(object_name , grcobject.program_elements, grcobject.program_values)
        do.openObjectEditWindow()
        do.showHiddenValues()
        do.verifyObjectValues(grcobject.program_elements, grcobject.program_values)
        do.deleteObject()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()