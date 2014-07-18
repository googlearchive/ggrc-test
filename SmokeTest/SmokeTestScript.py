
'''
Created on May 01, 2014

@author: ukyo.duong
'''

import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.GRCObject import GRCObject
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


myUtil = 0

class SmokeTestScript(WebDriverTestCase):
    
    
    
    def SmokeTestScript(self):
        self.testname="SmokeTestScript"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        grcobject = GRCObject()
        do = Helpers(self)
        do.setUtils(util)
        do.login()

# verify that all tabs on left hand navigation exist

        self.assertEqual("Programs", self._returnStringUpToFirstSpace(do.util.getTextFromXpathString(element.left_nav_expand_object_section_link.replace("OBJECT", "Program"))))
        self.assertEqual("Audits", self._returnStringUpToFirstSpace(do.util.getTextFromXpathString(element.left_nav_expand_object_section_link.replace("OBJECT", "Audit"))))
        self.assertEqual("Regulations", self._returnStringUpToFirstSpace(do.util.getTextFromXpathString(element.left_nav_expand_object_section_link.replace("OBJECT", "Regulation"))))
        self.assertEqual("Policies", self._returnStringUpToFirstSpace(do.util.getTextFromXpathString(element.left_nav_expand_object_section_link.replace("OBJECT", "Policy"))))
        self.assertEqual("Standards", self._returnStringUpToFirstSpace(do.util.getTextFromXpathString(element.left_nav_expand_object_section_link.replace("OBJECT", "Standard"))))
        self.assertEqual("Contracts", self._returnStringUpToFirstSpace(do.util.getTextFromXpathString(element.left_nav_expand_object_section_link.replace("OBJECT", "Contract"))))
        self.assertEqual("Clauses", self._returnStringUpToFirstSpace(do.util.getTextFromXpathString(element.left_nav_expand_object_section_link.replace("OBJECT", "Clause"))))
        self.assertEqual("Sections", self._returnStringUpToFirstSpace(do.util.getTextFromXpathString(element.left_nav_expand_object_section_link.replace("OBJECT", "Section"))))
        self.assertEqual("Objectives", self._returnStringUpToFirstSpace(do.util.getTextFromXpathString(element.left_nav_expand_object_section_link.replace("OBJECT", "Objective"))))
        self.assertEqual("Controls", self._returnStringUpToFirstSpace(do.util.getTextFromXpathString(element.left_nav_expand_object_section_link.replace("OBJECT", "Control"))))
        self.assertEqual("People", self._returnStringUpToFirstSpace(do.util.getTextFromXpathString(element.left_nav_expand_object_section_link.replace("OBJECT", "Person"))))              
        self.assertEqual("Org Groups", do.util.getTextFromXpathString(element.left_nav_org_group_link)[0:10])
        self.assertEqual("Systems", self._returnStringUpToFirstSpace(do.util.getTextFromXpathString(element.left_nav_expand_object_section_link.replace("OBJECT", "System"))))
        self.assertEqual("Processes", self._returnStringUpToFirstSpace(do.util.getTextFromXpathString(element.left_nav_expand_object_section_link.replace("OBJECT", "Process"))))
        self.assertEqual("Data Assets", do.util.getTextFromXpathString(element.left_nav_data_asset_link)[0:11])
        self.assertEqual("Products", self._returnStringUpToFirstSpace(do.util.getTextFromXpathString(element.left_nav_expand_object_section_link.replace("OBJECT", "Product"))))
        self.assertEqual("Projects", self._returnStringUpToFirstSpace(do.util.getTextFromXpathString(element.left_nav_expand_object_section_link.replace("OBJECT", "Project"))))
        self.assertEqual("Facilities", self._returnStringUpToFirstSpace(do.util.getTextFromXpathString(element.left_nav_expand_object_section_link.replace("OBJECT", "Facility"))))
        self.assertEqual("Markets", do.util.getTextFromXpathString(element.left_nav_market_link)[0:7])
        self.assertEqual("Risk Assessments", do.util.getTextFromXpathString(element.left_nav_risk_assessment_link)[0:16])
        self.assertEqual("Threats", self._returnStringUpToFirstSpace(do.util.getTextFromXpathString(element.left_nav_expand_object_section_link.replace("OBJECT", "Threat"))))
        self.assertEqual("Vulnerabilities", self._returnStringUpToFirstSpace(do.util.getTextFromXpathString(element.left_nav_expand_object_section_link.replace("OBJECT", "Vulnerability"))))
        self.assertEqual("Templates", self._returnStringUpToFirstSpace(do.util.getTextFromXpathString(element.left_nav_expand_object_section_link.replace("OBJECT", "Template"))))
        
# verify create, update, delete
        last_created_object_link = do.createObject("Program")
        object_name = str(do.util.getTextFromXpathString(last_created_object_link)).strip()
        do.navigateToObjectAndOpenObjectEditWindow("Program", last_created_object_link)
        do.populateObjectInEditWindow(object_name , grcobject.program_elements, grcobject.program_values)
        do.openObjectEditWindow()
        do.showHiddenValues()
        do.verifyObjectValues(grcobject.program_elements, grcobject.program_values)
        do.deleteObject()
        time.sleep(10)     
        last_created_object_link = do.createObject("Regulation")
        object_name = str(do.util.getTextFromXpathString(last_created_object_link)).strip()
        do.navigateToObjectAndOpenObjectEditWindow("Regulation", last_created_object_link)
        do.populateObjectInEditWindow(object_name , grcobject.regulation_elements, grcobject.regulation_values)
        do.openObjectEditWindow()
        do.showHiddenValues()
        do.verifyObjectValues(grcobject.regulation_elements, grcobject.regulation_values)
        do.deleteObject()
        time.sleep(10)    
        last_created_object_link = do.createObject("System")
        object_name = str(do.util.getTextFromXpathString(last_created_object_link)).strip()
        do.navigateToObjectAndOpenObjectEditWindow("System", last_created_object_link)
        do.populateObjectInEditWindow(object_name , grcobject.system_elements, grcobject.system_values, "testrecip@gmail.com")
        do.openObjectEditWindow()
        do.showHiddenValues()
        do.verifyObjectValues(grcobject.system_elements, grcobject.system_values)
        do.deleteObject()
        time.sleep(10)  

