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


class TestHideShowNewModalObjective(WebDriverTestCase):

    def testHideShowNewModalObjective(self):
        self.testname="TestHideShowNewModalObjective"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()

        list_all = "all"
        list_items = "description, note, owner, contact, url, reference_url, code, state"
        a_few_items = "url, state"
 
        print "TEST THAT YOU CAN SHOW OR HIDE FIELDS/ELEMENTS IN CREATE NEW OBJECT MODAL."
        
        # fill in mandatory fields only
        do.openCreateNewObjectWindowFromLhn("Objective")
 
        # hide_all, show_all, then hide individual
        do.hideInNewModal(list_all, True, "objective")
        do.hideInNewModal(list_all, False, "objective")
        
        # hide individually
        do.hideInNewModal(list_items, True)
                
        # show all again, hide a few will cause show_all to display, now reshow_all
        do.hideInNewModal(list_all, False, "objective")
        do.hideInNewModal(a_few_items, True, "objective")
        do.hideInNewModal(list_all, False, "objective")
        
        do.populateNewObjectData(do.generateNameForTheObject("objective"))
        do.saveNewObjectAndWait()
        do.clickOnInfoPageEditLink()
               
        # now start testing hide/show after clicking on the Edit link
        do.hideInNewModal(list_all, True, "objective")
        do.hideInNewModal(list_all, False, "objective")         
        do.hideInNewModal(a_few_items, True, "objective")
        do.hideInNewModal(list_all, False, "objective") 


if __name__ == "__main__":
    unittest.main()