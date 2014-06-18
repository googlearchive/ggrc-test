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


class TestPolicyMapWidget(WebDriverTestCase):

    def testPolicyMapWidget(self):
        self.testname="TestRPolicyMapWidget"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        grcobject = GRCObject()
        do = Helpers(self)
        do.setUtils(util, "Policy")
        do.login()
        policy_name = "Policy for Auto Mapping from Widget"  +do.getTimeId()
        last_created_object_link = do.createObject("Policy", policy_name)
        #do.navigateToObjectWithSearch(policy_name, "Policy")
        for obj in grcobject.policy_map_to_widget: 
            do.mapAObjectWidget(obj)
            #util.refreshPage()


if __name__ == "__main__":
    unittest.main()
