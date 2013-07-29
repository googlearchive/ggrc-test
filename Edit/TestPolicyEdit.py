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
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers()
        grcobject = GRCObject()
        do.setUtils(util)
        do.Login()
        self.assertTrue(util.isElementPresent(element.dashboard_title), "no dashboard page found")
        do.OpenCreateNewGovernanceWindow("Policy")
        random_number= do.GetTimeId()
        policy_name = "policy-auto-test"+random_number
        do.PopulateObjectData(policy_name)
        do.SaveObjectData()
        util.clickOn(element.logo)  #temporary workaround to refresh the page which will make the title appear (known bug)
        do.WaitForLeftNavToLoad()
        util.clickOn(element.governance_widget_nav_tabs_policies_link)
        object_name=do.VerifyObjectIsCreated("policies", policy_name)
        do.NavToWidgetInfoPage("policies",policy_name)
        do.OpenEditWindow(element.widget_governance_edit_page_edit_link)
        do.PopulateObjectInEditWindow( policy_name, grcobject.policy_elements, grcobject.policy_values)
        do.OpenEditWindow(element.widget_governance_edit_page_edit_link)
        do.ShowHiddenValues()
        do.verifyObjectValues(grcobject.policy_elements, grcobject.policy_values)
        
if __name__ == "__main__":
    unittest.main()