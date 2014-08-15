'''
Created on Jul 29, 2014

@author: uduong

This class will create one instance of each object type.
'''

import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestCreateOneObjectOfEachType(WebDriverTestCase):
      
    def testCreateOneObjectOfEachType(self):
              
        self.testname="TestCreateOneObjectOfEachType"
        self.setup()
        if 'localhost' in config.url:
            util = WebdriverUtilities()
            util.setDriver(self.driver)
            element = Elements()
            do = Helpers(self)
            do.setUtils(util)
            do.login()
            
            do.createObject("Contract")
            do.createObject("Control")
            do.createObject("DataAsset")
            do.createObject("Facility")
            do.createObject("Market")
            do.createObject("Objective")
            do.createObject("OrgGroup")
            do.createObject("Policy")       
            do.createObject("Process")
            do.createObject("Product")       
            do.createObject("Program")        
            do.createObject("Project")       
            do.createObject("Regulation")        
            do.createObject("System")
            do.createObject("Standard")
            do.createObject("Clause")
             
if __name__ == "__main__":
    unittest.main()
