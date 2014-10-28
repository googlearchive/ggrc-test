'''
Created on Jul 17, 2013

@author: diana.tzinov
'''


import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestMapRegulationToSystem(WebDriverTestCase):
    
    
    def testMapRegulationToSystem(self):
        self.testname="TestMapRegulationToSystem"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()

        titleReg = do.getUniqueString("regulation")
        titleSys = do.getUniqueString("system")
        
        do.createObject("Regulation", titleReg)
        do.createObject("System", titleSys)       
        do.mapAObjectLHN("Regulation", titleReg)
        
if __name__ == "__main__":
    unittest.main()
