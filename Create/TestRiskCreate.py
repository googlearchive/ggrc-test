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
        self.testname="TestRiskCreate"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()
        self.assertTrue(util.isElementPresent(element.dashboard_title), "no dashboard page found")
        do.OpenCreateNewRiskWindow(element.risk_widget_object_add_button)
        random_number= do.getTimeId()
        risk_name = "risk-auto-test"+random_number
        do.populateNewObjectData(risk_name)
        do.saveObjectData()
        do.waitForLeftNavToLoad()
        do.verifyObjectIsCreated("risks", risk_name)
        
        
if __name__ == "__main__":
    unittest.main()
