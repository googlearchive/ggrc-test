'''
Created on Sep 26, 2013

@author: diana.tzinov
'''
import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers
from helperRecip.GRCObject import GRCObject


class TestDeleteObject(WebDriverTestCase):

    
    def testDeleteObject(self):
        self.testname="deleteObject"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        grcobject = GRCObject()
        do = Helpers()
        do.setUtils(util)
        do.login()
        for section in ["Program",
                        #"Regulation", 
                        #"Contract",
                         #"Policy", 
                         #"Control",
                         # "Objective", 
                         
                          #"System", 
                         #"Process",
                         #  "Data", 
                        #   "Product", 
                        # "Project", 
                         #  "Facility", 
                          # "Market", 
                         # "Group"
                           ]:
            print "Starting Deletion of Objects for " + section
            deleted_objects=0
            util.clickOn(element.my_work_checkbox)
            while True:
                
                util.inputTextIntoField("Auto", element.left_nav_search_input_textfield)
                util.pressEnterKey(element.left_nav_search_input_textfield)
                do.expandLeftNavMenuForObject(section)
                left_nav_first_link = element.left_nav_first_object_link_in_the_section.replace("SECTION",section)
                util.waitForElementToBePresent(left_nav_first_link,10)
                lef_nav_objects_for_deleteion_in_section = element.left_nav_objects_candidate_for_deletion.replace("SECTION",section )
                number_of_auto_objects = util.getNumberOfOccurences(lef_nav_objects_for_deleteion_in_section)
                print "number of auto objects " + str(number_of_auto_objects)
                if number_of_auto_objects==0:
                    break
                print lef_nav_objects_for_deleteion_in_section
                link = element.left_nav_first_object_link_in_the_section.replace("SECTION",section) 
                do.navigateToObjectAndOpenObjectEditWindow(section,link, refresh_page=False)
                do.deleteObject()
                deleted_objects = deleted_objects+1
            print "Finished Deletion of Objects for " + section +", deleted objects:" + str(deleted_objects)
           

        
if __name__ == "__main__":
    unittest.main()