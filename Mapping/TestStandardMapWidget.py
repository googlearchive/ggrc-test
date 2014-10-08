'''
Created on Oct 7, 2014

@author: uduong
'''


import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.GRCObject import GRCObject
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestStandardMapWidget(WebDriverTestCase):

    def testStandardMapWidget(self):
        self.testname="TestStandardMapWidget"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        grcobject = GRCObject()
        do = Helpers(self)
        do.setUtils(util, "Standard")
        do.login()
        standard_name = "Standard for Auto Mapping from Widget" + do.getTimeId()
        last_created_object_link = do.createObject("Standard", standard_name)

        for obj in grcobject.standard_map_to_widget:
            do.mapAObjectWidget(obj, standard_name, False, ("Section", "Objective", "Control"))
            #util.refreshPage()

if __name__ == "__main__":
    unittest.main()
