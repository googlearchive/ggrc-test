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
        do.OpenCreateNewGovernanceWindow("Policy")
        random_number= do.GetTimeId()
        policy_name = "policy-auto-test"+random_number
        do.PopulateGovernanceData(policy_name)
        util.clickOn(element.logo)  #temporary workaround to refresh the page which will make the title appear (known bug)
        do.WaitForLeftNavToLoad()
        util.clickOn(element.governance_widget_nav_tabs_policies_link)
        do.VerifyObjectIsCreated("policies", policy_name)
        
        
if __name__ == "__main__":
    unittest.main()