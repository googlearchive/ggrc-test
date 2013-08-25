'''
Created on Aug 21, 2013

@author: diana.tzinov
'''

import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers
from helperRecip.GRCObject import GRCObject


class TestOrgGroupEdit(WebDriverTestCase):
    
    
    def testOrgGroupEdit(self):
        self.testname="testOrgGroupEdit"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers()
        grcobject = GRCObject()
        do.setUtils(util)
        do.Login()
        last_created_object_link = do.CreateObject("OrgGroup")
        object_name = str(util.getTextFromXpathString(last_created_object_link)).strip()
        do.NavigateToObjectAndOpenObjectEditWindow("OrgGroup",last_created_object_link)
        do.PopulateObjectInEditWindow( object_name , grcobject.org_group_elements, grcobject.org_group_values)
        do.OpenObjectEditWindow()
        do.ShowHiddenValues()
        do.verifyObjectValues(grcobject.org_group_elements, grcobject.org_group_values)
        do.deleteObject()
        
        
if __name__ == "__main__":
    unittest.main()