'''
Created on Jul 18, 2013

@author: diana.tzinov
'''


import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers


class TestPolicyCreate(WebDriverTestCase):
    
    
    def testPolicyCreate(self):
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers()
        do.setUtils(util)
        do.Login()
        self.assertTrue(util.isElementPresent(element.dashboard_title), "no dashboard page found")
        do.OpenCreateNewObjectWindow("Policy")
        random_number= do.GetTimeId()
        policy_name = "policy-auto-test"+random_number
        do.PopulateObjectData(policy_name)
        do.SaveObjectData()
        do.VerifyObjectIsCreated("Policy", policy_name)
        
        
if __name__ == "__main__":
    unittest.main()