'''
Created on Jul 17, 2013

@author: diana.tzinov
'''


import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers


class TestContractCreate(WebDriverTestCase):
    
    
    def testContractCreate(self):
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers()
        do.setUtils(util)
        do.Login()
        self.assertTrue(util.isElementPresent(element.dashboard_title), "no dashboard page found")
        do.OpenCreateNewObjectWindow("Contract")       
        random_number= do.GetTimeId()
        contract_name = "contract-auto-test"+random_number
        do.PopulateObjectData(contract_name)
        do.SaveObjectData()
        do.VerifyObjectIsCreated("Contract", contract_name)
       
        
if __name__ == "__main__":
    unittest.main()