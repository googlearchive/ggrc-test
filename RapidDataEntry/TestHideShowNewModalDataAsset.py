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


class TestHideShowNewModalDataAsset(WebDriverTestCase):

    def testHideShowNewModalDataAsset(self):
        self.testname="TestHideShowNewModalDataAsset"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()

        list_all = "all"
        list_items = "description, note, owner, contact, url, reference_url, code, effective_date, stop_date, state"
        a_few_items = "url"
 
        print "TEST THAT YOU CAN SHOW OR HIDE FIELDS/ELEMENTS IN CREATE NEW OBJECT MODAL."
        
        # fill in mandatory fields only
        do.openCreateNewObjectWindowFromLhn("DataAsset")
 
        # hide_all, show_all, then hide individual
        do.hideInNewModal(list_all, True, "DataAsset")
        do.hideInNewModal(list_all, False, "DataAsset")
        
        # hide individually
        do.hideInNewModal(list_items, True)
                
        # show all again, hide a few will cause show_all to display, now reshow_all
        do.hideInNewModal(list_all, False, "DataAsset")
        do.hideInNewModal(a_few_items, True, "DataAsset")
        do.hideInNewModal(list_all, False, "DataAsset")
        
        do.populateNewObjectData(do.generateNameForTheObject("DataAsset"))
        do.saveNewObjectAndWait()
        do.clickInfoPageEditLink()
               
        # now start testing hide/show after clicking on the Edit link
        do.hideInNewModal(list_all, True, "DataAsset")
        do.hideInNewModal(list_all, False, "DataAsset")         
        do.hideInNewModal(a_few_items, True, "DataAsset")
        do.hideInNewModal(list_all, False, "DataAsset") 


if __name__ == "__main__":
    unittest.main()