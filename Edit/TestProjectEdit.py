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


class TestProjectEdit(WebDriverTestCase):
    
    
    def testProjectEdit(self):
        self.testname="testProjectEdit"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers()
        grcobject = GRCObject()
        do.setUtils(util)
        do.login()
        last_created_object_link = do.createObject("Project")
        object_name = str(util.getTextFromXpathString(last_created_object_link)).strip()
        do.navigateToObjectAndOpenObjectEditWindow("Project",last_created_object_link)
        do.populateObjectInEditWindow( object_name , grcobject.project_elements, grcobject.project_values)
        do.openObjectEditWindow()
        #do.showHiddenValues()
        do.verifyObjectValues(grcobject.project_elements, grcobject.project_values)
        do.deleteObject()
        
if __name__ == "__main__":
    unittest.main()