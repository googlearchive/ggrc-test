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


class TestHideShowNewModalStandard(WebDriverTestCase):

    def testHideShowNewModalStandard(self):
        self.testname="TestHideShowNewModalStandard"
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
        do.openCreateNewObjectWindowFromLhn("Standard")
 
        # hide_all, show_all, then hide individual
        do.hideInNewModal(list_all, True, "standard")
        do.hideInNewModal(list_all, False, "standard")
        
        # hide individually
        do.hideInNewModal(list_items, True)
                
        # show all again, hide a few will cause show_all to display, now reshow_all
        do.hideInNewModal(list_all, False, "standard")
        do.hideInNewModal(a_few_items, True, "standard")
        do.hideInNewModal(list_all, False, "standard")
        
        do.populateNewObjectData(do.generateNameForTheObject("standard"))
        do.saveNewObjectAndWait()
        do.clickInfoPageEditLink()
               
        # now start testing hide/show after clicking on the Edit link
        do.hideInNewModal(list_all, True, "standard")
        do.hideInNewModal(list_all, False, "standard")         
        do.hideInNewModal(a_few_items, True, "standard")
        do.hideInNewModal(list_all, False, "standard") 


if __name__ == "__main__":
    unittest.main()