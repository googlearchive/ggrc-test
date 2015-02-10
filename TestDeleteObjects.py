'''
Created on Aug 26, 2014

@author: ukyo.duong
'''
import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers
from helperRecip.GRCObject import GRCObject


class TestDeleteObjects(WebDriverTestCase):

    
    def testDeleteObjects(self):
        self.testname="TestDeleteObjects"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        grcobject = GRCObject()
        do = Helpers(self)
        do.setUtils(util)
        do.login()
        for section in ["Regulation",
                        "Objective",
                        "Program",                        
                        "Contract",
                        "Policy",
                        "Control",
                        "System",
                        "Process",
                        "Data",
                        "Product",
                        "Project",
                        "Facility",
                        "Market",
                        "Group"
                           ]:
            print "Starting Deletion of Objects for " + section
            deleted_objects=0
            do.ensureLHNSectionExpanded(section)
            do.checkMyWorkBox()
            
            object_left_nav_section_object_link = element.left_nav_expand_object_section_link.replace("OBJECT", section)
#             util.clickOn(object_left_nav_section_object_link)
#             util.inputTextIntoField("Auto", element.left_nav_search_input_textfield)
#             util.pressEnterKey(element.left_nav_search_input_textfield)
            left_nav_first_link = element.left_nav_first_object_link_in_the_section.replace("SECTION",section)
            util.waitForElementToBePresent(left_nav_first_link)
            lef_nav_objects_for_deletion_in_section = element.left_nav_objects_candidate_for_deletion.replace("SECTION",section )
            number_of_auto_objects = do.countOfAnyObjectLHS(section)
                
            deleted_objects = number_of_auto_objects - 2     # leave 2 behind                        

            while (deleted_objects > 0):
                
                
                
                               
                do.navigateToObjectAndOpenObjectEditWindow(section,lef_nav_objects_for_deletion_in_section, refresh_page=False)
                do.deleteObject()
                deleted_objects = deleted_objects - 1 #LHN collapse after this
                
                do.showLHMenu(True) # reopen it
            
                object_left_nav_section_object_link = element.left_nav_expand_object_section_link.replace("OBJECT", section)
#               util.clickOn(object_left_nav_section_object_link)
#               util.inputTextIntoField("Auto", element.left_nav_search_input_textfield)
#               util.pressEnterKey(element.left_nav_search_input_textfield)
                left_nav_first_link = element.left_nav_first_object_link_in_the_section.replace("SECTION",section)
                util.waitForElementToBePresent(left_nav_first_link)
                lef_nav_objects_for_deletion_in_section = element.left_nav_objects_candidate_for_deletion.replace("SECTION",section )
                
            print "Finished deletion of objects for " + section + ". " + str(deleted_objects) + " object is left to be deleted."
           

        
if __name__ == "__main__":
    unittest.main()