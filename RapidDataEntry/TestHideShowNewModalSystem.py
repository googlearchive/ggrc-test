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


class TestHideShowNewModalSystem(WebDriverTestCase):

    def testHideShowNewModalSystem(self):
        self.testname="TestHideShowNewModalSystem"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()

        list_all = "all"
        list_items = "description, note, owner, contact, url, reference_url, code, effective_date, stop_date, state, network_zone"
        a_few_items = "url, effective_date, network_zone, code"
 
        print "TEST THAT YOU CAN SHOW OR HIDE FIELDS/ELEMENTS IN CREATE NEW OBJECT MODAL."
        
        # fill in mandatory fields only
        do.openCreateNewObjectWindowFromLhn("System")
 
        # hide_all, show_all, then hide individual
        do.hideInNewModal(list_all, True, "system")
        do.hideInNewModal(list_all, False, "system")
        
        # hide individually
        do.hideInNewModal(list_items, True)
                
        # show all again, hide a few will cause show_all to display, now reshow_all
        do.hideInNewModal(list_all, False, "system")
        do.hideInNewModal(a_few_items, True, "system")
        do.hideInNewModal(list_all, False, "system")
        
        do.populateNewObjectData(do.generateNameForTheObject("system"))
        do.saveNewObjectAndWait()
        do.clickInfoPageEditLink()
               
        # now start testing hide/show after clicking on the Edit link
        do.hideInNewModal(list_all, True, "system")
        do.hideInNewModal(list_all, False, "system")         
        do.hideInNewModal(a_few_items, True, "system")
        do.hideInNewModal(list_all, False, "system") 


if __name__ == "__main__":
    unittest.main()