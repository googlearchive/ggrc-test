'''
Created on Sep 22, 2013

@author: diana.tzinov
'''




import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers
from helperRecip.GRCObject import GRCObject


class TestObjectiveMapWidget(WebDriverTestCase):

    def testObjectiveMapWidget(self):
        self.testname="TestObjectiveMapWidget"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        grcobject = GRCObject()
        do = Helpers(self)
        do.setUtils(util, "Objective")
        do.login()
        objective_name = "Objective for Auto Mapping from Widget"  +do.getTimeId()
        last_created_object_link = do.createObject("Objective", objective_name)
        #do.navigateToObjectWithSearch(objective_name, "Objective")
        for obj in grcobject.objective_map_to_widget: 
            do.mapAObjectWidget(obj)
            #util.refreshPage()


if __name__ == "__main__":
    unittest.main()
