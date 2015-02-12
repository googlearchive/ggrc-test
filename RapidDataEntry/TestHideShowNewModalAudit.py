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


class TestHideShowNewModalAudit(WebDriverTestCase):

    def testHideShowNewModalAudit(self):
        self.testname="TestHideShowNewModalAudit"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()

        list_all = "all"
        list_items = "description, status, owner, contact, auto_generate, planned_start_date, planned_end_date" \
                     "planned_report_period_from, planned_report_period_to, auditors, audit_firm"
        a_few_items = "auditors, audit_firm"
 
        print "TEST THAT YOU CAN SHOW OR HIDE FIELDS/ELEMENTS IN CREATE NEW OBJECT MODAL."
        
        # fill in mandatory fields only
        do.openCreateNewObjectWindowFromLhn("Audit")
 
        # hide_all, show_all, then hide individual
        do.hideInNewModal(list_all, True, "audit")
        do.hideInNewModal(list_all, False, "audit")
        
        # hide individually
        do.hideInNewModal(list_items, True)
                
        # show all again, hide a few will cause show_all to display, now reshow_all
        do.hideInNewModal(list_all, False, "audit")
        do.hideInNewModal(a_few_items, True, "audit")
        do.hideInNewModal(list_all, False, "audit")
        
        do.populateNewObjectData(do.generateNameForTheObject("audit"))
        do.saveNewObjectAndWait()
        do.clickInfoPageEditLink()
               
        # now start testing hide/show after clicking on the Edit link
        do.hideInNewModal(list_all, True, "audit")
        do.hideInNewModal(list_all, False, "audit")         
        do.hideInNewModal(a_few_items, True, "audit")
        do.hideInNewModal(list_all, False, "audit") 


if __name__ == "__main__":
    unittest.main()