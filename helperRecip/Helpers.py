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
from time import strftime


class Helpers(unittest.TestCase):
    element = Elements()
    util = WebdriverUtilities()
    #driver = webdriver.Firefox()

    def setUtils(self,util):
        self.util = util
    
    
    def runTest(self):
        pass
    
    def GetTimeId(self):
        return strftime("_%Y_%m_%d__%H_%M_%S")
    
    def Login(self):
        self.util.waitForElementToBePresent(self.element.login_button)
        self.assertTrue(self.util.isElementPresent(self.element.login_button), "can't see the login button")
        self.util.clickOnAndWaitFor(self.element.login_button, self.element.gmail_password_textfield)
        self.util.inputTextIntoField(config.username, self.element.gmail_userid_textfield)
        self.util.inputTextIntoField(config.password, self.element.gmail_password_textfield)
        self.util.clickOnAndWaitFor(self.element.gmail_submit_credentials_button, self.element.dashboard_title)
        
    def WaitForLeftNavToLoad(self):
        # temporary method that waits for the '...) to be replaced with numbers
        self.util.waitForElementNotToBePresent(self.element.left_nav_governance_controls_numbers_not_loaded)
        self.util.waitForElementNotToBePresent(self.element.left_nav_governance_contracts_numbers_not_loaded)
        self.util.waitForElementNotToBePresent(self.element.left_nav_governance_policies_numbers_not_loaded)
        self.util.waitForElementNotToBePresent(self.element.left_nav_governance_regulations_numbers_not_loaded)
        self.util.scroll() #temporary workaround to refresh the page which will make the title appear (known bug)
        
    def OpenCreateNewProgramWindow(self,add_program_button):
        self.assertTrue(self.util.isElementPresent(add_program_button), "can't see the add program button")
        self.util.clickOn(add_program_button)
        
    def OpenCreateNewRiskWindow(self,add_risk_button):
        self.assertTrue(self.util.isElementPresent(add_risk_button), "can't see the add Risk button")
        self.util.clickOn(add_risk_button)
        
    def OpenCreateNewGovernanceWindow(self, governance_object):
        governavce_nav_tab_link = self.element.governance_widget_nav_tabs_link.replace("OBJECT", governance_object)
        governance_add_object_button = self.element.governance_widget_object_add_button.replace("OBJECT", governance_object)
        self.util.clickOnAndWaitFor(governavce_nav_tab_link, governance_add_object_button)
        self.util.clickOn(governance_add_object_button)
        
    def OpenCreateNewBusinessObjectWindow(self, business_object):
        business_object_nav_tab_link = self.element.business_object_widget_nav_tabs_link.replace("OBJECT", business_object)
        business_object_add_object_button = self.element.business_object_add_button.replace("OBJECT", business_object)
        self.util.clickOnAndWaitFor(business_object_nav_tab_link, business_object_add_object_button)
        self.util.clickOn(business_object_add_object_button)
        
        
    def PopulateObjectTitle(self, object_title):
        
        self.assertTrue(self.util.isElementPresent(self.element.modal), "can't see the modal body")
        self.util.waitForElementToBePresent2(self.element.modal_title_textfield)
        self.assertTrue(self.util.isElementPresent(self.element.modal_title_textfield), "can't access the input testfiled")
        self.util.inputTextIntoField(object_title, self.element.modal_title_textfield)
        self.util.inputTextIntoField(" ", self.element.modal_owner_textfield) #need this click to activate Save button
        self.util.typeIntoFrame2("alhdsfsfjcsdfdsjnfvmdfnvm cnmnv mfngvkdfnmnvmfdgnvmdnfmgm abala")

        
        
    def SaveObjectData(self):
        self.assertTrue(self.util.isElementPresent(self.element.modal_save_button), "do not see the Save button")
        self.util.clickOnByTextLink("Save")

        
        
        
        
        
        
    def VerifyObjectIsCreated(self, widget, object_title): 
        #this helper method is generic for any type 
        last_created_object_in_widget_element = self.element.dashboard_widget_last_created_object.replace("WIDGET", widget).replace("OBJECT_TITLE", object_title)
        print last_created_object_in_widget_element
        self.util.waitForElementToBePresent(last_created_object_in_widget_element)
        self.assertTrue(self.util.isElementPresent(last_created_object_in_widget_element), "do not see the newly created object in " + widget)
        return last_created_object_in_widget_element
    
    def NavToWidgetInfoPage(self,widget, object_title):
        object_title_link = self.element.widget_link_to_created_object.replace("OBJECT_TITLE", object_title)
        self.assertTrue(self.util.isElementPresent(object_title_link), "do not see the newly created object link " )
        self.util.clickOn(object_title_link)
        view_link = self.element.widget_view_link.replace("WIDGET", widget)
        self.assertTrue(self.util.isElementPresent(view_link), "do not see the View button")
        print view_link
        self.util.clickOn(view_link)
        
        
    def OpenEditWindow(self, edit_link):
        self.util.waitForElementToBePresent2(edit_link)
        self.assertTrue(self.util.isElementPresent(edit_link), "do not see the Edit button")
        self.util.clickOn(edit_link)
        self.util.waitForElementToBePresent2(self.element.object_title)
        self.assertTrue(self.util.isElementPresent(self.element.object_title), "do not see object_title in the edit window")
       
    #def PopulateObjectInEditWindow(self, name):
    def ShowHiddenValues(self):
        self.util.clickOnAndWaitFor(self.element.edit_window_show_hidden_fields_link, self.element.object_code)
    
    def PopulateObjectInEditWindow(self, name, grcobject_elements,grcobject_values ):
        #self.util.switch_to_active_element()
        self.util.waitForElementToBePresent(self.element.object_title)
        self.ShowHiddenValues()
        """
        self.util.inputTextIntoField(name+"-edited" ,self.element.object_title)
        #self.util.switchFrame("wysihtml5-sandbox")
        #self.util.inputTextIntoField("description for " + name, self.element.object_description)
        #self.util.focus()
        self.util.inputTextIntoField("owner " + name, self.element.object_owner)
        self.util.inputTextIntoField("https://www.google.com/", self.element.object_url)
        self.util.inputTextIntoField("PROGRAM" + name, self.element.object_code)
        self.util.inputTextIntoField("organization " + name, self.element.object_organization)
        self.util.inputTextIntoField("scope " + name, self.element.object_scope)
        self.assertTrue(self.util.isElementPresent(self.element.modal_save_button), "do not see the Save button")
        self.util.clickOnByTextLink("Save")
        """

        
        #self.ShowAdvance()   
        for key,xpath in grcobject_elements.iteritems():  
            if grcobject_values[key]=="":
                grcobject_values[key]=key+"_"+name+ "_edited"
            if key == "title":
                grcobject_values[key] = name + "_edited" 
            print key, xpath ,  grcobject_values[key]       
            self.util.waitForElementToBePresent2(xpath)
            if key == "kind":
                self.util.selectFromDropdownNew(xpath, grcobject_values[key] )
            else: 
                #if key == "description":
                #    self.util.switchFrame("wysihtml5-sandbox")
                #    self.util.typeIntoFrame(grcobject_values[key])
                #else:
                self.util.inputTextIntoField(grcobject_values[key] ,xpath)
        self.util.inputTextIntoField("testrecip@gmail.com", self.element.modal_owner_textfield)
        self.assertTrue(self.util.isElementPresent(self.element.modal_save_button), "do not see the Save button")
        self.util.waitForElementToBePresent2(self.element.modal_save_button) # hack for make the Save button clickable
        self.util.clickOn("//div[@class=\"confirm-buttons\"]/a[@data-toggle=\"modal-submit\"]")
        time.sleep(2)
       
 
    def verifyObjectValues(self, grcobject_elements,grcobject_values):
        for key,xpath in grcobject_elements.iteritems(): 
            new_value = self.util.getAnyAttribute(xpath, "value")
            self.assertTrue(new_value == grcobject_values[key], "the value of " + key + " should be " + grcobject_values[key] + " but it is " + new_value )
             
          
            
            
                
            
       
            
        
        
        
        
        
        
        
        
    
        