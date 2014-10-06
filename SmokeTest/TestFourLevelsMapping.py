'''
Created on Jul 14, 2014

@author: uduong
'''
import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestFourLevelsMapping(WebDriverTestCase):

    def testFourLevelsMapping(self):
        self.testname="TestFourLevelsMapping"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()

        # mapping and un-mapping up to 3 levels: 
        # Program->Regulation->Section->Object
        titleReg = do.getUniqueString("regulation")
        titlePrgm = do.getUniqueString("program")
        titleSec = do.getUniqueString("section")
        personEmail = "uduong@google.com"
          
        do.createObject("Regulation", titleReg)
        last_created_object_link = do.createObject("Program", titlePrgm)
        do.mapAObjectLHN("Regulation", titlePrgm)  # maps program object
        do.expandItemWidget("Regulation", titleReg)  # expand the item so that "+ Section" link is displayed
        do.createSectionFromInnerNavLink(titleSec)
        do.mapObjectToSectionFromInnerNav(titleSec)
        do.mapObjectFormFilling("People", personEmail)
        do.expandWidget4thTier(personEmail)
        do.unMapObjectFromWidget(True)  # unmap object
        do.deleteObjectFromSectionAfterMapping()
        do.unMapObjectFromWidget(False)  # unmap regulation

if __name__ == "__main__":

    unittest.main()