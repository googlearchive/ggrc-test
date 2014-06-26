'''
Created on Oct 30, 2013

@author: diana.tzinov
'''
'''
Created on Sep 10, 2013

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
import config
import time,  calendar
import datetime
from datetime import timedelta
from datetime import date

THIS_ABS_PATH = os.path.abspath(os.path.dirname(__file__))
SETUP_DIR = os.path.join(THIS_ABS_PATH, 'Setup')
SETUP_FILE_PREFIX = 'audit_setup_data_'
TARGET_SERVER_DICT = {
    "http://grc-test.appspot.com/": "test",
    "http://grc-dev.appspot.com/": "dev",
    "http://localhost:8080/": "local",
}


class TestProgramAudit(WebDriverTestCase):

    def testProgramAudit(self):
        self.testname="TestProgramAudit"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        grcobject = GRCObject()
        do = Helpers(self)
        do.setUtils(util)
        do.login()
        # Read audit_setup_data to retrieve program name and the IDs of the 3 objectives
        #
        objectiveID={}
        # default to using setup file for TEST server
        setup_file = SETUP_FILE_PREFIX + TARGET_SERVER_DICT.get(config.url, "test")
        f = open(os.path.join(SETUP_DIR, setup_file), "r")
        program_name=f.readline().strip("\n")
        # 1.  Navigate to the Program page created in Audit Part 1
        #print first_program_in_lhn
        do.navigateToObjectWithSearch(program_name,"Program")
        util.max_screen()
        
        # 2.  Choose Audit from Object page nav to bring up the Audit widget
        do.navigateToAuditSectionViaInnerNavSection("Audit")

        # 3.  Click on blue +Audit link in widget
        util.clickOn(element.audit_area_plus_audit_link)
                     
        # 4.  New Audit (modal)
        do.authorizeGAPI()  # Another place GAPI dialog could pop up
        new_audit_title = do.createAudit(program_name)
        
        # 5.  Confirm the audit appear in the widget
        newly_created_audit = element.audit_area_by_title.replace("AUDIT_TITLE", new_audit_title)
        print newly_created_audit
        util.waitForElementToBePresent(newly_created_audit)
        self.assertTrue(util.isElementPresent(newly_created_audit), "do not see the newly created audit " +new_audit_title )
        
        # 6. Click on it to open the 2nd tier info.  confirm there are 3 requests in the PBC Requests section. 
        # GAPI could pop up here
        do.authorizeGAPI()
        util.scrollIntoView(newly_created_audit)
        util.clickOn(newly_created_audit + element.first_link_within)
        #util.switch_to_active_element()
        util.max_screen()
        util.scrollIntoView(newly_created_audit)
        #verifying the 3 objectives
        
        do.dismissFlashMessages()
        for objective_title in grcobject.objective_title:
            objective_title_element = element.audit_pbc_request.replace("TITLE", objective_title)
            print objective_title_element
            util.waitForElementToBePresent(objective_title_element)
            self.assertTrue(util.isElementPresent(objective_title_element), "do not see the pbc request " + objective_title_element )
            util.scrollIntoView(objective_title_element)
        
        #do.waitForAlertSuccessMessages()
        
        ####7. Change Objective 2 for Auto test of Audit - Type: Interview
        ###print "Change Objective 2 for Auto test of Audit - Type: Interview"
        #### navigate into PBC edit modal
        ####click on "Objective 2 for Auto test of Audit" to open 2nd tier info
        ###print "click on Objective 2 for Auto test of Audit to open 2nd tier info"
        ###do.expandCollapseRequest(grcobject.objective_title[1])
        ####click on Edit PBC Request
        ###util.waitForElementToBePresent(element.audit_pbc_request_expanded_content_edit_link)
        ###self.assertTrue(util.isElementPresent(element.audit_pbc_request_expanded_content_edit_link), "do not see the Edit link in the expanded request  "  )
        ###util.clickOn(element.audit_pbc_request_expanded_content_edit_link)
        ###objective2_selected_option = element.audit_pbc_request_modal_type_select_selected_option
        ###util.waitForElementToBePresent(element.audit_pbc_request_modal_type_select)
        ###util.selectFromDropdownUntilSelected(element.audit_pbc_request_modal_type_select,  "Interview")
        ####verifying the selected option
        ###
        ###util.waitForElementToBePresent(objective2_selected_option)
        ###do.saveObjectData()
        ###util.clickOn(element.audit_pbc_request_expanded_content_edit_link)
        ###new_value = util.getTextFromXpathString(objective2_selected_option)
        ###self.assertTrue(new_value =="Interview" , "the selected option is not Interview" )

        ####Delete
        ###print "deleting Request"
        ###do.deleteObject()
        ### #8. Change Objective 3 for Auto test of Audit - Type: Population Sample
        ###objective3_select = element.audit_pbc_request_type_select.replace("TITLE", grcobject.objective_title[2] )
        ###do.expandCollapseRequest(grcobject.objective_title[2])
        ####click on Edit PBC Request
        ###util.waitForElementToBePresent(element.audit_pbc_request_expanded_content_edit_link)
        ###self.assertTrue(util.isElementPresent(element.audit_pbc_request_expanded_content_edit_link), "do not see the Edit link in the expanded request  "  )
        ###util.clickOn(element.audit_pbc_request_expanded_content_edit_link)
        ###objective3_selected_option = element.audit_pbc_request_modal_type_select_selected_option
        ###util.waitForElementToBePresent(element.audit_pbc_request_modal_type_select)
        ###util.selectFromDropdownUntilSelected(element.audit_pbc_request_modal_type_select,  "Population Sample")
        ####verifying the selected option
        ###
        ###util.waitForElementToBePresent(objective3_selected_option)
        ###do.saveObjectData()
        ###util.clickOn(element.audit_pbc_request_expanded_content_edit_link)
        ###new_value = util.getTextFromXpathString(objective2_selected_option)
        ###self.assertTrue(new_value == "Population Sample" , "the selected option is not Population Sample" )



        ####Delete
        ###print "deleting Response"
        ###do.deleteObject()
        
        #9.    Click on Objective 1 for Auto Test of Audit to open 2nd tier info (Documentation Response)
        #util.scrollIntoView(newly_created_audit_open_link)
        do.expandCollapseRequest(grcobject.objective_title[0])
        do.setRequestToRespondable(grcobject.objective_title[0])
        # open the response model and fill it out
        new_response_button = element.audit_pbc_request_response_create.replace("TITLE", grcobject.objective_title[0])
        util.waitForElementToBePresent(new_response_button)
        util.clickOn(new_response_button)
        new_response_title = "Response to " + grcobject.objective_title[0]
        do.NewResponseCreate(new_response_title)

        response_element = element.audit_pbc_request_response2.replace("TITLE", grcobject.objective_title[0]).replace("RESPONSE", new_response_title)
        print "response element " + response_element
        util.waitForElementToBePresent(response_element)
        util.scrollIntoView(response_element)       
        self.assertTrue(util.isElementPresent(response_element), "can't see the new Response for the request link") 

        # look for edit button
        new_response_edit_link = element.audit_pbc_request_expanded_response_edit_link2.replace("TITLE", grcobject.objective_title[0]).replace("RESPONSE", new_response_title)
        util.waitForElementToBePresent(new_response_edit_link)
        util.clickOn(new_response_edit_link)
        # need to re-open
        # verify assignee is the same as audit lead (user@example.com)
        pbc_response_elements = {
            # name is description, but functions more like a title in
            # the context of the verifyObjectValues helper
            "title": element.response_title,
            "owner": element.response_assignee,
        }

        pbc_response_values = {
            "title": new_response_title,
            "owner": do.current_user_email(),
        }
        do.verifyObjectValues(pbc_response_elements, pbc_response_values)
        do.saveObjectData()
        audit_edit_button = newly_created_audit + element.audit_edit
        util.scrollIntoView(audit_edit_button)
        util.clickOn(audit_edit_button)
        do.deleteObject()

        # Cut out for now; have minimal working test of audit.
        ### Assign that Response to another team member (jeff@reciprocitylabs.com is fine) while in window
        ##response_email_inputfield = element.audit_pbc_request_expanded_content_response_email_inputfield.replace("TITLE", grcobject.objective_title[0])
        ##print "response_email_inputfield " + response_email_inputfield
        ##util.waitForElementToBePresent(response_email_inputfield)
        ##self.assertTrue(util.isElementPresent(response_email_inputfield), "do not see the firts response owner email textfield presented")
        ##util.inputTextIntoField("jeff@reciprocitylabs.com", response_email_inputfield)
        ##
        ###Click on the response header to open the response
        ##open_response_link = element.audit_pbc_request_response_expand_collapse_link.replace("TITLE",grcobject.objective_title[0] )
        ##util.waitForElementToBePresent(open_response_link)
        ##self.assertTrue(util.isElementPresent(open_response_link), "do not see the open close button for the response")
        ##util.clickOn(open_response_link)
        ##
        ###click +Object to open Map Object Selector. 
        ##add_object_link = element.audit_pbc_request_response_add_object_link.replace("TITLE",grcobject.objective_title[0] )
        ##util.waitForElementToBePresent(add_object_link)
        ##self.assertTrue(util.isElementPresent(add_object_link), "do not see the open close button for the response")
        ##util.clickOn(add_object_link)
        ##
        ###Change top filter to Org Group. 
        ##util.waitForElementToBePresent(element.mapping_modal_window)
        ##self.assertTrue(util.isElementPresent(element.mapping_modal_window), "do not see the modal window")
        ##util.waitForElementToBePresent(element.mapping_modal_top_filter_selector_dropdown)
        ##self.assertTrue(util.isElementPresent(element.mapping_modal_top_filter_selector_dropdown), "do not see the modal window")
        ##util.selectFromDropdownByValue(element.mapping_modal_top_filter_selector_dropdown, "OrgGroup")
        ##
        ###Choose Reciprocity Dev Team and hit Map button. (use search to find this if easier to implement)
        ##util.waitForElementToBePresent(element.mapping_modal_top_filter_selector_dropdown_reciprocity_dev_team_option)
        ##self.assertTrue(util.isElementPresent(element.mapping_modal_top_filter_selector_dropdown_reciprocity_dev_team_option), "do not see the open close button for the response")
        ##util.clickOn(element.mapping_modal_top_filter_selector_dropdown_reciprocity_dev_team_option)
        ##util.waitForElementToBePresent(element.mapping_modal_window_map_button)
        ##self.assertTrue(util.isElementPresent(element.mapping_modal_window_map_button), "no Map button")
        ##util.clickOn(element.mapping_modal_window_map_button)
        ##util.waitForElementNotToBePresent(element.mapping_modal_window)
        ##
        ## #Confirm Reciprocity Dev Team is mapped to the Response and appears in the area provided
        ##util.waitForElementToBePresent(element.audit_pbc_request_response_mapped_org_group_object_withrecipprocity_dev_team)
        ##self.assertTrue(util.isElementPresent(element.audit_pbc_request_response_mapped_org_group_object_withrecipprocity_dev_team), "no Mapped org group button")
        ##
        ###Click +Upload Evidence in the Evidence area to open the file picker
        ##upload_evidence_link = element.audit_pbc_request_response_upload_evidence_link.replace("TITLE",grcobject.objective_title[0] )
        ##util.waitForElementToBePresent(upload_evidence_link)
        ##self.assertTrue(util.isElementPresent(upload_evidence_link), "no Upload Evidence link")
        ##util.clickOn(upload_evidence_link)
        ##util.waitForElementToBePresent('//iFrame[@class="picker-frame picker-dialog-frame"]')
        ###self.assertTrue(util.isElementPresent('//iFrame[@class="picker-frame picker-dialog-frame"]'), "no Upload window")
        ##url=util.getAnyAttribute('//iFrame[@class="picker-frame picker-dialog-frame"]', "src")
        ##print url
        ##util.switchToNewUrl(url)
        ##file_is = os.getcwd() + "/test_screenshot.png"
        ##util.uploadItem(file_is, element.select_file_button)
        ##util.waitForElementToBeVisible(element.upload_file_button)
        ##util.find_element_by_xpath(element.upload_file_button).click() 
        ##time.sleep(10) # wait for uploading the file
        ##util.backBrowser()
        ##util.refreshPage()
        ###waiting to audit to appear back
        ##newly_created_audit = element.audit_area_by_title.replace("AUDIT_TITLE", new_audit_title)
        ##print newly_created_audit
        ##util.waitForElementToBePresent(newly_created_audit)
        ##self.assertTrue(util.isElementPresent(newly_created_audit), "do not see the newly created audit " +new_audit_title )
        ## 
        ##newly_created_audit_open_link  = element.audit_area_by_title.replace("AUDIT_TITLE", new_audit_title)
        ##print newly_created_audit_open_link
        ##util.waitForElementToBePresent(newly_created_audit_open_link)
        ##self.assertTrue(util.isElementPresent(newly_created_audit_open_link), "do not see the newly created audit open link "  )
        ##util.clickOn(newly_created_audit_open_link)
        ##util.switch_to_active_element()
        ###expand objetiive 1 to verify the uploaded file
        ##do.expandCollapseRequest(grcobject.objective_title[0])
        ##evidence_folder_link = element.audit_pb_request_response_evidence_folder_link.replace("TITLE",grcobject.objective_title[0] )
        ##util.waitForElementToBePresent(evidence_folder_link)
        ##self.assertTrue(util.isElementPresent(evidence_folder_link), "do not see the evidene folder link "  )
        ##do.expandCollapseRequest(grcobject.objective_title[0])
        ##time.sleep(2)
        ##
        ###10.  Click on Objective 2 for Auto Test of Audit to open 2nd tier info (Interview)

        ##print "click on Objective 2 for Auto test of Audit to open 2nd tier info"
        ##do.expandCollapseRequest(grcobject.objective_title[1])
        ##objective2_select = element.audit_pbc_request_type_select.replace("TITLE",grcobject.objective_title[1] )
        ##util.waitForElementToBePresent(objective2_select)
        ##util.selectFromDropdownUntilSelected(objective2_select,  "Interview") # didn't work the first time
        ##print "Hover over +PBC Request then click on Create PBC Response to launch modal"
        ##add_pbc_response_link_within_the_objective = element.audit_pbc_request.replace("TITLE",grcobject.objective_title[1] )+element.section_add_link
        ##create_pbc_response_link_within_the_objective = element.audit_pbc_request.replace("TITLE",grcobject.objective_title[1] )+element.section_create_link
        ##util.waitForElementToBePresent(add_pbc_response_link_within_the_objective)
        ##util.scrollIntoView(add_pbc_response_link_within_the_objective)
        ##util.hoverOverAndWaitFor(add_pbc_response_link_within_the_objective,create_pbc_response_link_within_the_objective)
        ##util.clickOn(add_pbc_response_link_within_the_objective)
        ##util.clickOn(create_pbc_response_link_within_the_objective)
        ###Description field :  "Response foir Interview Type", Save
        ##print "creating new interview response"
        ##do.NewResponseCreate("Response for Interview Type")
        ###Click on Response for Interview Type header to reveal response 2nd tier info
      
        ## #click +Object to open Map Object Selector.  Change top filter to Org Group if neccessary (should not be).  Choose Reciprocity Dev Team and hit Map button. (use search to find this if easier to implement)
        ## #Confirm Reciprocity Dev Team is mapped to the Response and appears in the area provided

        ##
        ##
        ###after creating a new response, the whole response section gets expanded automatically now, 
        ###just need to wait for all elements to load (+Object, +Person, + Meeting)
        ##
        ##add_object_link = element.audit_pbc_request_response_add_object_link_within_response.replace("TITLE",grcobject.objective_title[1] )
        ##add_person_link = element.audit_pbc_request_response_add_person_within_response.replace("TITLE",grcobject.objective_title[1] )
        ##add_meeting_link = element.audit_pbc_request_response_add_meeting.replace("TITLE",grcobject.objective_title[1] )
        ##util.waitForElementToBePresent(add_object_link)
        ##self.assertTrue(util.isElementPresent(add_object_link), "do not see the open close button for the response")
        ##util.waitForElementToBePresent(add_person_link)
        ##self.assertTrue(util.isElementPresent(add_person_link), "do not see the + Person link")
        ##util.waitForElementToBePresent(add_meeting_link)
        ##self.assertTrue(util.isElementPresent(add_meeting_link), "do not see the + Meeting link")
        ##
        ###click +Object to open Map Object Selector. 
        ##util.clickOn(add_object_link)
        ## 
        ###Change top filter to Org Group. 
        ##util.waitForElementToBePresent(element.mapping_modal_window)
        ##self.assertTrue(util.isElementPresent(element.mapping_modal_window), "do not see the modal window")
        ##util.waitForElementToBePresent(element.mapping_modal_top_filter_selector_dropdown)
        ##self.assertTrue(util.isElementPresent(element.mapping_modal_top_filter_selector_dropdown), "do not see the modal window")
        ##util.selectFromDropdownByValue(element.mapping_modal_top_filter_selector_dropdown, "OrgGroup")
        ##
        ###Choose Reciprocity Dev Team and hit Map button. (use search to find this if easier to implement)
        ##util.waitForElementToBePresent(element.mapping_modal_top_filter_selector_dropdown_reciprocity_dev_team_option)
        ##self.assertTrue(util.isElementPresent(element.mapping_modal_top_filter_selector_dropdown_reciprocity_dev_team_option), "do not see the open close button for the response")
        ##util.clickOn(element.mapping_modal_top_filter_selector_dropdown_reciprocity_dev_team_option)
        ##util.waitForElementToBePresent(element.mapping_modal_window_map_button)
        ##self.assertTrue(util.isElementPresent(element.mapping_modal_window_map_button), "no Map button")
        ##util.clickOn(element.mapping_modal_window_map_button)
        ##util.waitForElementNotToBePresent(element.mapping_modal_window)
        ##
        ## #Confirm Reciprocity Dev Team is mapped to the Response and appears in the area provided
        ##util.waitForElementToBePresent(element.audit_pbc_request_response_mapped_org_group_object_withrecipprocity_dev_team)
        ##self.assertTrue(util.isElementPresent(element.audit_pbc_request_response_mapped_org_group_object_withrecipprocity_dev_team), "no Mapped org group button")
        ##
        ##
        ###click on +Person link to launch Map People modal
        ##print "click on +Person link to launch Map People modal"
        ###add_person_link = element.audit_pbc_request_response_add_person_within_response.replace("TITLE",grcobject.objective_title[1] )
        ##util.waitForElementToBePresent(add_person_link)
        ##self.assertTrue(util.isElementPresent(add_person_link), "do not see the + Person link")
        ##util.clickOn(add_person_link)
        ##
        ###search for "silas"
        ##print "searching and mapping another participant"
        ##person_email=do.mapPerson("silas")
        ##
        ###confirm silas has been added to Participant area
        ##print "confirming another participant has been mapped"
        ##participant_email = element.audit_pbc_request_response_participant_email.replace("EMAIL",person_email)
        ##util.waitForElementToBePresent(participant_email)
        ##self.assertTrue(util.isElementPresent(participant_email), "do not see the Person Mapped email")
        ##
        ###click on +Meetings in Meetings area
        ##print "click on +Meetings in Meetings area"
        ##
        ##add_meeting_link = element.audit_pbc_request_response_add_meeting.replace("TITLE",grcobject.objective_title[1] )
        ##print "add meeting link is " +add_meeting_link
        ##util.waitForElementToBePresent(add_meeting_link)
        ##self.assertTrue(util.isElementPresent(add_meeting_link), "do not see +Meeting link")
        ##create_meeting_link = element.audit_pbc_request_response_create_meeting.replace("TITLE",grcobject.objective_title[1] )
        ##util.scrollIntoView(add_meeting_link)
        ##util.scrollIntoView(add_meeting_link)
        ##util.move_mouse_over(add_meeting_link)
        ##util.scrollIntoView(add_meeting_link)
        ##util.hoverOver(add_meeting_link)
        ##util.clickOn(create_meeting_link)
        ##
        ##meeting_date = (date.today())+ datetime.timedelta(days=14)
        ##meeting_date_into_format = do.convertDateIntoFormat(meeting_date)
        ##
        ###Enter Title:  Auto Test of Audit - Interview Response - Scheduling a meeting, Choose date : current date + 2 weeks, Set start time to 12pm, Set end time to 1pm, Confirm particpants are silas and testrecip
        ##do.scheduleMeeting("Auto Test of Audit - Interview Response - Scheduling a meeting-"+strftime("%Y_%m_%d__%H_%M_%S"),meeting_date_into_format, "03:00 PM", "04:00 PM")
        ###do.closeOtherWindows()
        ###util.switch_to_active_element()
        ##util.focus()
        ##util.waitForElementToBePresent(element.meeting_expnad_link)
        ##util.clickOn(element.meeting_expnad_link)
        ##
        ##do.verifyMeetingData(meeting_date_into_format, "03:00 PM", "04:00 PM")

        ##do.expandCollapseRequest(grcobject.objective_title[1])

        ##
        ##time.sleep(3)
        ###11. Click on Objective 3 for Auto Test of Audit to open 2nd tier info (Population Sample)
        ##print "11. Click on Objective 3 for Auto Test of Audit to open 2nd tier info (Population Sample)"
        ##do.expandCollapseRequest(grcobject.objective_title[2])
        ##print "Hover over +PBC Request then click on Create PBC Response to launch modal"
        ##add_pbc_response_link_within_the_objective = element.audit_pbc_request.replace("TITLE",grcobject.objective_title[2] )+element.section_add_link
        ##create_pbc_response_link_within_the_objective = element.audit_pbc_request.replace("TITLE",grcobject.objective_title[2] )+element.section_create_link
        ##util.waitForElementToBePresent(add_pbc_response_link_within_the_objective)
        ##util.scrollIntoView(add_pbc_response_link_within_the_objective)
        ##util.hoverOverAndWaitFor(add_pbc_response_link_within_the_objective,create_pbc_response_link_within_the_objective)
        ##util.clickOn(add_pbc_response_link_within_the_objective)
        ##util.clickOn(create_pbc_response_link_within_the_objective)
        ###Description field :  ""Response for Population Sample Type"", Save
        ##print "creating new interview response"
        ##do.NewResponseCreate("Response for Population Sample Type")
        ##
        ###click +Object to open Map Object Selector. 
        ##add_object_link = element.audit_pbc_request_response_add_object_link_within_response.replace("TITLE",grcobject.objective_title[2] )
        ##util.waitForElementToBePresent(add_object_link)
        ##util.clickOn(add_object_link)
        ## 
        ##
        ###Change top filter to Org Group. 
        ##util.waitForElementToBePresent(element.mapping_modal_window)
        ##self.assertTrue(util.isElementPresent(element.mapping_modal_window), "do not see the modal window")
        ##util.waitForElementToBePresent(element.mapping_modal_top_filter_selector_dropdown)
        ##self.assertTrue(util.isElementPresent(element.mapping_modal_top_filter_selector_dropdown), "do not see the modal window")
        ##util.clickOn(element.mapping_modal_search_reset)
        ##util.selectFromDropdownByValue(element.mapping_modal_top_filter_selector_dropdown, "OrgGroup")
        ##
        ###Choose Reciprocity Dev Team and hit Map button. (use search to find this if easier to implement)
        ##util.waitForElementToBePresent(element.mapping_modal_top_filter_selector_dropdown_reciprocity_dev_team_option)
        ##self.assertTrue(util.isElementPresent(element.mapping_modal_top_filter_selector_dropdown_reciprocity_dev_team_option), "do not see the open close button for the response")
        ##util.clickOn(element.mapping_modal_top_filter_selector_dropdown_reciprocity_dev_team_option)
        ##util.waitForElementToBePresent(element.mapping_modal_window_map_button)
        ##self.assertTrue(util.isElementPresent(element.mapping_modal_window_map_button), "no Map button")
        ##util.clickOn(element.mapping_modal_window_map_button)
        ##util.waitForElementNotToBePresent(element.mapping_modal_window)
        ##
        ## #Confirm Reciprocity Dev Team is mapped to the Response and appears in the area provided
        ##util.waitForElementToBePresent(element.audit_pbc_request_response_mapped_org_group_object_withrecipprocity_dev_team)
        ##self.assertTrue(util.isElementPresent(element.audit_pbc_request_response_mapped_org_group_object_withrecipprocity_dev_team), "no Mapped org group button")


if __name__ == "__main__":
    unittest.main()