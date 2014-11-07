'''
Created on Jul 29, 2014

@author: uduong

This class will create one instance of each object type.
'''

import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestCreateObjectsAsSetupForLocalRun(WebDriverTestCase):
      
    def testCreateObjectsAsSetupForLocalRun(self):
              
        self.testname="TestCreateObjectsAsSetupForLocalRun"
        self.setup()
        if 'localhost' in config.url:
            
                       
            object_list = ["Contract","Control","DataAsset","Facility","Market","Objective","OrgGroup","Policy","Process","Product","Program",
                            "Project","Regulation","System","Standard","Clause"]
            
            util = WebdriverUtilities()
            util.setDriver(self.driver)
            element = Elements()
            do = Helpers(self)
            do.setUtils(util)
            do.login()
            
            for obj in object_list:
                count = 0; #initalize to 0
                currentCount = do.countOfAnyObjectLHS(obj)
                if currentCount < 2:
                    count = 2 - currentCount;
                
                while count > 0:
                    do.createObject(obj)
                    count = count - 1
             
if __name__ == "__main__":
    unittest.main()
