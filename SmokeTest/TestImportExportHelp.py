'''
Created on Jan 12, 2015

@author: uduong

Description:  Export a file and and reimport it.

'''


import time
import unittest
import config
from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestImportExportHelp(WebDriverTestCase):
       
    def testImportExportHelp(self):
        self.testname="TestImportExportHelp"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        do = Helpers(self)
        do.setUtils(util)
        do.login()
     
        # export help
        filePath = config.test_db + "HELP.csv"
        do.selectMenuInTopRight("Admin Dashboard")
        do.exportFile("help", filePath)
   
        # import help
        do.importFile("Processes", filePath)

if __name__ == "__main__":
    unittest.main()
