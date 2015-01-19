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


class TestHideShowNewModalPeople(WebDriverTestCase):

    def testHideShowNewModalPeople(self):
        self.testname="TestHideShowNewModalPeople"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()

        list_all = "all"
        list_items = "enabled_user, company"
        a_few_items = "company"
 
        print "TEST THAT YOU CAN SHOW OR HIDE FIELDS/ELEMENTS IN CREATE NEW OBJECT MODAL."
        
        # fill in mandatory fields only
        do.openCreateNewObjectWindowFromLhn("People")
 
        # hide_all, show_all, then hide individual
        do.hideInNewModal(list_all, True, "people")
        do.hideInNewModal(list_all, False, "people")
        
        # hide individually
        do.hideInNewModal(list_items, True)
                
        # show all again, hide a few will cause show_all to display, now reshow_all
        do.hideInNewModal(list_all, False, "people")
        do.hideInNewModal(a_few_items, True, "people")
        do.hideInNewModal(list_all, False, "people")
        
        do.populateNewObjectData(do.generateNameForTheObject("people"))
        do.saveNewObjectAndWait()
        do.clickOnInfoPageEditLink()
               
        # now start testing hide/show after clicking on the Edit link
        do.hideInNewModal(list_all, True, "people")
        do.hideInNewModal(list_all, False, "people")         
        do.hideInNewModal(a_few_items, True, "people")
        do.hideInNewModal(list_all, False, "people") 


if __name__ == "__main__":
    unittest.main()