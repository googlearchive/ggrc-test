'''
Created on Sep 13, 2013

@author: diana.tzinov
'''


import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers
from helperRecip.GRCObject import GRCObject


class TestRegulationMapLHN(WebDriverTestCase):

    
    def testRegulationMapLHN(self):
        self.testname="TestRegulationMapLHN"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        grcobject = GRCObject()
        do = Helpers(self)
        do.setUtils(util, "Regulation")
        do.login()
        program_name = "Regulation for Auto Mapping from LHN"  +do.getTimeId()
        last_created_object_link = do.createObject("Regulation", program_name)

        for obj in grcobject.regulation_map_to_lhn: 
            do.mapAObjectLHN(obj)
            #util.refreshPage()
       
        # test unmapping
        for obj in grcobject.regulation_map_to_lhn: 
            self.assertTrue(do.unmapAObjectFromWidget(obj))
        
if __name__ == "__main__":
    unittest.main()
