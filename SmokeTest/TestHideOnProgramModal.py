'''
Created on Oct 22, 2014

@author: uduong
'''


import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *



class TestHideOnProgramModal(WebDriverTestCase):

    def testHideOnProgramModal(self):
        self.testname="TestHideOnProgramModal"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()
        
        list_all = "all"
        list_items = "description, private, note, owner, contact, url, reference_url, code, effective_date, stop_date, state"

        print "TEST THAT YOU CAN SHOW OR HIDE FIELDS/ELEMENTS ON WORKFLOW MODAL."
        
        do.openCreateNewObjectWindowFromLhn("Program")
        do.hideInProgramNewModal(True, list_all)
        do.hideInProgramNewModal(False, list_all)
        do.hideInProgramNewModal(True, list_items)
        

if __name__ == "__main__":
    unittest.main()