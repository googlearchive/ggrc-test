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
        # Program->Regulation->Section->Object
        titleReg = do.getUniqueString("regulation")
        titlePrgm = do.getUniqueString("program")
        titleSec = do.getUniqueString("section")
        person = "person" + str(do.getRandomNumber()) + "@gmail.com"
          
        print "Regulation: " + titleReg
        print "Program: " + titlePrgm
        print "Section: " + titleSec
        print "Person: " + person
                    
        do.createPersonLHN(person, person, person)
        do.createObject("Regulation", titleReg)  
        last_created_object_link = do.createObject("Program", titlePrgm)
        do.mapAObjectLHN("Regulation", titleReg)  # maps to a Regulation object
        do.expandItemWidget("Regulation", titleReg)  # expand the item so that "+ Section" link is displayed
        do.createSectionFromInnerNavLink(titleSec)
        do.mapObjectToSectionFromInnerNav(titleSec)
        do.mapObjectFormFilling("People", person)
        do.expandWidget4thTier(person)
        
        # Verification: you don't see person object from Regulation page
        do.navigateToObjectWithSearch(titleReg, "Regulation")
        do.navigateToInnerNavSection("Person")
        do.assertEqual(0, do.countOfAnyObjectInWidget("person"), "Count is not 0 in Widget.")
        do.assertEqual(0, do.countOfAnyObjectInnerNav("person"), "Count is not 0 in InnerNav.")
         
        # Verification: you don't see person object from Program page
        # 1 because the creator is automatically mapped to the program
        do.navigateToObjectWithSearch(titlePrgm, "Program")
        do.navigateToInnerNavSection("Person")
        do.assertEqual(1, do.countOfAnyObjectInWidget("person"), "Count is not 1 in Widget.")
        do.assertEqual(1, do.countOfAnyObjectInnerNav("person"), "Count is not 1 in InnerNav.")  
    
        # Verification: you see person object in Section page
        do.navigateToObjectWithSearch(titleSec, "Section")
        do.navigateToInnerNavSection("Person")
        do.assertEqual(person, do.getTitleFromWidgetList(1, "Section"))
        do.assertEqual(1, do.countOfAnyObjectInWidget("person"), "Count is not 1 in Widget.")
        do.assertEqual(1, do.countOfAnyObjectInnerNav("person"), "Count is not 1 in InnerNav.") 
         
        # Verification: you see section object from People page
        do.uncheckMyWorkBox()        
        do.navigateToObjectWithSearch(person, "Person")
        do.navigateToInnerNavSection("Section")
        do.assertEqual(titleSec, do.getTitleFromWidgetList(1, "Person"))
        do.assertEqual(1, do.countOfAnyObjectInWidget("section"), "Count is not 1 in Widget.")
        do.assertEqual(1, do.countOfAnyObjectInnerNav("section"), "Count is not 1 in InnerNav.") 

        # **** Test making person object relevant and verify its effect **************************
        do.navigateToObjectWithSearch(titleReg, "Regulation")
        
        # Before making it relevant
        do.navigateToInnerNavSection("Person")
        do.assertEqual(0, do.countOfAnyObjectInWidget("person"), "Count is not 0 in Widget.")
        do.assertEqual(0, do.countOfAnyObjectInnerNav("person"), "Count is not 0 in InnerNav.")
        
        do.navigateToInnerNavSection("Section")
        do.expandItemWidget("Section", titleSec)  # expand the item so that "+ Section" link is displayed
        do._searchObjectIn3rdLevelAndClickOnIt(person, True)
        do.expandWidget4thTier(person, True)

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
        do.navigateToObjectWithSearch(person, "Person")
        do.navigateToInnerNavSection("regulation")
        
        title_fr_widget = do.getTitleFromWidgetList(1, "Person")
        do.assertEqual(titleReg, title_fr_widget, "Titles do match.")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()