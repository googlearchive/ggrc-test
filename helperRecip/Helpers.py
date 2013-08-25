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
from selenium.webdriver.common.by import By


class Helpers(unittest.TestCase):
    element = Elements()
    util = WebdriverUtilities()
    #driver = webdriver.Firefox()

    def setUtils(self,util):
        self.util = util
    
    
    def runTest(self):
        pass
    
    def GetTimeId(self):
        return strftime("_%Y_%m_%d_%H_%M_%S")
    
    def Login(self):
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
        
    def GenerateNameForTheObject(self,grc_object):
        random_number= self.GetTimeId()
        name = grc_object + "-auto-test"+random_number
        return name
        
    def ExpandLeftNavMenuForObject(self, grc_object):
        object_left_nav_section_object_link = self.element.left_nav_expand_object_section_link.replace("OBJECT", grc_object)
        object_left_nav_section_object_add_button = self.element.left_nav_object_section_add_button.replace("OBJECT", grc_object)
        #self.util.clickOnAndWaitFor(object_left_nav_section_object_link, object_left_nav_section_object_add_button)
        #self.util.clickOn(object_left_nav_section_object_link)
        #self.util.waitForElementToBeClickable(object_left_nav_section_object_link)
        self.util.waitForElementToBeVisible(object_left_nav_section_object_link)
        self.util.clickOn(object_left_nav_section_object_link)
        self.util.waitForElementToBeVisible(object_left_nav_section_object_add_button)
        #self.util.waitForElementToBeClickable(object_left_nav_section_object_add_button)
        
    def CreateObject(self, grc_object):
        self.assertTrue(self.util.isElementPresent(self.element.dashboard_title), "no dashboard page found")
              
        grc_object_name = self.GenerateNameForTheObject(grc_object)
        self.OpenCreateNewObjectWindow(grc_object) 
        self.PopulateNewObjectData(grc_object_name)
        self.SaveObjectData()
        last_created_object_link = self.VerifyObjectIsCreated(grc_object, grc_object_name)
        return last_created_object_link

    def OpenCreateNewObjectWindow(self, grc_object):
        object_left_nav_section_object_link = self.element.left_nav_expand_object_section_link.replace("OBJECT", grc_object)
        object_left_nav_section_object_add_button = self.element.left_nav_object_section_add_button.replace("OBJECT", grc_object)
        self.util.waitForElementToBeClickable(object_left_nav_section_object_link)
        self.assertTrue(self.util.isElementPresent(object_left_nav_section_object_link), "can't click on the object left nav link")
        self.util.clickOn(object_left_nav_section_object_link)
        self.util.waitForElementToBeClickable(object_left_nav_section_object_add_button)
        self.assertTrue(self.util.isElementPresent(object_left_nav_section_object_add_button), "can't click on CreateNew link")
        #self.util.clickOnAndWaitFor(object_left_nav_section_object_link, object_left_nav_section_object_add_button)
        self.util.clickOn(object_left_nav_section_object_add_button)
        


        
    def PopulateNewObjectData(self, object_title):
        
        # Make sure window is there
        self.util.waitForElementToBeVisible(self.element.modal_window)
        #self.assertTrue(self.util.isElementPresent(self.element.modal), "can't see the modal body")
        
        # Populate title
        self.util.waitForElementToBeVisible(self.element.modal_window_title_textfield)
        self.assertTrue(self.util.isElementPresent(self.element.modal_window_title_textfield), "can't access the input textfiled")
        self.util.inputTextIntoField(object_title, self.element.modal_window_title_textfield)
        self.util.inputTextIntoField("", self.element.modal_window_owner_textfield) #need this click to activate Save button
        # Populate Description
        #self.util.typeIntoFrame("description-"+object_title)

        
        
    def SaveObjectData(self):
        #self.util.inputTextIntoField("testrecip@gmail.com", self.element.modal_owner_textfield) #need this click to activate Save button
        self.assertTrue(self.util.isElementPresent(self.element.modal_window_save_button), "do not see the Save button")
        self.util.clickOnSave(self.element.modal_window_save_button)
        self.util.waitForElementNotToBePresent(self.element.modal_window)

        
        
        
        
    def closeAndOpenObjectSection(self, link):
        self.util.clickOn(link)
        time.sleep(1)
        self.util.clickOn(link)
        
    def VerifyObjectIsCreated(self, widget, object_title): 
        #this helper method is generic for any type 
        object_left_nav_section_object_link = self.element.left_nav_expand_object_section_link.replace("OBJECT", widget)
        self.closeAndOpenObjectSection(object_left_nav_section_object_link)
        last_created_object_link = self.element.left_nav_last_created_object_link.replace("SECTION", widget).replace("OBJECT_TITLE", object_title)
        self.util.waitForElementToBeVisible(last_created_object_link)
        self.assertTrue(self.util.isElementPresent(last_created_object_link), "do not see the newly created object in " + widget)
        return last_created_object_link
    
    def NavigateToObjectAndOpenObjectEditWindow(self,widget,object_title_link):
        object_left_nav_section_object_link = self.element.left_nav_expand_object_section_link.replace("OBJECT", widget)
        self.closeAndOpenObjectSection(object_left_nav_section_object_link)
        #self.closeAndOpenObjectSection(object_left_nav_section_object_link)
        self.util.waitForElementToBeVisible(object_title_link)
        self.assertTrue(self.util.isElementPresent(object_title_link), "do not see the newly created object link " )
        self.util.clickOn(object_title_link)
        self.assertTrue(self.util.isElementPresent(self.element.object_detail_page_info_section), "do not see object info section")
        self.util.hoverOver(self.element.object_detail_page_info_section)
        self.util.waitForElementToBeVisible(self.element.object_info_page_edit_link)
        self.assertTrue(self.util.isElementPresent(self.element.object_info_page_edit_link), "do not see the Edit button")
        self.util.clickOn(self.element.object_info_page_edit_link)
        self.util.waitForElementToBeVisible(self.element.modal_window)
        self.util.waitForElementToBeVisible(self.element.object_title)
        self.assertTrue(self.util.isElementPresent(self.element.object_title), "do not see object_title in the edit window")
        
    def OpenObjectEditWindow(self):
        self.util.hoverOver(self.element.object_detail_page_info_section)  
        self.util.waitForElementToBeVisible(self.element.object_info_page_edit_link)
        self.assertTrue(self.util.isElementPresent(self.element.object_info_page_edit_link), "do not see the Edit button")
        self.util.clickOn(self.element.object_info_page_edit_link)
        self.util.waitForElementToBeVisible(self.element.modal_window)
        self.util.waitForElementToBeVisible(self.element.object_title)
        self.assertTrue(self.util.isElementPresent(self.element.object_title), "do not see object_title in the edit window")
       
    
    def ShowHiddenValues(self):
        self.util.clickOnAndWaitFor(self.element.modal_window_show_hidden_fields_link, self.element.object_code)
    
    def PopulateObjectInEditWindow(self, name, grcobject_elements,grcobject_values ):
        self.util.waitForElementToBeVisible(self.element.object_title)
        self.ShowHiddenValues() 
        for key,xpath in grcobject_elements.iteritems():  
            #print key, xpath ,  grcobject_values[key] 
            self.util.waitForElementToBeVisible(xpath) 
            if key == "kind":
                option = self.util.getTextFromXpathString(self.element.object_kind + "/option[" + str(grcobject_values[key]) + "]")
                self.selectFromDropdownOption(self.element.object_kind, grcobject_values[key])  
                grcobject_values[key]=option
            if key=="code":
                grcobject_values[key] = self.util.getAnyAttribute(self.element.object_code, "value") + "_edited"
                self.util.inputTextIntoField(grcobject_values[key] ,xpath)
            if key == "title":
                grcobject_values[key] = name + "_edited" 
                self.util.inputTextIntoField(grcobject_values[key] ,xpath)
            if key == "owner":
                grcobject_values[key] = "testrecip@gmail.com" 
                self.util.inputTextIntoField(grcobject_values[key] ,xpath)
            if key == "description":
                grcobject_values[key]=key+"_"+name+ "_edited"
                self.util.typeIntoFrame(grcobject_values[key], self.element.modal_window_description_frame) 
            if key=="url":
                grcobject_values[key] = "http://www.google.com"
                self.util.inputTextIntoField(grcobject_values[key] ,xpath)
                
        self.util.inputTextIntoField("testrecip@gmail.com" , self.element.modal_window_owner_textfield)
        self.assertTrue(self.util.isElementPresent(self.element.modal_window_save_button), "do not see the Save button")
        self.util.waitForElementToBeVisible(self.element.modal_window_save_button) # hack for make the Save button clickable
        self.SaveObjectData()
        
    def selectFromDropdownOption(self,select_element,option_number):
        self.assertTrue(self.util.isElementPresent(select_element), "do not see the dropdown")
        self.util.waitForElementToBeVisible(select_element)
        option_to_be_selected = self.util.getTextFromXpathString(select_element + "/option[" + str(option_number) + "]")
        #print option_to_be_selected
        self.util.selectFromDropdownUntilSelected(select_element, option_to_be_selected)
        time.sleep(3)
        
       
 
    def verifyObjectValues(self, grcobject_elements,grcobject_values):
        for key,xpath in grcobject_elements.iteritems(): 
            #print "Inside verifyObjectValues, key=" + key + ", value="+grcobject_values[key]
            if key == "description":
                new_value = self.util.getTextFromFrame(self.element.modal_window_description_frame)

                #print "new_value for description=" + new_value
                #print "the value for description initially is " + grcobject_values[key]
                self.assertTrue(new_value == grcobject_values[key], "Verification ERROR: the value of " + key + " should be " + grcobject_values[key] + " but it is " + new_value )       
            elif key == "kind":                
                    new_value = self.util.getTextFromXpathString(self.element.object_kind_selected_option)
                    self.assertTrue(new_value == grcobject_values[key], "Verification ERROR: the value of " + key + " should be " + grcobject_values[key] + " but it is " + new_value )

            else:
                    new_value = self.util.getAnyAttribute(xpath, "value")
                    #print "new_value="+new_value
                    self.assertTrue(new_value == grcobject_values[key], "Verification ERROR: the value of " + key + " should be " + grcobject_values[key] + " but it is " + new_value )
            print "Verification OK: the value of " + key + " is "+grcobject_values[key] +", as expected." 
    
    def deleteObject(self):
        self.assertTrue(self.util.isElementPresent(self.element.modal_window_delete_button), "do not see the Delete button")
        #self.util.clickOnAndWaitFor(self.element.modal_window_delete_button,self.element.modal_window_confirm_delete_button)
        self.util.clickOn(self.element.modal_window_delete_button)
        time.sleep(1)
        #self.assertTrue(self.util.isElementPresent(self.element.modal_window_confirm_delete_button), "do not see the Confirm Delete button")
        self.util.clickOn(self.element.modal_window_confirm_delete_button)
        self.util.waitForElementNotToBePresent(self.element.modal_window)
     
            

            

        
        
        
        
        
        
        
        
    
        