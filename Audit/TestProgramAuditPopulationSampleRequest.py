'''
Created on Jan 11, 2014

@author: diana.tzinov
'''





import unittest
import time
import os
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers
from helperRecip.GRCObject import GRCObject
import time,  calendar
import datetime
from datetime import timedelta
from datetime import date



class TestProgramAuditPopulationSampleRequest(WebDriverTestCase):

    
    def testProgramAuditPopulationSampleRequest(self):
        self.testname="TestProgramAuditPopulationSampleRequest"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        grcobject = GRCObject()
        do = Helpers()
        do.setUtils(util)
        do.login()

        #
        # Read audit_setup_data to retrieve program name and the IDs of the 3 objectives
        #
        objectiveID={}
        f=open("audit_setup_data","r")
        program_name=f.readline().strip("\n")

        do.navigateToObjectWithSearch(program_name,"Program")
        util.max_screen()
        
        # 2.  Choose Audit from Object page nav to bring up the Audit widget
        do.navigateToAuditSectionViaInnerNavSection("Audit")
        newly_created_audit = element.audit_area_created_audit.replace("AUDIT_TITLE", "2014: program - Audit")
       
        print newly_created_audit
        util.waitForElementToBePresent(newly_created_audit)
        self.assertTrue(util.isElementPresent(newly_created_audit), "do not see the newly created audit " +"2014: program - Audit" )
        
        # 6. Click on it to open the 2nd tier info.  confirm there are 3 requests in the PBC Requests section. 
        newly_created_audit_open_link  = element.audit_area_created_audit_open_link.replace("AUDIT_TITLE", "2014: program - Audit")
        print newly_created_audit_open_link
        util.waitForElementToBePresent(newly_created_audit_open_link)
        self.assertTrue(util.isElementPresent(newly_created_audit_open_link), "do not see the newly created audit open link "  )
        util.clickOn(newly_created_audit_open_link)
        util.switch_to_active_element()

        for objective_title in grcobject.objective_title:
            objective_title_element = element.audit_pbc_request.replace("TITLE", objective_title)
            print objective_title_element
            util.waitForElementToBePresent(objective_title_element)
            self.assertTrue(util.isElementPresent(objective_title_element), "do not see the pbc request " + objective_title_element )
            
            
                #8. Change Objective 3 for Auto test of Audit - Type: Population Sample
        objective3_select = element.audit_pbc_request_type_select.replace("TITLE",grcobject.objective_title[2] )
        util.waitForElementToBePresent(objective3_select)
        #print "Change Objective 3 for Auto test of Audit - Type: Population Sample"
        #util.selectFromDropdownUntilSelected(objective3_select,  "Population Sample")
        #click on "Objective 3 for Auto test of Audit" to open 2nd tier info
        
        do.expandCollapseRequest(grcobject.objective_title[2])
        #click on Edit PBC Response
        util.waitForElementToBePresent(element.audit_pbc_request_expanded_content_edit_link)
        self.assertTrue(util.isElementPresent(element.audit_pbc_request_expanded_content_edit_link), "do not see the Edit link in the expanded request  "  )
        #click on Response to open that 2nd tier info
        response_element = element.audit_pbc_request_response.replace("TITLE",grcobject.objective_title[2] )
        print "response element " + response_element
        util.waitForElementToBePresent(response_element)
        self.assertTrue(util.isElementPresent(response_element), "do not see the Respond element in the expanded Request section for  "+ grcobject.objective_title[2]   )
        print "expanding response and Edit PBC Response "
        util.clickOn(response_element) #to expand the response
        util.waitForElementToBePresent(element.audit_pbc_request_expanded_response_edit_link)
        self.assertTrue(util.isElementPresent(element.audit_pbc_request_expanded_response_edit_link), "do not see the Edit PBS Response link in the expanded Request section for  "+ grcobject.objective_title[2]   )
        util.clickOn(element.audit_pbc_request_expanded_response_edit_link)
        #Delete
        print "deleting Response"
        do.deleteObject()
        #collapse back the request
       # print "collapse back the request"
       
        #do.expandCollapseRequest(grcobject.objective_title[2])
        #time.sleep(5)
        util.selectFromDropdownUntilSelected(objective3_select,  "Population Sample")
        
        #taking a screenshot
        util.switch_to_active_element()
        util.get_a_screen_shot("test_screenshot.png")
        
        #11. Click on Objective 3 for Auto Test of Audit to open 2nd tier info (Population Sample)
        print "11. Click on Objective 3 for Auto Test of Audit to open 2nd tier info (Population Sample)"
        
        do.expandCollapseRequest(grcobject.objective_title[2])
        print "Hover over +PBC Request then click on Create PBC Response to launch modal"
        add_pbc_response_link_within_the_objective = element.audit_pbc_request.replace("TITLE",grcobject.objective_title[2] )+element.section_add_link
        create_pbc_response_link_within_the_objective = element.audit_pbc_request.replace("TITLE",grcobject.objective_title[2] )+element.section_create_link
        util.waitForElementToBePresent(add_pbc_response_link_within_the_objective)
        self.assertTrue(util.isElementPresent(add_pbc_response_link_within_the_objective), "do not see the add response link")
        util.scrollIntoView(add_pbc_response_link_within_the_objective)
        #util.hoverOverAndWaitFor(add_pbc_response_link_within_the_objective,create_pbc_response_link_within_the_objective)
        util.hoverOver(add_pbc_response_link_within_the_objective)
        #util.clickOn(add_pbc_response_link_within_the_objective)
        util.clickOn(create_pbc_response_link_within_the_objective)
        #Description field :  ""Response for Population Sample Type"", Save
        
        print "creating new population sample response"
        do.NewResponseCreate("Response for Population Sample Type")
        
        #click +Object to open Map Object Selector. 
        add_object_link = element.audit_pbc_request_response_add_object_link_within_response.replace("TITLE",grcobject.objective_title[2] )
        util.waitForElementToBePresent(add_object_link)
        util.clickOn(add_object_link)
         
        
        #Change top filter to Org Group. 
        util.waitForElementToBePresent(element.mapping_modal_window)
        self.assertTrue(util.isElementPresent(element.mapping_modal_window), "do not see the modal window")
        util.waitForElementToBePresent(element.mapping_modal_top_filter_selector_dropdown)
        self.assertTrue(util.isElementPresent(element.mapping_modal_top_filter_selector_dropdown), "do not see the modal window")
        util.clickOn(element.mapping_modal_search_reset)
        util.selectFromDropdownByValue(element.mapping_modal_top_filter_selector_dropdown, "OrgGroup")
        
        #Choose Reciprocity Dev Team and hit Map button. (use search to find this if easier to implement)
        util.waitForElementToBePresent(element.mapping_modal_top_filter_selector_dropdown_reciprocity_dev_team_option)
        self.assertTrue(util.isElementPresent(element.mapping_modal_top_filter_selector_dropdown_reciprocity_dev_team_option), "do not see the open close button for the response")
        util.clickOn(element.mapping_modal_top_filter_selector_dropdown_reciprocity_dev_team_option)
        util.waitForElementToBePresent(element.mapping_modal_window_map_button)
        self.assertTrue(util.isElementPresent(element.mapping_modal_window_map_button), "no Map button")
        util.clickOn(element.mapping_modal_window_map_button)
        util.waitForElementNotToBePresent(element.mapping_modal_window)
        
         #Confirm Reciprocity Dev Team is mapped to the Response and appears in the area provided
        util.waitForElementToBePresent(element.audit_pbc_request_response_mapped_org_group_object_withrecipprocity_dev_team)
        self.assertTrue(util.isElementPresent(element.audit_pbc_request_response_mapped_org_group_object_withrecipprocity_dev_team), "no Mapped org group button")

        #deleteing the responce
        

if __name__ == '__main__':
    pass