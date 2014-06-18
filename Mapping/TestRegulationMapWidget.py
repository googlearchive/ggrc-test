'''
Created on Sep 15, 2013

@author: diana.tzinov
'''




import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers
from helperRecip.GRCObject import GRCObject


class TestRegulationMapWidget(WebDriverTestCase):

    def testRegulationMapWidget(self):
        self.testname="TestRegulationMapWidget"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        grcobject = GRCObject()
        do = Helpers(self)
        do.setUtils(util, "Regulation")
        do.login()
        regulation_name = "Regulation for Auto Mapping from Widget" + do.getTimeId()
        last_created_object_link = do.createObject("Regulation", regulation_name)
        #do.navigateToObjectWithSearch(regulation_name, "Regulation")
        for obj in grcobject.regulation_map_to_widget: 
            do.mapAObjectWidget(obj)
            #util.refreshPage()


if __name__ == "__main__":
    unittest.main()
