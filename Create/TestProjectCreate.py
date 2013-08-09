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


class TestProjectCreate(WebDriverTestCase):
    
    
    def testProjectCreate(self):
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers()
        do.setUtils(util)
        do.Login()
        self.assertTrue(util.isElementPresent(element.dashboard_title), "no dashboard page found")
        do.OpenCreateNewObjectWindow("Project")
        random_number= do.GetTimeId()
        project_name = "project-test"+random_number
        do.PopulateObjectData(project_name)
        do.SaveObjectData()
        do.VerifyObjectIsCreated("Project", project_name)
        
        
if __name__ == "__main__":
    unittest.main()