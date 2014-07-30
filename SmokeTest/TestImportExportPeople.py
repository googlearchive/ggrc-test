'''
Created on Jul 24, 2013

@author: ukyo.duong

Description:  Case1: Create a user, export People database and verified that the user is found in the exported file.
              Case2: Create a new user, and append to the file and import it.  Then, verify that it gets in the database.

'''


import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers


class TestImportExportPeople(WebDriverTestCase):
       
    def testImportExportPeople(self):
        self.testname="TestImportExportPeople"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        do = Helpers(self)
        do.setUtils(util)
        do.login()

        # create a person
        number = str(do.getRandomNumber())
        aEmail = "email" + number + "@gmail.com"
        aName =  "name" + number   
        aCompany = "company" + number              
        do.createPersonLHN(aName, aEmail, aCompany)

        do.uncheckMyWorkBox()
        do.navigateToObjectWithSearch(aName, "Person")
        
        print ""
        print "On screen."
        print "User is displayed as : " + aName
        print "Email is displayed as : " + aEmail
        print "Company is displayed as : " + aCompany
        
# export people
        filePath = config.file_download_path + "PEOPLE.csv"
        do.selectMenuInTopRight("Admin Dashboard")
        do.exportFile("people", filePath)
               
        # verify that information in file matched
        self.assertTrue(do.verifyPeopleExportFile(aName, aEmail, aCompany, filePath), "User not found in exported file.")
   
# import people
        # create some data, add it to the import file and upload       
        number = str(do.getRandomNumber())
        aEmail = "emailImport" + number + "@gmail.com"
        aName =  "nameImport" + number   
        aCompany = "companyImport" + number  
        
        print ""
        print "Add this new user info to the import file and upload."
        print "User name: " + aName
        print "Email: " + aEmail
        print "Company: " + aCompany
        userInfo = aName + "," + aEmail + "," + aCompany
        
        # proof: verify that this user never exist in the database
        do.navigateToObjectWithSearchWithNoAssertion(aName, "Person")
        count = do.countOfAnyObjectLHS("Person")
        self.assertEqual(0, count, "User " + aName + " is verified not existed.")
                
        do.appendToFile(userInfo, filePath)
        do.importFile("People", filePath)
        do.refresh()   
        
        # after import, verify that user has been added to the database
        do.navigateToObjectWithSearch(aName, "Person")
        count = do.countOfAnyObjectLHS("Person")
        self.assertEqual(1, count, "User " + aName + " is verified not existed.")
        self.assertEqual(aName, do.getObjectNavWidgetInfo("username"), "User's name " + aName + " is not found in the database.")
        self.assertEqual(aEmail, do.getObjectNavWidgetInfo("email"), "User's email " + aEmail + " is not found in the database.")
        self.assertEqual(aCompany, do.getObjectNavWidgetInfo("company"), "User's company " + aCompany + " is not found in the database.")
        
        print ""
        print "User is imported successfully and found in the database."
        print aName + "," + aEmail + "," + aCompany

if __name__ == "__main__":
    unittest.main()
