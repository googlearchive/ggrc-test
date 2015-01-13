'''
Created on Jan 12, 2015

@author: uduong
'''

import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestHideShowNewModalProduct(WebDriverTestCase):

    def testHideShowNewModalProduct(self):
        self.testname="TestHideShowNewModalProduct"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()

        list_all = "all"
        list_items = "description, note, owner, contact, url, reference_url, code, effective_date, stop_date, state"
        a_few_items = "url, effective_date, stop_date, state"
 
        print "TEST THAT YOU CAN SHOW OR HIDE FIELDS/ELEMENTS IN CREATE NEW OBJECT MODAL."
        
        # fill in mandatory fields only
        do.openCreateNewObjectWindowFromLhn("Product")
 
        # hide_all, show_all, then hide individual
        do.hideInNewModal(list_all, True, "product")
        do.hideInNewModal(list_all, False, "product")
        
        # hide individually
        do.hideInNewModal(list_items, True)
                
        # show all again, hide a few will cause show_all to display, now reshow_all
        do.hideInNewModal(list_all, False, "product")
        do.hideInNewModal(a_few_items, True, "product")
        do.hideInNewModal(list_all, False, "product")
        
        # hide all again
        do.hideInNewModal(list_all, True, "product")


if __name__ == "__main__":
    unittest.main()