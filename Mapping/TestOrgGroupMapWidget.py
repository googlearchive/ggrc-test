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


class TestOrgGroupMapWidget(WebDriverTestCase):

    def testOrgGroupMapWidget(self):
        self.testname="TestOrgGroupMapWidget"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        grcobject = GRCObject()
        do = Helpers(self)
        do.setUtils(util, "OrgGroup")
        do.login()
        org_group_name = "OrgGroup for Auto Mapping from Widget"  +do.getTimeId()
        last_created_object_link = do.createObject("OrgGroup",org_group_name)
        #do.navigateToObjectWithSearch(org_group_name, "OrgGroup")
        for obj in grcobject.org_group_map_to_widget: 
            do.mapAObjectWidget(obj)
            #util.refreshPage()


if __name__ == "__main__":
    unittest.main()
