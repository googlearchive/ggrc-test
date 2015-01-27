'''
Created on Jan 26, 2015

Description:  This script test some general access such as tabs or navigation and help link after login in.

@author: uduong

'''

import time
import unittest
import unittest

from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *

class TestMyWorkPageGeneral(WebDriverTestCase):
       
    def testMyWorkPageGeneral(self):
        self.testname="TestMyWorkPageGeneral"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()

        # add help content
        do.addHelpTitleContent("Help Me", "I will help you.")
        do.clickHelpTopRightCorner()
        do.assertEqual(do.getHelpTitle(), "Help Me", "Fail to get Help title.")
        do.assertEqual(do.getHelpContent(), "Help Me", "Fail to get Help title.")
        
        # open menu
        do.showLHMenu(True)
        # close menu
        do.showLHMenu(False)
        
        



        
if __name__ == "__main__":
    unittest.main()







