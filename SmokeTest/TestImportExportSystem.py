'''
Created on Jul 24, 2013

@author: ukyo.duong

Description:  Case1: Create a system object, export System database and verified that the system object is found in the export file.
              Case2: Create a new system object, and append to the file and import it.  Then, verify that it gets in the database.

'''


import time
import unittest
import config
from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestImportExportSystem(WebDriverTestCase):
       
    def testImportExportSystem(self):
        self.testname="TestImportExportSystem"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        do = Helpers(self)
        do.setUtils(util)
        do.login()

        # create a system
        systemObject =do.createObject("System")
        systemObject = str(util.getTextFromXpathString(systemObject)) #it's name, not xpath
        
        print ""
        print "On screen."
        print "System object is displayed as : " + systemObject
     
# export system
        filePath = config.test_db + "SYSTEMS.csv"
        do.selectMenuInTopRight("Admin Dashboard")
        do.exportFile("systems", filePath)
               
        # verify that information in file matched
        self.assertTrue(do.verifyDataInExportFile(systemObject, filePath), "System object not found in exported file.")
   
# import system
        # create some data, add it to the import file and upload       
        number = str(do.getRandomNumber())
        systemObject = "systemImport" + number
      
        print ""
        print "Add this new system object to the import file and upload."
        print "System object: " + systemObject
       
        # proof: verify that this user never exist in the database
        do.navigateToObjectWithSearchWithNoAssertion(systemObject, "System")
        count = do.countOfAnyObjectLHS("System")
        self.assertEqual(0, count, "System " + systemObject + " is verified not existed.")
             
        # make it complete     
        conformingText = "SYSTEM-" + number + "," + systemObject + ",,,,,,user@example.com,,,,,,2014-7-16,2014-7-16,,Draft"        
        do.appendToFile(conformingText, filePath)
        
        do.importFile("Systems", filePath)
        do.refresh()   
        
        # after import, verify that user has been added to the database
        do.navigateToObjectWithSearch(systemObject, "System")
        count = do.countOfAnyObjectLHS("System")
        self.assertEqual(1, count, "System " + systemObject + " is not added successfully.")
        self.assertEqual(systemObject, do.getObjectNavWidgetInfo("username"), "System object " + systemObject + " is not found in the database.")

 
        print ""
        print "System object is imported successfully and found in the database."
        print systemObject
 
if __name__ == "__main__":
    unittest.main()
