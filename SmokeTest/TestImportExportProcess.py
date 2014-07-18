'''
Created on Jul 24, 2013

@author: ukyo.duong

Description:  Case1: Create a process object, export Process database and verified that the process object is found in the export file.
              Case2: Create a new process object, and append to the file and import it.  Then, verify that it gets in the database.

'''


import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestImportExportProcess(WebDriverTestCase):
       
    def testImportExportProcess(self):
        self.testname="TestImportExportProcess"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        do = Helpers(self)
        do.setUtils(util)
        do.login()

        # create a process
        processObject =do.createObject("Process")
        processObject = str(util.getTextFromXpathString(processObject)) #it's name, not xpath
        
        print ""
        print "On screen."
        print "Process object is displayed as : " + processObject
     
# export process
        filePath = config.fileDownloadPath + "PROCESSES.csv"
        do.selectMenuInTopRight("Admin Dashboard")
        do.exportFile("processes", filePath)
               
        # verify that information in file matched
        self.assertTrue(do.verifyDataInExportFile(processObject, filePath), "Process object not found in exported file.")
   
# import process
        # create some data, add it to the import file and upload       
        number = str(do.getRandomNumber())
        processObject = "processImport" + number
      
        print ""
        print "Add this new system object to the import file and upload."
        print "Process object: " + processObject
       
        # proof: verify that this user never exist in the database
        do.navigateToObjectWithSearchWithNoAssertion(processObject, "Process")
        count = do.countOfAnyObjectLHS("Process")
        self.assertEqual(0, count, "Process " + processObject + " is verified not existed.")
             
        # make it complete     
        conformingText = "PROCESS-" + number + "," + processObject + ",,,,,,user@example.com,,,,,,2014-7-17,2014-7-17,,Draft"        
        do.appendToFile(conformingText, filePath)
        
        do.importFile("Processes", filePath)
        do.refresh()   
        
        # after import, verify that user has been added to the database
        do.navigateToObjectWithSearch(processObject, "Process")
        count = do.countOfAnyObjectLHS("Process")
        self.assertEqual(1, count, "Process " + processObject + " is not added successfully.")
        self.assertEqual(processObject, do.getObjectNavWidgetInfo("username"), "Process object " + processObject + " is not found in the database.")
 
        print ""
        print "Process object is imported successfully and found in the database."
        print processObject
 
if __name__ == "__main__":
    unittest.main()
