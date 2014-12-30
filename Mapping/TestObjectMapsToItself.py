'''
Created on Oct 10, 2014

@author: uduong
'''


import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers
from helperRecip.GRCObject import GRCObject


class TestObjectMapsToItself(WebDriverTestCase):
   
    def testObjectMapsToItself(self):
        self.testname="TestObjectMapsToItself"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        grcobject = GRCObject()
        do = Helpers(self)
        do.setUtils(util, "Contract")
        do.login()
        contract_name = "Contract for Auto Mapping from LHN"  +do.getTimeId()
        
        contract_map_to_lhn2 =  ["Contract", "Program"]
        for obj in grcobject.contract_map_to_lhn2:
            last_created_object_link = do.createObject(obj, contract_name)
            do.mapAObjectLHN(obj)
            #util.refreshPage()
       
        # test unmapping
        for obj in grcobject.contract_map_to_lhn: 
            self.assertTrue(do.unmapAObjectFromWidget(obj))


if __name__ == "__main__":
    unittest.main()
