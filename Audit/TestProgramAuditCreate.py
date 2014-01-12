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



class TestProgramAuditCreate(WebDriverTestCase):

    
    def testProgramAuditCreate(self):
        self.testname="TestProgramAuditCreate"
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
        ##objectiveID[0]=int(f.readline().strip("\n"))
        #objectiveID[1]=int(f.readline().strip("\n"))
        #objectiveID[2]=int(f.readline().strip("\n"))
        #print program_name
        #print objectiveID
        
        
        
        # 1.  Navigate to the Program page created in Audit Part 1
        #first_program_in_lhn = '//ul[@class="top-level"]//li[contains(@data-model-name,"Program")]//li[contains(.,"NAME")]/a'.replace("NAME", program_name)
        #print first_program_in_lhn
        do.navigateToObjectWithSearch(program_name,"Program")
        util.max_screen()
        
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
        util.max_screen()
        #verifying the 3 objectives
        
        for objective_title in grcobject.objective_title:
            objective_title_element = element.audit_pbc_request.replace("TITLE", objective_title)
            print objective_title_element
            util.waitForElementToBePresent(objective_title_element)
            self.assertTrue(util.isElementPresent(objective_title_element), "do not see the pbc request " + objective_title_element )
        
        do.waitForAlertSuccessMessages()
        
        
if __name__ == '__main__':
    pass