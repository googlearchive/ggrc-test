'''
Created on Aug 27, 2014

@author: uduong
'''

import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestRelevantMapping(WebDriverTestCase):


    def testRelevantMapping(self):
        self.testname="TestRelevantMapping"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()

        # mapping and un-mapping up to 3 levels: 
        # Program->Policy->Section->Object
        titlePol = do.getUniqueString("policy") #regulation
        titlePrgm = do.getUniqueString("program")
        titleSec = do.getUniqueString("section")
        titleMkt = do.getUniqueString("market")
       
        print "Policy: " + titlePol
        print "Program: " + titlePrgm
        print "Section: " + titleSec
        print "Market: " + titleMkt
                    
        # SETUP
        do.createObject("Market", titleMkt) 
        do.createObject("Policy", titlePol)  
        last_created_object_link = do.createObject("Program", titlePrgm)
        do.mapAObjectLHN("Policy", titlePol)  # maps to a Policy object
        do.expandItemWidget("Policy", titlePol)  # expand the item so that "+ Section" link is displayed
        do.createSectionFromInnerNavLink(titleSec)
        do.mapObjectToSectionFromInnerNav(titleSec)
        do.mapObjectFormFilling("Market", titleMkt)
        do.expandWidget4thTier(titleMkt)
        
        # Policy page
        do.navigateToObjectWithSearch(titlePol, "Policy")
        do.navigateToInnerNavSection("Market")
        do.assertEqual(0, do.countOfAnyObjectInWidget("market"), "Count is not 0 in Widget.")
        do.assertEqual(0, do.countOfAnyObjectInnerNav("market"), "Count is not 0 in InnerNav.")
         
        # Verification: you don't see person object from Program page
        # 1 because the creator is automatically mapped to the program
        do.navigateToObjectWithSearch(titlePrgm, "Program")
        do.navigateToInnerNavSection("Market")
        do.assertEqual(1, do.countOfAnyObjectInWidget("market"), "Count is not 1 in Widget.")
        do.assertEqual(1, do.countOfAnyObjectInnerNav("market"), "Count is not 1 in InnerNav.")  
    
        # Verification: you see Market object in Section page
        do.navigateToObjectWithSearch(titleSec, "Section")
        do.navigateToInnerNavSection("Market")
        do.assertEqual(titleMkt, do.getTitleFromWidgetList(1, "Section"))
        do.assertEqual(1, do.countOfAnyObjectInWidget("market"), "Count is not 1 in Widget.")
        do.assertEqual(1, do.countOfAnyObjectInnerNav("market"), "Count is not 1 in InnerNav.") 
         
        # Verification: you see section object from People page
        do.uncheckMyWorkBox()        
        do.navigateToObjectWithSearch(titleMkt, "Market")
        do.navigateToInnerNavSection("Section")
        do.assertEqual(titleSec, do.getTitleFromWidgetList(1, "Market")) #STOP HERE
        do.assertEqual(1, do.countOfAnyObjectInWidget("section"), "Count is not 1 in Widget.")
        do.assertEqual(1, do.countOfAnyObjectInnerNav("section"), "Count is not 1 in InnerNav.") 

        # **** Test making person object relevant and verify its effect **************************
        do.navigateToObjectWithSearch(titlePol, "Regulation")
        
        # Before making it relevant
        do.navigateToInnerNavSection("Person")
        do.assertEqual(0, do.countOfAnyObjectInWidget("person"), "Count is not 0 in Widget.")
        do.assertEqual(0, do.countOfAnyObjectInnerNav("person"), "Count is not 0 in InnerNav.")
        
        do.navigateToInnerNavSection("Section")
        do.expandItemWidget("Section", titleSec)  # expand the item so that "+ Section" link is displayed
        do._searchObjectIn3rdLevelAndClickOnIt(titleMkt, True)
        do.expandWidget4thTier(titleMkt, True)

        # Verification: you now see person object from Regulation page
        do.navigateToInnerNavSection("Person")
        do.assertEqual(1, do.countOfAnyObjectInWidget("person"), "Count is not 1 in Widget.")
        do.assertEqual(1, do.countOfAnyObjectInnerNav("person"), "Count is not 1 in InnerNav.")

        # Verification: you don't see person object from Program page
        # 1 because the creator is automatically mapped to the program
        do.navigateToObjectWithSearch(titlePrgm, "Program")
        do.navigateToInnerNavSection("Person")
        do.assertEqual(1, do.countOfAnyObjectInWidget("person"), "Count is not 1 in Widget.")
        do.assertEqual(1, do.countOfAnyObjectInnerNav("person"), "Count is not 1 in InnerNav.")  

        # Verification: regulation object appears in the widget on People page
        do.navigateToObjectWithSearch(titleMkt, "Person")
        do.navigateToInnerNavSection("regulation")
        
        title_fr_widget = do.getTitleFromWidgetList(1, "Person")
        do.assertEqual(titlePol, title_fr_widget, "Titles do match.")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()