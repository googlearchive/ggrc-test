'''
Created on Sep 15, 2013

@author: diana.tzinov
'''



import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.GRCObject import GRCObject
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestContractMapWidget(WebDriverTestCase):

    def testContractMapWidget(self):
        self.testname="TestContractMapWidget"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        grcobject = GRCObject()
        do = Helpers(self)
        do.setUtils(util, "Contract")
        do.login()
        contract_name = "Contract for Auto Mapping from Widget" + do.getTimeId()
        last_created_object_link = do.createObject("Contract", contract_name)

        for obj in grcobject.contract_map_to_widget: 
            do.mapAObjectWidget(obj)
            #util.refreshPage()
        
        # unmap from widget
        for obj in grcobject.contract_map_to_widget: 
            do.unmapAnObjectFromWidget(obj, contract_name)
            
            
        


if __name__ == "__main__":
    unittest.main()
