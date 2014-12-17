'''
Created on Dec 12, 2014

@author: uduong
'''


import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestRelevantStress(WebDriverTestCase):

    def testRelevantStress(self):
        self.testname="TestRelevantStress"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()

        titleContract = do.getUniqueString("contract")
        titleClause = do.getUniqueString("clause")
          
        print "Contract: " + titleContract
        print "Clause: " + titleClause
                       
        # SETUP        
        do.checkMyWorkBox() # show my objects only
        # Make sure we have at least 20 data assets already if not create them
        count = do.countOfAnyObjectLHS("Data")
        diff = 20 - count
        while diff > 0:
            id = do.getRandomNumber()            
            do.createObject("Data", "data_" + str(id))
            diff = diff - 1
            do.delay(5)
           
        # Map 20 data assets to Clause
        do.createObject("Clause", titleClause)   
        expandables = []   
        do.mapAObjectWidget("Data_Asset", "data_", False, expandables, 20)
           
        # Map a clause to contract
        do.createObject("Contract", titleContract)
         
        do.mapAObjectWidget("Clause", titleClause, False, ("Clause"), 1)         
        # expand it

        do.expandItemWidget("Clause", titleClause)
         
        # check the MakeAllRelevant checkbox
        do.makeAllRelevant(True)

        # switch to Data Asset tab
        do.selectInnerNavTab("data_asset")
        do.assertEqual(20, do.countOfAnyObjectInWidget("data_asset"), "Count is not 20 in Data Asset Widget.")
       
        # just select because it will maintain its expanded mode
        do.selectInnerNavTab("clause")  
        
        do.makeAllRelevant(False)
        do.delay(30) # takes time for the unmapping to complete
        
        # switch to Data Asset tab again
        do.selectInnerNavTab("data_asset")
        
        # if MAKE ALL RELEVANT checkbox is deselected, no data asset tab is shown and thus no count is shown either
        do.assertEqual(0, do.countOfAnyObjectInWidget("data_asset"), "Count is not 0 in Data Asset Widget.")


if __name__ == "__main__":
    unittest.main()