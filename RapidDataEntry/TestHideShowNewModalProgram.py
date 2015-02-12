'''
Created on Nov 4, 2014

@author: uduong
'''
import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestHideShowNewModalProgram(WebDriverTestCase):

    def testHideShowNewModalProgram(self):
        self.testname="TestHideShowNewModalProgram"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()

        list_all = "all"
        list_items = "url, private_program, description, owner, contact,  note, reference_url, code, effective_date, end_date, state"
        a_few_items = "owner, private_program"

        print "TEST THAT YOU CAN SHOW OR HIDE FIELDS/ELEMENTS IN NEW MODAL."
       
        # fill in mandatory fields only
        do.openCreateNewObjectWindowFromLhn("Program")

        # hide_all, show_all, then hide individual
        do.hideInNewModal(list_all, True)
        do.hideInNewModal(list_all, False)
        
        # hide individually
        do.hideInNewModal(list_items, True)
                
        # show all again, hide a few will cause show_all to display, now reshow_all
        do.hideInNewModal(list_all, False)
        do.hideInNewModal(a_few_items, True)
        do.hideInNewModal(list_all, False)
        
        do.populateNewObjectData(do.generateNameForTheObject("program"))
        do.saveNewObjectAndWait()
        do.clickInfoPageEditLink()
               
        # now start testing hide/show after clicking on the Edit link
        do.hideInNewModal(list_all, True, "program")
        do.hideInNewModal(list_all, False, "program")         
        do.hideInNewModal(a_few_items, True, "program")
        do.hideInNewModal(list_all, False, "program") 


if __name__ == "__main__":
    unittest.main()