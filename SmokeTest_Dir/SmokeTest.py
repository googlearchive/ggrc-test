
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
from helperRecip.WorkFlowHelper import WorkFlowHelper
from helperRecip.testcase import WebDriverTestCase


myUtil = 0

class SmokeTest(WebDriverTestCase):
    
    
    
    def testSmokeTest(self):
        self.testname="SmokeTest"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        grcobject = GRCObject()
        do = Helpers(self)
        do.setUtils(util)
        myUtil = do.getUtils()
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
        time.sleep(5)     
        last_created_object_link = do.createObject("Regulation")
        object_name = str(do.util.getTextFromXpathString(last_created_object_link)).strip()
        do.navigateToObjectAndOpenObjectEditWindow("Regulation", last_created_object_link)
        do.populateObjectInEditWindow(object_name , grcobject.regulation_elements, grcobject.regulation_values)
        do.openObjectEditWindow()
        do.showHiddenValues()
        do.verifyObjectValues(grcobject.regulation_elements, grcobject.regulation_values)
        do.deleteObject()
        time.sleep(5)    
        last_created_object_link = do.createObject("System")
        object_name = str(do.util.getTextFromXpathString(last_created_object_link)).strip()
        do.navigateToObjectAndOpenObjectEditWindow("System", last_created_object_link)
        do.populateObjectInEditWindow(object_name , grcobject.system_elements, grcobject.system_values, "testrecip@gmail.com")
        do.openObjectEditWindow()
        do.showHiddenValues()
        do.verifyObjectValues(grcobject.system_elements, grcobject.system_values)
        do.deleteObject()
        time.sleep(5)  

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
 
# map workflow(instead of audit)  to -> program
        titleWF = do.getUniqueString("workflow")
        do.createObject("Workflow", titleWF)     
        do.navigateToObjectWithSearch(titlePrgm, "Program")
        do.mapAObjectLHN("Workflow", titleWF)    
 
# unmap workflow <-- from program
        self.assertTrue(do.unmapAObjectFromWidget("workflow"), "Fail unmapping Workflow from Program")
 
# event log
        do.selectMenuInTopRight("Admin Dashboard")
        do.selectMenuItemInnerNavDashBoard("People")
        do.verifyInfoInEventLogTable(titleWF + " unmapped from " + titlePrgm, 0)
        do.verifyInfoInEventLogTable(titleWF + " mapped to " + titlePrgm, 1)
 
# import people
        # can't do now because there is no test tool to interact with Linux OS object
        # On windows, there is AutoIT that you can use to interacti with Windows' object like the upload button
 
# create person in Admin Dashboard
        aEmail = "auto_email_" + str(do.getRandomNumber(65535)) + "@gmail.com"
        aName = do.getUniqueString("name")
        aCompany = do.getUniqueString("company")
 
        do.addPersonInAdminDB(aName, aEmail, aCompany)
        self.assertTrue(do.searchPersonInAdminDB(aName), "newly added person named \"" + aName + "\" is not found.")
        
# export people
        do.exportFile("people")
        print ""
        print "*** ATTENTION:  Need to manually verify if file exported correctly ***"
        print ""

# export systems
        do.exportFile("system")
        print ""
        print "*** ATTENTION:  Need to manually verify if file exported correctly ***"
        print ""

# export processes
        do.exportFile("process")
        print ""
        print "*** ATTENTION:  Need to manually verify if file exported correctly ***"
        print ""

# add role in Admin Dashboard
        do.selectMenuItemInnerNavDashBoard("Roles") # on the roles selection
        count_before = do.roleCount()
        do.createRoleInAdminDB("readingOnly", "this role can read only")
        count_after = do.roleCount()
        self.assertEquals(count_after, count_before+1, "Role count has not incremented.")


    # _ underscore prefix is a convention for internal use
    def _returnStringUpToFirstSpace(self, text):
        index = text.index(' ') # locate index of space
        return text[0:index]

if __name__ == "__main__":
    unittest.main()
