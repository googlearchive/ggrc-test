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
        
        directive_xpath = '//a[(@class="governance list-toggle" and @data-object-singular="OBJECT")]'

        self.assertEqual("PROGRAMS", self._returnStringUpToFirstSpace(do.util.getTextFromXpathString(element.left_nav_expand_object_section_link.replace("OBJECT", "Program"))))
        self.assertEqual("AUDITS", self._returnStringUpToFirstSpace(do.util.getTextFromXpathString(element.left_nav_expand_object_section_link.replace("OBJECT", "Audit"))))
        
        temp = do.util.getTextFromXpathString('//a[(@class="governance list-toggle" and @data-object-singular="Regulation")]')
        self.assertEqual("REGULATIONS", self._returnStringUpToFirstSpace(do.util.getTextFromXpathString(self.directive_xpath.replace("OBJECT", "Regulation"))))
        self.assertEqual("POLICIES", self._returnStringUpToFirstSpace(directive_xpath.replace("OBJECT", "Policy")))
        self.assertEqual("STANDARDS", self._returnStringUpToFirstSpace(directive_xpath.replace("OBJECT", "Standard")))
        self.assertEqual("CONTRACTS", self._returnStringUpToFirstSpace(directive_xpath.replace("OBJECT", "Contract")))
        self.assertEqual("CLAUSES", self._returnStringUpToFirstSpace(directive_xpath.replace("OBJECT", "Clause")))
        self.assertEqual("Sections", self._returnStringUpToFirstSpace(directive_xpath.replace("OBJECT", "Section")))
        
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
 
    # _ underscore prefix is a convention for internal use
    def _returnStringUpToFirstSpace(self, text):
        index = text.index(' ') # locate index of space
        return text[0:index]

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()