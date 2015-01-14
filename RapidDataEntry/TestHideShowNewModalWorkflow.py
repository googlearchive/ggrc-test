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


class TestHideShowNewModalWorkflow(WebDriverTestCase):

    def testHideShowNewModalWorkflow(self):
        self.testname="TestHideShowNewModalWorkflow"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()

        list_all = "all"
        list_items = "description, note, owner, frequency, email_preferences, first_task_groups_title, custom_email_message"
        a_few_items = "first_task_groups_title, custom_email_message"
 
        print "TEST THAT YOU CAN SHOW OR HIDE FIELDS/ELEMENTS IN CREATE NEW OBJECT MODAL."
        
        # fill in mandatory fields only
        do.openCreateNewObjectWindowFromLhn("Workflow")
 
        # hide_all, show_all, then hide individual
        do.hideInNewModal(list_all, True, "workflow")
        do.hideInNewModal(list_all, False, "workflow")
        
        # hide individually
        do.hideInNewModal(list_items, True)
                
        # show all again, hide a few will cause show_all to display, now reshow_all
        do.hideInNewModal(list_all, False, "workflow")
        do.hideInNewModal(a_few_items, True, "workflow")
        do.hideInNewModal(list_all, False, "workflow")
        
        # hide all again
        do.hideInNewModal(list_all, True, "workflow")


if __name__ == "__main__":
    unittest.main()