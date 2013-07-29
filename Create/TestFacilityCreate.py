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


class TestFacilityCreate(WebDriverTestCase):
    
    
    def testFacilityCreate(self):
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers()
        do.setUtils(util)
        do.Login()
        self.assertTrue(util.isElementPresent(element.dashboard_title), "no dashboard page found")
        do.OpenCreateNewBusinessObjectWindow("Facility")
        random_number= do.GetTimeId()
        facility_name = "facility-test"+random_number
        do.PopulateObjectData(facility_name)
        do.SaveObjectData()
        util.clickOn(element.logo) #temporary workaround to refresh the page which will make the title appear (known bug)
        do.WaitForLeftNavToLoad()
        util.clickOn(element.business_object_widget_nav_tabs_facilities_link)
        do.VerifyObjectIsCreated("facilities", facility_name)
        
        
if __name__ == "__main__":
    unittest.main()