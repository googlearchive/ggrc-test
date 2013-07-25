'''
Created on Jul 24, 2013

@author: diana.tzinov
'''


import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers


class TestOrgGroupCreate(WebDriverTestCase):
    
    
    def testOrgGroupCreate(self):
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers()
        do.setUtils(util)
        do.Login()
        self.assertTrue(util.isElementPresent(element.dashboard_title), "no dashboard page found")
        do.OpenCreateNewBusinessObjectWindow("OrgGroup")
        random_number= do.GetTimeId()
        org_group_name = "org_group-test"+random_number
        do.PopulateObjectTitle(org_group_name)
        util.clickOn(element.logo) #temporary workaround to refresh the page which will make the title appear (known bug)
        do.WaitForLeftNavToLoad()
        util.clickOn(element.business_object_widget_nav_tabs_org_groups_link)
        do.VerifyObjectIsCreated("org_groups", org_group_name)
        
        
if __name__ == "__main__":
    unittest.main()