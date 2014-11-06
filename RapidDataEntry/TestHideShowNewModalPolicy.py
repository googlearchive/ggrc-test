'''
Created on Oct 29, 2014

@author: uduong
'''
import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestHideShowNewModalPolicy(WebDriverTestCase):

    def testHideShowNewModalPolicy(self):
        self.testname="TestHideShowNewModalPolicy"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()

        list_all = "all"
        list_items = "description, owner, contact, url, note, reference_url, code, effective_date, end_date, state, kind_type"
        a_few_items = "owner, note"

        print "TEST THAT YOU CAN SHOW OR HIDE FIELDS/ELEMENTS IN NEW MODAL."
       
        # fill in mandatory fields only
        do.openCreateNewObjectWindowFromLhn("Policy")

        # hide_all, show_all, then hide individual
        do.hideInNewModal(list_all, True)
        do.hideInNewModal(list_all, False)
        
        # hide individually
        do.hideInNewModal(list_items, True)
                
        # show all again, hide a few will cause show_all to display, now reshow_all
        do.hideInNewModal(list_all, False)
        do.hideInNewModal(a_few_items, True)
        do.hideInNewModal(list_all, False)
        
        # hide all again
        do.hideInNewModal(list_all, True)


if __name__ == "__main__":
    unittest.main()