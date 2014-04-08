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


class TestPolicyEdit(WebDriverTestCase):
    
    
    def testPolicyEdit(self):
        self.testname="testPolicyEdit"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        grcobject = GRCObject()
        do.setUtils(util)
        do.login()
        last_created_object_link = do.createObject("Policy")
        object_name = str(util.getTextFromXpathString(last_created_object_link)).strip()
        do.navigateToObjectAndOpenObjectEditWindow("Policy",last_created_object_link)
        do.populateObjectInEditWindow( object_name , grcobject.policy_elements, grcobject.policy_values)
        do.openObjectEditWindow()
        do.showHiddenValues()
        do.verifyObjectValues(grcobject.policy_elements, grcobject.policy_values)
        do.deleteObject()
        
if __name__ == "__main__":
    unittest.main()
