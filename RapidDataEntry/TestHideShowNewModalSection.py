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


class TestHideShowNewModalSection(WebDriverTestCase):

    def testHideShowNewModalSection(self):
        self.testname="TestHideShowNewModalSection"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()

        list_all = "all"
        list_items = "text_of_section, note, owner, contact, reference_url, code"
        a_few_items = "code, contact"
 
        print "TEST THAT YOU CAN SHOW OR HIDE FIELDS/ELEMENTS IN CREATE NEW OBJECT MODAL."
        
        # fill in mandatory fields only
        do.openCreateNewObjectWindowFromLhn("Section")
 
        # hide_all, show_all, then hide individual
        do.hideInNewModal(list_all, True, "section")
        do.hideInNewModal(list_all, False, "section")
        
        # hide individually
        do.hideInNewModal(list_items, True)
                
        # show all again, hide a few will cause show_all to display, now reshow_all
        do.hideInNewModal(list_all, False, "section")
        do.hideInNewModal(a_few_items, True, "section")
        do.hideInNewModal(list_all, False, "section")
        
        do.populateNewObjectData(do.generateNameForTheObject("section"))
        do.saveNewObjectAndWait()
        do.clickInfoPageEditLink()
               
        # now start testing hide/show after clicking on the Edit link
        do.hideInNewModal(list_all, True, "section")
        do.hideInNewModal(list_all, False, "section")         
        do.hideInNewModal(a_few_items, True, "section")
        do.hideInNewModal(list_all, False, "section") 


if __name__ == "__main__":
    unittest.main()