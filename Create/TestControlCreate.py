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


class TestControlCreate(WebDriverTestCase):
    
    
    def testControlCreate(self):
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers()
        do.setUtils(util)
        do.Login()
        self.assertTrue(util.isElementPresent(element.dashboard_title), "no dashboard page found")
        do.OpenCreateNewObjectWindow("Control")
        random_number= do.GetTimeId()
        control_name = "control-auto-test"+random_number
        do.PopulateObjectData(control_name)
        do.SaveObjectData()
        do.VerifyObjectIsCreated("Control", control_name)
        
        
if __name__ == "__main__":
    unittest.main()