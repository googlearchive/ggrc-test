'''
Created on Aug 10, 2013

@author: diana.tzinov
'''





import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers
from helperRecip.GRCObject import GRCObject


class TestDataAssetEdit(WebDriverTestCase):
    
    
    def testDataAssetEdit(self):
        self.testname="testDataAssetEdit"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers()
        grcobject = GRCObject()
        do.setUtils(util)
        do.Login()
        last_created_object_link = do.CreateObject("DataAsset")
        object_name = str(util.getTextFromXpathString(last_created_object_link)).strip()
        do.NavigateToObjectAndOpenObjectEditWindow(last_created_object_link)
        do.PopulateObjectInEditWindow( object_name , grcobject.data_asset_elements, grcobject.data_asset_values)
        do.OpenObjectEditWindow()
        do.ShowHiddenValues()
        do.verifyObjectValues(grcobject.data_asset_elements, grcobject.data_asset_values)
        do.deleteObject()
        
if __name__ == "__main__":
    unittest.main()