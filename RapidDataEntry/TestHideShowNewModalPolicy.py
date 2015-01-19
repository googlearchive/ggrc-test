'''
Created on Jan 06, 2015

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
        list_items = "description, note, owner, contact, url, kind_type, reference_url, code, effective_date, stop_date, state"
        a_few_items = "url, kind_type"
 
        print "TEST THAT YOU CAN SHOW OR HIDE FIELDS/ELEMENTS IN CREATE NEW OBJECT MODAL."
        
        # fill in mandatory fields only
        do.openCreateNewObjectWindowFromLhn("Policy")
 
        # hide_all, show_all, then hide individual
        do.hideInNewModal(list_all, True, "policy")
        do.hideInNewModal(list_all, False, "policy")
        
        # hide individually
        do.hideInNewModal(list_items, True)
                
        # show all again, hide a few will cause show_all to display, now reshow_all
        do.hideInNewModal(list_all, False, "policy")
        do.hideInNewModal(a_few_items, True, "policy")
        do.hideInNewModal(list_all, False, "policy")
        
        do.populateNewObjectData(do.generateNameForTheObject("policy"))
        do.saveNewObjectAndWait()
        do.clickOnInfoPageEditLink()
               
        # now start testing hide/show after clicking on the Edit link
        do.hideInNewModal(list_all, True, "policy")
        do.hideInNewModal(list_all, False, "policy")         
        do.hideInNewModal(a_few_items, True, "policy")
        do.hideInNewModal(list_all, False, "policy") 


if __name__ == "__main__":
    unittest.main()