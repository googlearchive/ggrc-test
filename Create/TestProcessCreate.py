'''
Created on Jul 23, 2013

@author: diana.tzinov
'''

import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers


class TestProcessCreate(WebDriverTestCase):
    
    
    def testProcessCreate(self):
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers()
        do.setUtils(util)
        do.Login()
        self.assertTrue(util.isElementPresent(element.dashboard_title), "no dashboard page found")
        do.OpenCreateNewObjectWindow("Process")
        random_number= do.GetTimeId()
        process_name = "process-auto-test"+random_number
        do.PopulateObjectData(process_name)
        do.SaveObjectData()
        do.VerifyObjectIsCreated("Process", process_name)
        
        
if __name__ == "__main__":
    unittest.main()