'''
Created on June 10, 2014
Create person from the admin dashboard page

@author: ukyo.duong
'''


import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestCreatePeople(WebDriverTestCase):
    
    
    def testContractCreate(self):
        self.testname="TestCreatePeople"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()
        do.selectMenuInTopRight("Admin Dashboard")
        
        
        
if __name__ == "__main__":
    unittest.main()