# mapping and un-mapping up to 3 levels: 

        # Program->Regulation->Section->Object
        titleReg = do.getUniqueString("regulation")
        titlePrgm = do.getUniqueString("program")
        titleSec = do.getUniqueString("section")
        personEmail = "uduong@google.com"
          
        do.createObject("Regulation", titleReg)
        last_created_object_link = do.createObject("Program", titlePrgm)
        do.mapAObjectLHN("Regulation", titleReg)  # maps to a Regulation object
        do.expandItemWidget("Regulation", titleReg)  # expand the item so that "+ Section" link is displayed
        do.createSectionFromInnerNavLink(titleSec)
        do.mapObjectToSectionFromInnerNav(titleSec)
        do.mapObjectFormFilling("People", personEmail)
        do.expandWidget4thTier(personEmail)
        do.unMapObjectFromWidget(True)  # unmap object
        do.deleteObjectFromSectionAfterMapping()
        do.unMapObjectFromWidget(False)  # unmap regulation
 
# map regulation to -> system
        titleSys = do.getUniqueString("system")
        do.createObject("System", titleSys)
        do.mapAObjectLHN("Regulation", titleReg)
         
# map system to -> people
        aEmail = "auto_email_" + str(do.getRandomNumber(65535)) + "@gmail.com"
        aName = do.getUniqueString("name")
        aCompany = do.getUniqueString("company")
        
        do.createPersonLHN(aName, aEmail, aCompany)
 
# map workflow (instead of audit)  to -> program
        titleWF = do.getUniqueString("workflow")
        do.createObject("Workflow", titleWF)     
        do.navigateToObjectWithSearch(titlePrgm, "Program")
        do.mapAObjectLHN("Workflow", titleWF)    
 
# unmap workflow <-- from program
        self.assertTrue(do.unmapAObjectFromWidget("workflow"), "Fail unmapping Workflow from Program")
 
# event log
        do.selectMenuInTopRight("Admin Dashboard")
        do.selectMenuItemInnerNavDashBoard("Events")
        do.verifyInfoInEventLogTable(titleWF + " unmapped from " + titlePrgm, 0)
        do.verifyInfoInEventLogTable(titleWF + " mapped to " + titlePrgm, 1)
 
# create person in Admin Dashboard
        aEmail = "auto_email_" + str(do.getRandomNumber(65535)) + "@gmail.com"
        aName = do.getUniqueString("name")
        aCompany = do.getUniqueString("company")
 
        do.addPersonInAdminDB(aName, aEmail, aCompany)
        self.assertTrue(do.searchPersonInAdminDB(aName), "newly added person named \"" + aName + "\" is not found.")
        
# add role in Admin Dashboard
        do.selectMenuItemInnerNavDashBoard("Roles") # on the roles selection
        count_before = do.roleCount()
        do.createRoleInAdminDB("readingOnly", "this role can read only")
        count_after = do.roleCount()
        self.assertEquals(count_after, count_before+1, "Role count has not incremented.")

# edit person authorization
        do.selectMenuItemInnerNavDashBoard("People") # on the roles selection      
        do.clickOnEditAuthorization(aName)
        do.assignUserRole("ProgramCreator")
        
# now log out and then log in with the new account and try to create a program
        oldEmail = "user@example.com"
        oldName = "Example User"
        absFilePath = "/Users/uduong/ggrc-core/src/ggrc/login/noop.py"
        do.changeUsernameEmail(oldName, aName, oldEmail, aEmail, absFilePath)
        do.selectMenuInTopRight("Logout")
        
        # Refresh the page
        do.refresh()
        
        # Log back in
        do.login()
        print "Log in as : " + do.whoAmI()
        last_created_object_link = do.createObject("Program")
        object_name = str(do.util.getTextFromXpathString(last_created_object_link)).strip()
        self.assertTrue(do.partialMatch("program-auto-test", object_name), "Fail to match program name.")
        print do.whoAmI()
        self.assertEqual(do.whoAmI(), aName, "Still logged in as old user.")

# Restore old login information
        do.changeUsernameEmail(aName, oldName, aEmail, oldEmail, absFilePath)         

# import and export people ********************************************************
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
        filePath = config.fileDownloadPath + "PEOPLE.csv"
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

# import and export systems ********************************************************
        # create a system
        systemObject =do.createObject("System")
        systemObject = str(util.getTextFromXpathString(systemObject)) #it's name, not xpath
        
        print ""
        print "On screen."
        print "System object is displayed as : " + systemObject
     
        # export system
        filePath = config.fileDownloadPath + "SYSTEMS.csv"
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

# import and export processes ********************************************************
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

    # _ underscore prefix is a convention for internal use
    def _returnStringUpToFirstSpace(self, text):
        index = text.index(' ') # locate index of space
        return text[0:index]

if __name__ == "__main__":
    unittest.main()
