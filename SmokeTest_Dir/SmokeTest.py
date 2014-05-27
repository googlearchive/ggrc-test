'''
Created on May 20, 2014

@author: ukyo.duong
'''

import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.GRCObject import GRCObject
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestControlCreate(WebDriverTestCase):
   
    util = WebdriverUtilities()
    element = Elements()
    
    def testControlCreate(self):
        self.testname="TestControlCreate"
        self.setup()
        # we have move functions so make these member variables
        
        
        self.util.setDriver(self.driver)
        grcobject = GRCObject()
        do = Helpers(self)
        do.setUtils(self.util)
        do.login()

# verify that all tabs on left hand navigation exist      
#         self.assertEqual("Programs", self._returnStringUpToFirstSpace(self.element.left_nav_expand_object_section_link.replace("OBJECT", "Program")))
#         self.assertEqual("Audits", self._returnStringUpToFirstSpace(self.element.left_nav_expand_object_section_link.replace("OBJECT", "Audit")))
#         self.assertEqual("Regulations", self._returnStringUpToFirstSpace(self.element.left_nav_expand_object_section_link.replace("OBJECT", "Regulation")))
#         self.assertEqual("Policies", self._returnStringUpToFirstSpace(self.element.left_nav_expand_object_section_link.replace("OBJECT", "Policy")))
#         self.assertEqual("Standards", self._returnStringUpToFirstSpace(self.element.left_nav_expand_object_section_link.replace("OBJECT", "Standard")))
#         self.assertEqual("Contracts", self._returnStringUpToFirstSpace(self.element.left_nav_expand_object_section_link.replace("OBJECT", "Contract")))
#         self.assertEqual("Clauses", self._returnStringUpToFirstSpace(self.element.left_nav_expand_object_section_link.replace("OBJECT", "Clause")))
#         self.assertEqual("Sections", self._returnStringUpToFirstSpace(self.element.left_nav_expand_object_section_link.replace("OBJECT", "Section")))
#         self.assertEqual("Objectives", self._returnStringUpToFirstSpace(self.element.left_nav_expand_object_section_link.replace("OBJECT", "Objective")))
#         self.assertEqual("Controls", self._returnStringUpToFirstSpace(self.element.left_nav_expand_object_section_link.replace("OBJECT", "Control")))
#         self.assertEqual("People", self._returnStringUpToFirstSpace(self.element.left_nav_expand_object_section_link.replace("OBJECT", "Person")))               
#         self.assertEqual("Org Groups", self.util.getTextFromXpathString(self.element.left_nav_org_group_link)[0:10])
#         self.assertEqual("Systems", self._returnStringUpToFirstSpace(self.element.left_nav_expand_object_section_link.replace("OBJECT", "System")))
#         self.assertEqual("Processes", self._returnStringUpToFirstSpace(self.element.left_nav_expand_object_section_link.replace("OBJECT", "Process")))
#         self.assertEqual("Data Assets", self.util.getTextFromXpathString(self.element.left_nav_data_asset_link)[0:11])
#         self.assertEqual("Products", self._returnStringUpToFirstSpace(self.element.left_nav_expand_object_section_link.replace("OBJECT", "Product")))
#         self.assertEqual("Projects", self._returnStringUpToFirstSpace(self.element.left_nav_expand_object_section_link.replace("OBJECT", "Project")))
#         self.assertEqual("Facilities", self._returnStringUpToFirstSpace(self.element.left_nav_expand_object_section_link.replace("OBJECT", "Facility")))
#         self.assertEqual("Markets", self.util.getTextFromXpathString(self.element.left_nav_market_link)[0:7])
#         self.assertEqual("Risk Assessments", self.util.getTextFromXpathString(self.element.left_nav_risk_assessment_link)[0:16])
#         self.assertEqual("Threats", self._returnStringUpToFirstSpace(self.element.left_nav_expand_object_section_link.replace("OBJECT", "Threat")))
#         self.assertEqual("Vulnerabilities", self._returnStringUpToFirstSpace(self.element.left_nav_expand_object_section_link.replace("OBJECT", "Vulnerability")))
#         self.assertEqual("Templates", self._returnStringUpToFirstSpace(self.element.left_nav_expand_object_section_link.replace("OBJECT", "Template")))

        
#verify create, update, delete
#         last_created_object_link = do.createObject("Program")
#         object_name = str(self.util.getTextFromXpathString(last_created_object_link)).strip()
#         do.navigateToObjectAndOpenObjectEditWindow("Program",last_created_object_link)
#         do.populateObjectInEditWindow( object_name , grcobject.program_elements, grcobject.program_values)
#         do.openObjectEditWindow()
#         do.showHiddenValues()
#         do.verifyObjectValues(grcobject.program_elements, grcobject.program_values)
#         do.deleteObject()
#             
#         last_created_object_link = do.createObject("Regulation")
#         object_name = str(self.util.getTextFromXpathString(last_created_object_link)).strip()
#         do.navigateToObjectAndOpenObjectEditWindow("Regulation",last_created_object_link)
#         do.populateObjectInEditWindow( object_name , grcobject.regulation_elements, grcobject.regulation_values)
#         do.openObjectEditWindow()
#         do.showHiddenValues()
#         do.verifyObjectValues(grcobject.regulation_elements, grcobject.regulation_values)
#         do.deleteObject()
#             
#         last_created_object_link = do.createObject("System")
#         object_name = str(self.util.getTextFromXpathString(last_created_object_link)).strip()
#         do.navigateToObjectAndOpenObjectEditWindow("System",last_created_object_link)
#         do.populateObjectInEditWindow( object_name , grcobject.system_elements, grcobject.system_values)
#         do.openObjectEditWindow()
#         do.showHiddenValues()
#         do.verifyObjectValues(grcobject.system_elements, grcobject.system_values)
#         do.deleteObject()
         

    
# mapping and un-mapping up to 3 levels: 

        #Program->Regulation->Section->Object
        do.createObject("Regulation", "myRegulationX")
        last_created_object_link = do.createObject("Program", "myProgramX")
        do.navigateToObjectWithSearch("myProgramX", "Program")
        do.mapAObjectLHN("Regulation") # maps to a Regulation object
        do.expandItemWidget() #expand the item so that "+ Section" link is displayed
        do.createSectionFromInnerNavLink()
        do.mapObjectToSectionFromInnerNav("mySectionX")
        do.mapObjectFormFilling("Person", "john doe x")
        do.expandMapObjectItemWidget()
        do.unMapObjectFromWidget(True) #unmap object
        do.deleteObjectFromSectionAfterMapping()
        do.unMapObjectFromWidget(False) #unmap regulation    
    
    












    # _ underscore prefix is a convention for internal use
    def _returnStringUpToFirstSpace(self, elem):
        str = self.util.getTextFromXpathString(elem)
        index = str.index(' ') # locate index of space
        return str[0:index]

if __name__ == "__main__":
    unittest.main()
