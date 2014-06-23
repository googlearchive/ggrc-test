'''
Created on June 10, 2014

@author: ukyo.duong
'''


import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestExportDifferentFile(WebDriverTestCase):
    
    
    def testContractCreate(self):
        self.testname="TestExportDifferentFile"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()
        do.selectMenuInTopRight("Admin Dashboard")
        do.exportFile("System")
        do.exportFile("Process")
        do.exportFile("People")
        do.exportFile("Help")
        
        print ("WARNING:  Need to verify the content manually.")


       
        
if __name__ == "__main__":
    unittest.main()
