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


class TestProductCreate(WebDriverTestCase):
    
    
    def testProductCreate(self):
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers()
        do.setUtils(util)
        do.Login()
        self.assertTrue(util.isElementPresent(element.dashboard_title), "no dashboard page found")
        do.OpenCreateNewObjectWindow("Product")
        random_number= do.GetTimeId()
        product_name = "product-test"+random_number
        do.PopulateObjectData(product_name)
        do.SaveObjectData()
        do.VerifyObjectIsCreated("Product", product_name)
        
        
if __name__ == "__main__":
    unittest.main()