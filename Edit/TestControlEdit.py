'''
Created on Jul 31, 2013

@author: diana.tzinov
'''



import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers
from helperRecip.GRCObject import GRCObject


class TestControlEdit(WebDriverTestCase):
    
    
    def testControlEdit(self):
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers()
        grcobject = GRCObject()
        do.setUtils(util)
        do.Login()
        self.assertTrue(util.isElementPresent(element.dashboard_title), "no dashboard page found")
        do.OpenCreateNewObjectWindow("Control")
        random_number= do.GetTimeId()
        control_name = "control-auto-test"+random_number
        do.PopulateObjectData(control_name)
        do.SaveObjectData()
        util.clickOn(element.logo)  #temporary workaround to refresh the page which will make the title appear (known bug)
        do.WaitForLeftNavToLoad()
        util.clickOn(element.governance_widget_nav_tabs_controls_link)
        do.VerifyObjectIsCreated("controls", control_name)
        do.NavToWidgetInfoPage("controls", control_name)
        do.OpenEditWindow(element.widget_governance_edit_page_edit_link)
        do.PopulateObjectInEditWindow( control_name, grcobject.control_elements, grcobject.control_values)
        do.OpenEditWindow(element.widget_governance_edit_page_edit_link)
        do.ShowHiddenValues()
        do.verifyObjectValues(grcobject.control_elements, grcobject.control_values)
        do.deleteObject()
        
        
if __name__ == "__main__":
    unittest.main()