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


class TestSystemCreate(WebDriverTestCase):
    
    
    def testSystemCreate(self):
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers()
        do.setUtils(util)
        do.Login()
        self.assertTrue(util.isElementPresent(element.dashboard_title), "no dashboard page found")
        do.OpenCreateNewObjectWindow("System")
        random_number= do.GetTimeId()
        system_name = "system-test"+random_number
        do.PopulateObjectData(system_name)
        do.SaveObjectData()
        do.VerifyObjectIsCreated("System", system_name)
        
        
if __name__ == "__main__":
    unittest.main()