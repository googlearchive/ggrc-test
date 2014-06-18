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
        #do.navigateToObjectWithSearch(contract_name, "Contract")
        for obj in grcobject.contract_map_to_widget: 
            do.mapAObjectWidget(obj)
            #util.refreshPage()


if __name__ == "__main__":
    unittest.main()
