'''
Created on Oct 7, 2014

@author: uduong
'''

import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers
from helperRecip.GRCObject import GRCObject


class TestStandardMapLHN(WebDriverTestCase):
   
    def testStandardMapLHN(self):
        self.testname="TestStandardMapLHN"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        grcobject = GRCObject()
        do = Helpers(self)
        do.setUtils(util, "Standard")
        do.login()
        standard_name = "Standard for Auto Mapping from LHN"  +do.getTimeId()
        last_created_object_link = do.createObject("Standard", standard_name)

        for obj in grcobject.standard_map_to_lhn: 
            do.mapAObjectLHN(obj)
            #util.refreshPage()
       
        # test unmapping
        for obj in grcobject.standard_map_to_lhn: 
            self.assertTrue(do.unmapAObjectFromWidget(obj))


if __name__ == "__main__":
    unittest.main()
