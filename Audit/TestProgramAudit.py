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
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers
from helperRecip.GRCObject import GRCObject



class TestProgramAudit(WebDriverTestCase):

    
    def testProgramAudit(self):
        self.testname="TestProgramAudit"
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
        objectiveID[0]=int(f.readline().strip("\n"))
        objectiveID[1]=int(f.readline().strip("\n"))
        objectiveID[2]=int(f.readline().strip("\n"))
        print program_name
        print objectiveID
        
        
        
        # 1.  Navigate to the Program page created in Audit Part 1
        first_program_in_lhn = '//ul[@class="top-level"]//li[contains(@data-model-name,"Program")]//li[contains(.,"'+program_name+'")]/a'
        print first_program_in_lhn
        do.navigateToObject("Program", first_program_in_lhn)
        
        # 2.  Choose Audit from Object page nav to bring up the Audit widget
        do.navigateToAuditSectionViaInnerNavSection("Audit")
        
        # 3.  Hover over blue +Audit link in widget, link changes to Create Audit - Click on Create Audit to open modal
        util.hoverOverAndWaitFor(element.audit_area_plus_audit_link, element.audit_area_create_audit_link)
        util.clickOn( element.audit_area_create_audit_link)
        
        # 4.  New Audit (modal)
        new_audit_title = do.createAudit(program_name)
        
        # 5.  Confirm the audit appear in the widget
        newly_created_audit = element.audit_area_created_audit.replace("AUDIT_TITLE", new_audit_title)
        print newly_created_audit
        util.waitForElementToBePresent(newly_created_audit)
        self.assertTrue(util.isElementPresent(newly_created_audit), "do not see the newly created audit " +new_audit_title )
        
        # 6. Click on it to open the 2nd tier info.  confirm there are 3 requests in the PBC Requests section. 
        newly_created_audit_open_link  = element.audit_area_created_audit_open_link.replace("AUDIT_TITLE", new_audit_title)
        print newly_created_audit_open_link
        util.waitForElementToBePresent(newly_created_audit_open_link)
        self.assertTrue(util.isElementPresent(newly_created_audit_open_link), "do not see the newly created audit open link "  )
        util.clickOn(newly_created_audit_open_link)
        util.switch_to_active_element()
        #verifying the 3 objectives
        
        for objective_title in grcobject.objective_title:
            objective_title_element = element.audit_pbc_request.replace("TITLE", objective_title)
            print objective_title_element
            util.waitForElementToBePresent(objective_title_element)
            self.assertTrue(util.isElementPresent(objective_title_element), "do not see the pbc request " + objective_title_element )
        
        #7. Change Objective 2 for Auto test of Audit - Type: Interview
        objective2_select = element.audit_pbc_request_type_select.replace("TITLE",grcobject.objective_title[1] )
        util.waitForElementToBePresent(objective2_select)
        util.selectFromDropdownUntilSelected(objective2_select,  "Interview")
        
        # 8. Change Objective 3 for Auto test of Audit - Type: Population Sample
        objective3_select = element.audit_pbc_request_type_select.replace("TITLE", grcobject.objective_title[2])
        util.waitForElementToBePresent(objective3_select)
        util.selectFromDropdownUntilSelected(objective3_select,  "Population Sample")
        
        do.expandRequest(grcobject.objective_title[0])
        time.sleep(5)

        #9A.    confirm the Response auto created 
        response_element = element.audit_pbc_request_response.replace("TITLE",grcobject.objective_title[0] )
        print "response element " + response_element
        util.waitForElementValueToBePresent(response_element)
        self.assertTrue(util.isElementPresent(response_element), "can't see the expanded contetnt for the request link") 
        #util.waitForElementToBePresent(element.audit_pbc_request_response)
        #self.assertTrue(util.isElementPresent(element.audit_pbc_request_response), "do not see the firts response presented")
            
       
        #B.    Assign that Response to another team member (jeff@reciprocitylabs.com is fine)
        #response_email_inputfield = element.audit_pbc_request_expanded_content_response_email_inputfield.replace("TITLE",grcobject.objective_title[0] )
        #print "response_email_inputfield " + response_email_inputfield
        #util.waitForElementToBePresent(response_email_inputfield)
        #self.assertTrue(util.isElementPresent(response_email_inputfield), "do not see the firts response owner email textfield presented")
        #util.inputTextIntoField("jeff@reciprocitylabs.com", response_email_inputfield)

        # C.    Click on +PBC Response link to create a new Documentation Response
        response_add_button = element.audit_pbc_request_expanded_content_add_response_button.replace("TITLE",grcobject.objective_title[0] )
        create_response_button = element.audit_pbc_request_expanded_content_create_response_button.replace("TITLE",grcobject.objective_title[0] )
        print "response_add_button " + response_add_button
        util.waitForElementToBePresent(response_add_button)
        self.assertTrue(util.isElementPresent(response_add_button), "do not see the +PBC Response button")
        print create_response_button
        util.hoverOverAndWaitFor(response_add_button,create_response_button)
        #util.waitForElementToBePresent(create_response_button)
        util.clickOn(create_response_button)
        
        #D.    Enter "This is a documentation response for Objective 1 for Auto Test of Audit Request"
        # E.    Confirm Assignee is populated with Audit lead name

        util.waitForElementToBePresent(element.audit_modal_audit_lead_input_field)
        self.assertTrue(util.isElementPresent(element.audit_modal_audit_lead_input_field), "can't see the Audit Lead input field")
        audit_auto_populated_audit_lead = util.getAnyAttribute(element.audit_modal_audit_lead_input_field,"value")
        self.assertTrue(element.audit_modal_audit_lead_value  in audit_auto_populated_audit_lead,"not correct Audit Lead value")
        do.createObject("Request", "This is a documentation response for Objective 1 for Auto Test of Audit Request",False)
        
        
        time.sleep(10)
       
if __name__ == "__main__":
    unittest.main()