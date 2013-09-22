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


class TestDataAssetMapLHN(WebDriverTestCase):

    
    def testDataAssetMapLHN(self):
        self.testname="TestDataAssetMapLHN"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        grcobject = GRCObject()
        do = Helpers()
        do.setUtils(util)
        do.login()
        system_name = "DataAsset for Auto Mapping from LHN"  +do.getTimeId()
        last_created_object_link = do.createObject("DataAsset", system_name)
        #object_name = str(util.getTextFromXpathString(last_created_object_link)).strip() 
        do.navigateToObject("DataAsset",last_created_object_link)
        for obj in grcobject.data_asset_map_to_lhn: 
            do.mapAObjectLHN(obj)
            util.refreshPage()
       

        
if __name__ == "__main__":
    unittest.main()