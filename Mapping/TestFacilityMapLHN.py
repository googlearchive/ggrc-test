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


class TestFacilityMapLHN(WebDriverTestCase):

    
    def testFacilityMapLHN(self):
        self.testname="TestFacilityMapLHN"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        grcobject = GRCObject()
        do = Helpers(self)
        do.setUtils(util, "Facility")
        do.login()
        system_name = "Facility for Auto Mapping from LHN"  +do.getTimeId()
        last_created_object_link = do.createObject("Facility", system_name)
        #object_name = str(util.getTextFromXpathString(last_created_object_link)).strip() 
        #do.navigateToObjectWithSearch(system_name, "Facility")
        for obj in grcobject.facility_map_to_lhn: 
            do.mapAObjectLHN(obj)
            #util.refreshPage()
       

        
if __name__ == "__main__":
    unittest.main()
