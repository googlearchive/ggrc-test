'''
Created on Jan 10, 2014

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



class TestProgramAuditInterviewRequest(WebDriverTestCase):

    
    def testProgramAuditInterviewRequest(self):
        self.testname="TestProgramAuditInterviewRequest"
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
            
                #7. Change Objective 2 for Auto test of Audit - Type: Interview
        
#         print "Change Objective 2 for Auto test of Audit - Type: Interview"
        objective2_select = element.audit_pbc_request_type_select.replace("TITLE",grcobject.objective_title[1] )
        objective2_selected_option = element.audit_pbc_request_type_select_selected_option.replace("TITLE",grcobject.objective_title[1] )
        """
        util.waitForElementToBePresent(objective2_select)
        util.selectFromDropdownUntilSelected(objective2_select,  "Interview")
        #verifying the selected option
        
        util.waitForElementToBePresent(objective2_selected_option)
        new_value = util.getTextFromXpathString(objective2_selected_option)
        self.assertTrue(new_value =="Interview" , "the selected option is not Interview" )
        """
        
        #click on "Objective 2 for Auto test of Audit" to open 2nd tier info
        print "click on Objective 2 for Auto test of Audit to open 2nd tier info"
        do.expandCollapseRequest(grcobject.objective_title[1])
        #click on Edit PBC Response
        util.waitForElementToBePresent(element.audit_pbc_request_expanded_content_edit_link)
        self.assertTrue(util.isElementPresent(element.audit_pbc_request_expanded_content_edit_link), "do not see the Edit link in the expanded request  "  )
        #click on Response to open that 2nd tier info
        response_element = element.audit_pbc_request_response.replace("TITLE",grcobject.objective_title[1] )
        print "response element " + response_element
        util.waitForElementToBePresent(response_element)
        self.assertTrue(util.isElementPresent(response_element), "do not see the Respond element in the expanded Request section for  "+ grcobject.objective_title[1]   )
        print "expanding response and Edit PBC Response "
        util.clickOn(response_element) #to expand the response
        util.waitForElementToBePresent(element.audit_pbc_request_expanded_response_edit_link)
        self.assertTrue(util.isElementPresent(element.audit_pbc_request_expanded_response_edit_link), "do not see the Edit PBS Response link in the expanded Request section for  "+ grcobject.objective_title[1]   )
        util.clickOn(element.audit_pbc_request_expanded_response_edit_link)
        #Delete
        print "deleting Response"
        do.deleteObject()
        #collapse back the request
        print "collapse back the request"
        do.expandCollapseRequest(grcobject.objective_title[1])
        time.sleep(3)
        util.selectFromDropdownUntilSelected(objective2_select,  "Interview")
        time.sleep(3)
        
        util.waitForElementToBePresent(objective2_selected_option)
        new_value = util.getTextFromXpathString(objective2_selected_option)
        self.assertTrue(new_value =="Interview" , "the selected option is not Interview" )
        
        #10.  Click on Objective 2 for Auto Test of Audit to open 2nd tier info (Interview)

        print "click on Objective 2 for Auto test of Audit to open 2nd tier info"
        do.expandCollapseRequest(grcobject.objective_title[1])
        objective2_select = element.audit_pbc_request_type_select.replace("TITLE",grcobject.objective_title[1] )
        util.waitForElementToBePresent(objective2_select)
        util.selectFromDropdownUntilSelected(objective2_select,  "Interview") # didn't work the first time
        print "Hover over +PBC Request then click on Create PBC Response to launch modal"
        add_pbc_response_link_within_the_objective = element.audit_pbc_request.replace("TITLE",grcobject.objective_title[1] )+element.section_add_link
        create_pbc_response_link_within_the_objective = element.audit_pbc_request.replace("TITLE",grcobject.objective_title[1] )+element.section_create_link
        util.waitForElementToBePresent(add_pbc_response_link_within_the_objective)
        util.scrollIntoView(add_pbc_response_link_within_the_objective)
        util.hoverOverAndWaitFor(add_pbc_response_link_within_the_objective,create_pbc_response_link_within_the_objective)
        util.clickOn(add_pbc_response_link_within_the_objective)
        util.clickOn(create_pbc_response_link_within_the_objective)
        #Description field :  "Response foir Interview Type", Save
        print "creating new interview response"
        do.NewResponseCreate("Response for Interview Type")
        #Click on Response for Interview Type header to reveal response 2nd tier info
      
         #click +Object to open Map Object Selector.  Change top filter to Org Group if neccessary (should not be).  Choose Reciprocity Dev Team and hit Map button. (use search to find this if easier to implement)
         #Confirm Reciprocity Dev Team is mapped to the Response and appears in the area provided

        
        
        #after creating a new response, the whole response section gets expanded automatically now, 
        #just need to wait for all elements to load (+Object, +Person, + Meeting)
        
        add_object_link = element.audit_pbc_request_response_add_object_link_within_response.replace("TITLE",grcobject.objective_title[1] )
        add_person_link = element.audit_pbc_request_response_add_person_within_response.replace("TITLE",grcobject.objective_title[1] )
        add_meeting_link = element.audit_pbc_request_response_add_meeting.replace("TITLE",grcobject.objective_title[1] )
        util.waitForElementToBePresent(add_object_link)
        self.assertTrue(util.isElementPresent(add_object_link), "do not see the open close button for the response")
        util.waitForElementToBePresent(add_person_link)
        self.assertTrue(util.isElementPresent(add_person_link), "do not see the + Person link")
        util.waitForElementToBePresent(add_meeting_link)
        self.assertTrue(util.isElementPresent(add_meeting_link), "do not see the + Meeting link")
        
        #click +Object to open Map Object Selector. 
        util.clickOn(add_object_link)
         
        #Change top filter to Org Group. 
        util.waitForElementToBePresent(element.mapping_modal_window)
        self.assertTrue(util.isElementPresent(element.mapping_modal_window), "do not see the modal window")
        util.waitForElementToBePresent(element.mapping_modal_top_filter_selector_dropdown)
        self.assertTrue(util.isElementPresent(element.mapping_modal_top_filter_selector_dropdown), "do not see the modal window")
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
        
        
        #click on +Person link to launch Map People modal
        print "click on +Person link to launch Map People modal"
        #add_person_link = element.audit_pbc_request_response_add_person_within_response.replace("TITLE",grcobject.objective_title[1] )
        util.waitForElementToBePresent(add_person_link)
        self.assertTrue(util.isElementPresent(add_person_link), "do not see the + Person link")
        util.clickOn(add_person_link)
        
        #search for "silas"
        print "searching and mapping another participant"
        person_email=do.mapPerson("silas")
        
        #confirm silas has been added to Participant area
        print "confirming another participant has been mapped"
        participant_email = element.audit_pbc_request_response_participant_email.replace("EMAIL",person_email)
        util.waitForElementToBePresent(participant_email)
        self.assertTrue(util.isElementPresent(participant_email), "do not see the Person Mapped email")
        
        #click on +Meetings in Meetings area
        print "click on +Meetings in Meetings area"
        
        add_meeting_link = element.audit_pbc_request_response_add_meeting.replace("TITLE",grcobject.objective_title[1] )
        print "add meeting link is " +add_meeting_link
        util.waitForElementToBePresent(add_meeting_link)
        self.assertTrue(util.isElementPresent(add_meeting_link), "do not see +Meeting link")
        create_meeting_link = element.audit_pbc_request_response_create_meeting.replace("TITLE",grcobject.objective_title[1] )
        util.scrollIntoView(add_meeting_link)
        util.scrollIntoView(add_meeting_link)
        util.move_mouse_over(add_meeting_link)
        util.scrollIntoView(add_meeting_link)
        util.hoverOver(add_meeting_link)
        util.clickOn(create_meeting_link)
        
        meeting_date = (date.today())+ datetime.timedelta(days=14)
        meeting_date_into_format = do.convertDateIntoFormat(meeting_date)
        
        #Enter Title:  Auto Test of Audit - Interview Response - Scheduling a meeting, Choose date : current date + 2 weeks, Set start time to 12pm, Set end time to 1pm, Confirm particpants are silas and testrecip
        do.scheduleMeeting("Auto Test of Audit - Interview Response - Scheduling a meeting-"+strftime("%Y_%m_%d__%H_%M_%S"),meeting_date_into_format, "03:00 PM", "04:00 PM")
        #do.closeOtherWindows()
        #util.switch_to_active_element()
        util.focus()
        util.waitForElementToBePresent(element.meeting_expnad_link)
        util.clickOn(element.meeting_expnad_link)
        
        do.verifyMeetingData(meeting_date_into_format, "03:00 PM", "04:00 PM")
        
if __name__ == '__main__':
    pass