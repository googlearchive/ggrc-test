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


class TestProjectMapWidget(WebDriverTestCase):

    def testProjectMapWidget(self):
        self.testname="TestProjectMapWidget"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        grcobject = GRCObject()
        do = Helpers(self)
        do.setUtils(util, "Project")
        do.login()
        project_name = "Project for Auto Mapping from Widget" + do.getTimeId()
        last_created_object_link = do.createObject("Project",project_name)
        #do.navigateToObjectWithSearch(project_name, "Project")
        for obj in grcobject.project_map_to_widget: 
            do.mapAObjectWidget(obj)
            #util.refreshPage()


if __name__ == "__main__":
    unittest.main()
