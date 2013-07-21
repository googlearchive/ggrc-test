'''
Created on Jun 19, 2013

@author: diana.tzinov
'''
import sys
from Elements import Elements
from WebdriverUtilities import WebdriverUtilities
import time
import string
import unittest
import config


class Helpers(unittest.TestCase):
    element = Elements()
    util = WebdriverUtilities()
    #driver = webdriver.Firefox()

    def setUtils(self,util):
        self.util = util
    
    
    def runTest(self):
        pass
    
    def Login(self):
        self.util.waitForElementToBePresent(self.element.login_button)
        self.assertTrue(self.util.isElementPresent(self.element.login_button), "can't see the login button")
        self.util.clickOnAndWaitFor(self.element.login_button, self.element.gmail_password_textfield)
        self.util.inputTextIntoField(config.username, self.element.gmail_userid_textfield)
        self.util.inputTextIntoField(config.password, self.element.gmail_password_textfield)
        self.util.clickOnAndWaitFor(self.element.gmail_submit_credentials_button, self.element.dashboard_title)
        
    def WaitForLeftNavToLoad(self):
        # temporary method that waits for the '...) to be replaced with numbers
        self.util.waitForElementNotToBePresent(self.element.left_nav_governance_controls_numbers_not_loaded, 20)
        self.util.waitForElementNotToBePresent(self.element.left_nav_governance_contracts_numbers_not_loaded, 20)
        self.util.waitForElementNotToBePresent(self.element.left_nav_governance_policies_numbers_not_loaded, 20)
        self.util.waitForElementNotToBePresent(self.element.left_nav_governance_regulations_numbers_not_loaded, 20)
        
    def OpenCreateNewProgramWindow(self,add_program_button):
        self.assertTrue(self.util.isElementPresent(add_program_button), "can't see the add program button")
        self.util.clickOn(add_program_button)
        
        
    def OpenCreateNewGovernanceWindow(self, governance_object):
        governavce_nav_tab_link = self.element.governance_widget_nav_tabs_link.replace("OBJECT", governance_object)
        governance_add_object_button = self.element.governance_widget_object_add_button.replace("OBJECT", governance_object)
        self.util.clickOnAndWaitFor(governavce_nav_tab_link, governance_add_object_button)
        self.util.clickOn(governance_add_object_button)
        
        
        
    def PopulateProgramData(self, program_title):
        
        self.assertTrue(self.util.isElementPresent(self.element.program_modal), "can't see the modal body")
        self.util.waitForElementToBePresent(self.element.program_modal_title_textfield, 30)
        self.assertTrue(self.util.isElementPresent(self.element.program_modal_title_textfield), "can't access the input testfiled")
        self.util.inputTextIntoField(program_title, self.element.program_modal_title_textfield)
        self.util.inputTextIntoField(" ", self.element.program_modal_owner_textfield) #need this click to activate Save button
        self.assertTrue(self.util.isElementPresent(self.element.modal_save_button), "do not see the Save button")
        self.util.clickOnByTextLink("Save")

        
        
        
    def PopulateGovernanceData(self, contract_title):
        
        self.assertTrue(self.util.isElementPresent(self.element.program_modal), "can't see the modal body")
        self.util.switch_to_active_element()
        self.util.waitForElementToBePresent(self.element.program_modal_title_textfield, 30)
        self.assertTrue(self.util.isElementPresent(self.element.program_modal_title_textfield), "can't access the input testfiled")
        self.util.inputTextIntoField(contract_title, self.element.program_modal_title_textfield)
        self.util.inputTextIntoField(" ", self.element.program_modal_owner_textfield)
        #self.util.clickOn(self.element.program_modal_owner_textfield)
        self.assertTrue(self.util.isElementPresent(self.element.modal_save_button), "do not see the Save button")
        self.util.clickOnByTextLink("Save")

        
        
        
        
        
    def VerifyObjectIsCreated(self, widget, object_title): 
        #this helper method is generic for any type 
        last_created_object_in_widget_element = self.element.dashboard_widget_last_created_object.replace("WIDGET", widget).replace("OBJECT_TITLE", object_title)
        self.util.waitForElementToBePresent(last_created_object_in_widget_element)
        self.assertTrue(self.util.isElementPresent(last_created_object_in_widget_element), "do not see the newly created object in " + widget)
        return last_created_object_in_widget_element
    
    def NavToWidgetInfoPage(self,link):
        self.assertTrue(self.util.isElementPresent(link), "do not see the newly created object link " )
        self.util.clickOnAndWaitFor(link, self.element.widget_edit_page_edit_link)
        self.assertTrue(self.util.isElementPresent(self.element.widget_edit_page_edit_link), "do not see the edit button")
        
    def OpenEditWindow(self):
        self.assertTrue(self.util.isElementPresent(self.element.widget_edit_page_edit_link), "do not see the edit button")
        self.util.clickOn(self.element.widget_edit_page_edit_link)
        self.util.waitForElementToBePresent(self.element.object_title)
        self.assertTrue(self.util.isElementPresent(self.element.object_title), "do not see object_title in the edit window")
       
    def PopulateProgramInEditWindow(self, name):
        self.util.switch_to_active_element()
        self.util.waitForElementToBePresent(self.element.object_title)
        #self.util.switch_to_active_element()
        time.sleep(2)
        self.util.clickOnAndWaitFor(self.element.edit_window_show_hidden_fields_link, self.element.object_scope)
        self.util.inputTextIntoField(name+"-edited" ,self.element.object_title)
        self.util.inputTextIntoField("owner " + name, self.element.object_owner)
        
        #self.util.waitForElementToBePresent(self.element.object_code)
        #self.util.inputTextIntoField("PROGRAM" + name, self.element.object_code)
        #self.util.waitForElementToBePresent(self.element.object_organization)
        self.util.inputTextIntoField("organization " + name, self.element.object_organization)
        #self.util.waitForElementToBePresent(self.element.object_scope)
        self.util.inputTextIntoField("scope " + name, self.element.object_scope)
        self.assertTrue(self.util.isElementPresent(self.element.modal_save_button), "do not see the Save button")
        self.util.clickOnByTextLink("Save")

        """
        #self.ShowAdvance()   
        #for key,xpath in grcobject_elements.iteritems():  
            if grcobject_values[key]=="":
                grcobject_values[key]=key+"_"+name+ "_edited"
            if key == "title":
                grcobject_values[key] = name + "_edited" 
            print key, xpath ,  grcobject_values[key]       
            self.util.inputTextIntoField(grcobject_values[key] ,xpath)
        """
            
        
          
            
            
                
            
       
            
        
        
        
        
        
        
        
        
    
        