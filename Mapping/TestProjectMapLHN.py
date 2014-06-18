'''
Created on Sep 21, 2013

@author: diana.tzinov
'''



import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers
from helperRecip.GRCObject import GRCObject


class TestProjectMapLHN(WebDriverTestCase):

    
    def testProjectMapLHN(self):
        self.testname="TestProjectMapLHN"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        grcobject = GRCObject()
        do = Helpers(self)
        do.setUtils(util, "Project")
        do.login()
        system_name = "Project for Auto Mapping from LHN"  +do.getTimeId()
        last_created_object_link = do.createObject("Project", system_name)
        #object_name = str(util.getTextFromXpathString(last_created_object_link)).strip() 
        #do.navigateToObjectWithSearch(system_name, "Project")
        for obj in grcobject.project_map_to_lhn: 
            do.mapAObjectLHN(obj)
            #util.refreshPage()
       

        
if __name__ == "__main__":
    unittest.main()
