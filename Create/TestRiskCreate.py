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


class TestRiskCreate(WebDriverTestCase):
    
    
    def testRiskCreate(self):
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers()
        do.setUtils(util)
        do.Login()
        self.assertTrue(util.isElementPresent(element.dashboard_title), "no dashboard page found")
        do.OpenCreateNewRiskWindow(element.risk_widget_object_add_button)
        random_number= do.GetTimeId()
        risk_name = "risk-auto-test"+random_number
        do.PopulateNewObjectData(risk_name)
        do.SaveObjectData()
        do.WaitForLeftNavToLoad()
        do.VerifyObjectIsCreated("risks", risk_name)
        
        
if __name__ == "__main__":
    unittest.main()