'''
Created on Jul 16, 2013

@author: diana.tzinov
'''


import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers


class TestProgramCreate(WebDriverTestCase):
    
    
    def testProgramCreate(self):
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers()
        do.setUtils(util)
        do.Login()
        self.assertTrue(util.isElementPresent(element.dashboard_title), "no dashboard page found")
        do.OpenCreateNewProgramWindow(element.programs_widget_add_program_button)
        random_number= do.GetTimeId()
        program_name = "program-auto-test"+random_number
        do.PopulateObjectData(program_name)
        do.SaveObjectData()
        do.WaitForLeftNavToLoad()
        do.VerifyObjectIsCreated("programs", program_name)
        
        
if __name__ == "__main__":
    unittest.main()