'''
Created on Jul 19, 2013

@author: diana.tzinov
'''



import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers
from helperRecip.GRCObject import GRCObject


class TestProgramEdit(WebDriverTestCase):

    
    def testProgramEdit(self):
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        grcobject = GRCObject()
        do = Helpers()
        do.setUtils(util)
        do.Login()
        last_created_object_link = do.CreateObject("Program")
        object_name = str(util.getTextFromXpathString(last_created_object_link)).strip()
        do.NavigateToObjectAndOpenObjectEditWindow("Program",last_created_object_link)
        do.PopulateObjectInEditWindow( object_name , grcobject.program_elements, grcobject.program_values)
        do.OpenObjectEditWindow()
        do.ShowHiddenValues()
        do.verifyObjectValues(grcobject.program_elements, grcobject.program_values)
        do.deleteObject()
        
        
        
if __name__ == "__main__":
    unittest.main()