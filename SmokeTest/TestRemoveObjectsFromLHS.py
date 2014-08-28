'''
Created on Jul 14, 2014

@author: uduong
'''
import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestRemoveObjectsFromLHS(WebDriverTestCase):


    def testRemoveObjectsFromLHS(self):
        self.testname="TestRemoveObjectsFromLHS"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()

        myObjList = [           
            "Program",
            "OrgGroup",
            "Regulation",
            "Contract",
            "Policy",
            "Control",
            "Objective",
            "Standard",
            "Section",
            "Person",
            "OrgGroup",
            "System",
            "Process",
            "DataAsset",
            "Product",
            "Project",
            "Facility",
            "Market",
            "Audit"]
 
        for obj in myObjList:
            do.deleteObjectsFromHLSMatching("auto", obj, False)




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()