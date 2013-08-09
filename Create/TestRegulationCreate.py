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


class TestRegulationCreate(WebDriverTestCase):
    
    
    def testRegulationCreate(self):
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers()
        do.setUtils(util)
        do.Login()
        self.assertTrue(util.isElementPresent(element.dashboard_title), "no dashboard page found")
        do.OpenCreateNewObjectWindow("Regulation")
        random_number= do.GetTimeId()
        regulation_name = "regulation-auto-test"+random_number
        do.PopulateObjectData(regulation_name)
        do.SaveObjectData()
        do.VerifyObjectIsCreated("Regulation", regulation_name)
        
        
if __name__ == "__main__":
    unittest.main()