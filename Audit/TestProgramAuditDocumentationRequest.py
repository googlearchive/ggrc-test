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



class TestProgramAuditDocumentationRequest(WebDriverTestCase):

    
    def testProgramAuditDocumentationRequest(self):
        self.testname="testProgramAuditDocumentationRequest"
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
        
        util.switch_to_active_element()
        util.get_a_screen_shot("test_screenshot.png")
        
        do.expandCollapseRequest(grcobject.objective_title[0])
        #.    Assign that Response to another team member (jeff@reciprocitylabs.com is fine)
        response_email_inputfield = element.audit_pbc_request_expanded_content_response_email_inputfield.replace("TITLE",grcobject.objective_title[0] )
        print "response_email_inputfield " + response_email_inputfield
        util.waitForElementToBePresent(response_email_inputfield)
        self.assertTrue(util.isElementPresent(response_email_inputfield), "do not see the firts response owner email textfield presented")
        util.inputTextIntoField("jeff@reciprocitylabs.com", response_email_inputfield)
        
        #Click on the response header to open the response
        open_response_link = element.audit_pbc_request_response_expand_collapse_link.replace("TITLE",grcobject.objective_title[0] )
        util.waitForElementToBePresent(open_response_link)
        self.assertTrue(util.isElementPresent(open_response_link), "do not see the open close button for the response")
        util.clickOn(open_response_link)
        
        #click +Object to open Map Object Selector. 
        add_object_link = element.audit_pbc_request_response_add_object_link.replace("TITLE",grcobject.objective_title[0] )
        util.waitForElementToBePresent(add_object_link)
        self.assertTrue(util.isElementPresent(add_object_link), "do not see the open close button for the response")
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
        
        #Click +Upload Evidence in the Evidence area to open the file picker
        upload_evidence_link = element.audit_pbc_request_response_upload_evidence_link.replace("TITLE",grcobject.objective_title[0] )
        util.waitForElementToBePresent(upload_evidence_link)
        self.assertTrue(util.isElementPresent(upload_evidence_link), "no Upload Evidence link")
        util.clickOn(upload_evidence_link)
        util.waitForElementToBePresent('//iFrame[@class="picker-frame picker-dialog-frame"]')
        #self.assertTrue(util.isElementPresent('//iFrame[@class="picker-frame picker-dialog-frame"]'), "no Upload window")
        url=util.getAnyAttribute('//iFrame[@class="picker-frame picker-dialog-frame"]', "src")
        print url
        util.switchToNewUrl(url)
        file_is = os.getcwd() + "/test_screenshot.png"
        util.uploadItem(file_is, element.select_file_button)
        util.waitForElementToBeVisible(element.upload_file_button)
        util.find_element_by_xpath(element.upload_file_button).click() 
        time.sleep(10) # wait for uploading the file
        util.backBrowser()
        util.refreshPage()
        #waiting to audit to appear back
        newly_created_audit = element.audit_area_created_audit.replace("AUDIT_TITLE", "2014: program - Audit")
        #newly_created_audit = element.audit_area_created_audit.replace("AUDIT_TITLE", new_audit_title)
        print newly_created_audit
        util.waitForElementToBePresent(newly_created_audit)
        self.assertTrue(util.isElementPresent(newly_created_audit), "do not see the newly created audit 2014: program - Audit")
         
        newly_created_audit_open_link  = element.audit_area_created_audit_open_link.replace("AUDIT_TITLE", "2014: program - Audit") 
        #newly_created_audit_open_link  = element.audit_area_created_audit_open_link.replace("AUDIT_TITLE", new_audit_title)
        print newly_created_audit_open_link
        util.waitForElementToBePresent(newly_created_audit_open_link)
        self.assertTrue(util.isElementPresent(newly_created_audit_open_link), "do not see the newly created audit open link "  )
        util.clickOn(newly_created_audit_open_link)
        util.switch_to_active_element()
        #expand objetiive 1 to verify the uploaded file
        do.expandCollapseRequest(grcobject.objective_title[0])
        evidence_folder_link = element.audit_pb_request_response_evidence_folder_link.replace("TITLE",grcobject.objective_title[0] )
        util.waitForElementToBePresent(evidence_folder_link)
        self.assertTrue(util.isElementPresent(evidence_folder_link), "do not see the evidene folder link "  )
        do.expandCollapseRequest(grcobject.objective_title[0])
   



if __name__ == '__main__':
    pass