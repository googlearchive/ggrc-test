'''
Created on Jul 14, 2014

@author: uduong
'''
import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestAllTabsIntegrity(WebDriverTestCase):


    def testAllTabsIntegrity(self):
        self.testname="TestAllTabsIntegrity"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()

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
     
    # _ underscore prefix is a convention for internal use
    def _returnStringUpToFirstSpace(self, text):
        index = text.index(' ') # locate index of space
        return text[0:index]

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()