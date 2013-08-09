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


class TestContractEdit(WebDriverTestCase):
    
    
    def testContractEdit(self):
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers()
        grcobject = GRCObject()
        do.setUtils(util)
        do.Login()
        self.assertTrue(util.isElementPresent(element.dashboard_title), "no dashboard page found")
        do.OpenCreateNewObjectWindow("Contract")
        random_number= do.GetTimeId()
        contract_name = "contract-auto-test"+random_number
        do.PopulateObjectData(contract_name)
        do.SaveObjectData()
        util.clickOn(element.logo)  #temporary workaround to refresh the page which will make the title appear (known bug)
        do.WaitForLeftNavToLoad()
        util.clickOn(element.governance_widget_nav_tabs_contracts_link)
        link_to_the_object=do.VerifyObjectIsCreated("contracts", contract_name)
        do.NavToWidgetInfoPage("contracts",contract_name )
        do.OpenEditWindow(element.widget_governance_edit_page_edit_link)
        do.PopulateObjectInEditWindow( contract_name, grcobject.contract_elements, grcobject.contract_values)
        do.OpenEditWindow(element.widget_governance_edit_page_edit_link)
        do.ShowHiddenValues()
        do.verifyObjectValues(grcobject.contract_elements, grcobject.contract_values)
        do.deleteObject()
        
        
if __name__ == "__main__":
    unittest.main()