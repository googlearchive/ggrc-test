'''
Created on Jul 21, 2013

@author: ukyo.duong

Description:  Validate import file when each import file has different error

'''

import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestImportProcessesValidation(WebDriverTestCase):
          
    def testImportProcessesValidation(self):
        noRow = config.test_db + "PROCESSES_NO_ROW.csv"
        wrongType = config.test_db + "PROCESSES_WRONG_TYPE.csv"
        noTitle = config.test_db + "PROCESSES_NO_TITLE.csv"
        dupTitle = config.test_db + "PROCESSES_DUP_TITLE.csv"
        

        
        self.testname="TestImportProcessesValidation"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        do = Helpers(self)
        do.setUtils(util)
        do.login()

#         do.selectMenuInTopRight("Admin Dashboard")
#         self.assertTrue(do.importFile("Processes", noRow, True), "Fail negative test on file with now data.")   
#          
#         do.selectMenuInTopRight("Admin Dashboard")        
#         self.assertTrue(do.importFile("Processes", wrongType, True), "Fail negative test on file with wrong data type.")
#         self.assertEquals(do.getWrongTypeMessage(),"Type must be \"Processes\"", "Fail to display 'wrong type' message.")
        
        do.selectMenuInTopRight("Admin Dashboard")        
        self.assertTrue(do.importFile("Processes", noRow, True), "Fail negative test on file with no row.")
        
        do.selectMenuInTopRight("Admin Dashboard")        
        self.assertTrue(do.importFile("Processes", noTitle, True), "Fail negative test on file with no title.")
         






        
if __name__ == "__main__":
    unittest.main()
