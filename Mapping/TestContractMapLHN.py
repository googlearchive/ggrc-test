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


class TestContractMapLHN(WebDriverTestCase):

    def testContractMapLHN(self):
        self.setup()
        self.testname="TestContractMapLHN"
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        grcobject = GRCObject()
        do = Helpers(self)
        do.setUtils(util, "Contract")
        do.login()
        contract_name = "Contract for Auto Mapping from LHN"  +do.getTimeId()
        last_created_object_link = do.createObject("Contract", contract_name)

        for obj in grcobject.contract_map_to_lhn: 
            do.mapAObjectLHN(obj)
            #util.refreshPage()


if __name__ == "__main__":
    unittest.main()
