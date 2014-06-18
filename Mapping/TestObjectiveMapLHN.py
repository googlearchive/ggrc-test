'''
Created on Sep 17, 2013

@author: diana.tzinov
'''


import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers
from helperRecip.GRCObject import GRCObject


class TestObjectiveMapLHN(WebDriverTestCase):

    
    def testObjectiveMapLHN(self):
        self.testname="TestObjectiveMapLHN"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        grcobject = GRCObject()
        do = Helpers(self)
        do.setUtils(util, "Objective")
        do.login()
        program_name = "Objective for Auto Mapping from LHN"  +do.getTimeId()
        last_created_object_link = do.createObject("Objective", program_name)
        #object_name = str(util.getTextFromXpathString(last_created_object_link)).strip() 
        #do.navigateToObjectWithSearch(program_name, "Objective")
        for obj in grcobject.objective_map_to_lhn: 
            do.mapAObjectLHN(obj)
            #util.refreshPage()
       

        
if __name__ == "__main__":
    unittest.main()
