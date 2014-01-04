'''
Created on Jun 19, 2013

@author: diana.tzinov
'''
import sys
from Elements import Elements
from WebdriverUtilities import WebdriverUtilities
import time,  calendar
import datetime
from datetime import timedelta
from datetime import date
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
    
    def getTimeId(self):
        return strftime("_%Y_%m_%d_%H_%M_%S")
    
    def login(self):
        self.assertTrue(self.util.isElementPresent(self.element.login_button), "can't see the login button")
        if "localhost" in config.url:
            self.util.clickOnAndWaitFor(self.element.login_button, self.element.dashboard_title)
        else:
            self.util.clickOnAndWaitFor(self.element.login_button, self.element.gmail_password_textfield)
            self.assertTrue(self.util.isElementPresent(self.element.gmail_password_textfield), "can't see the password textfield")
            self.util.inputTextIntoField(config.username, self.element.gmail_userid_textfield)
            self.assertTrue(self.util.isElementPresent(self.element.gmail_userid_textfield), "can't see the userid textfield")
            self.util.inputTextIntoField(config.password, self.element.gmail_password_textfield)
            self.util.clickOnAndWaitFor(self.element.gmail_submit_credentials_button, self.element.dashboard_title)
        # need to check for permission screen, and if it's there
        # de-select "Remember..." if checked; then click on "Allow"
        if self.util.isElementPresent(self.element.g_accounts_login_prompt):
            checkbox = self.util.driver.find_element_by_xpath(self.element.g_accounts_remember_box)
            if checkbox.get_attribute("checked") == "true":
                self.util.clickOn(self.element.g_accounts_remember_box)
            self.util.clickOn(self.element.g_accounts_allow)
        # need to check for chrome login screen, 
        # and if it's there, click on "skip for now"
        if self.util.isElementPresent(self.element.chrome_login_prompt):
            self.util.clickOn(self.element.chrome_login_skip_button)
            if self.util.isElementPresent(self.element.google_permission_prompt):
                self.util.clickOn(self.element.google_permission_remember)
                self.util.clickOn(self.element.google_permission_yes)
        self.assertTrue(self.util.waitForElementToBePresent(self.element.dashboard_title),"ERROR inside login(): can't see dashboard_title")
        
    def waitForLeftNavToLoad(self):
        # temporary method that waits for the '...) to be replaced with numbers
        self.util.waitForElementNotToBePresent(self.element.left_nav_governance_controls_numbers_not_loaded)
        self.util.waitForElementNotToBePresent(self.element.left_nav_governance_contracts_numbers_not_loaded)
        self.util.waitForElementNotToBePresent(self.element.left_nav_governance_policies_numbers_not_loaded)
        self.util.waitForElementNotToBePresent(self.element.left_nav_governance_regulations_numbers_not_loaded)
        self.util.scroll() #temporary workaround to refresh the page which will make the title appear (known bug)
        
    def generateNameForTheObject(self,grc_object):
        random_number= self.getTimeId()
        name = grc_object + "-auto-test"+random_number
        return name
        
    def expandLeftNavMenuForObject(self, grc_object):
        object_left_nav_section_object_link = self.element.left_nav_expand_object_section_link.replace("OBJECT", grc_object)
        self.assertTrue(self.util.waitForElementToBePresent(object_left_nav_section_object_link),"ERROR inside expandLeftNavMenuForObject(): can't see the LHN link for "+ grc_object)
        result=self.util.clickOn(object_left_nav_section_object_link)
        time.sleep(10)
        self.assertTrue(result,"ERROR in expandLeftNavMenuForObject(): could not click on LHN link for "+grc_object)
        object_left_nav_section_object_add_button = self.element.left_nav_object_section_add_button.replace("OBJECT", grc_object)
        self.assertTrue(self.util.waitForElementToBePresent(object_left_nav_section_object_add_button), "ERROR inside expandLeftNavMenuForObject(): can't see the LHN Create New link for "+ grc_object)
        
        
    def createObject(self, grc_object, object_name="", private_checkbox="unchecked", open_new_object_window_from_lhn = True, owner=""):
        self.closeOtherWindows()
        if object_name == "":
            grc_object_name = self.generateNameForTheObject(grc_object)
        else:
            grc_object_name = object_name
        #in the standard create object flow, a new window gets open via Create link in the LHN, in audit tests the new object gets created via + link, and that's why
        #openCreateNewObjectWindowFromLhn have to be skipped
        if open_new_object_window_from_lhn:
            self.openCreateNewObjectWindowFromLhn(grc_object) 
        self.populateNewObjectData(grc_object_name,owner)
        if private_checkbox == "checked":
            self.util.clickOn(self.element.modal_window_private_checkbox)
        self.saveObjectData()
        #in the standard create object flow, verify the new object is created happens vi LHN, for audits tests this verification should happen in the mapping modal window
        if open_new_object_window_from_lhn:
            # uncheck box if it is checked
            self.uncheckMyWork()
            last_created_object_link = self.verifyObjectIsCreatedinLHN(grc_object, grc_object_name)
            return last_created_object_link
        else:
            print "verifying create object in mapping window"
            #commented the verifycation for now
            last_created_object_link = self.verifyObjectIsCreatedInSections(grc_object_name)
        print "Object created successfully."
        
        
    def NewResponseCreate(self, object_name):
        self.closeOtherWindows()
        # Make sure window is there
        self.util.waitForElementToBeVisible(self.element.modal_window)
        self.assertTrue(self.util.isElementPresent(self.element.modal_window), "can't see modal dialog window for create new object")

        #self.assertTrue(self.util.isElementPresent(self.element.modal), "can't see the modal body")
        
        # Populate title
        self.util.waitForElementToBeVisible(self.element.response_title)
        self.assertTrue(self.util.isElementPresent(self.element.response_title), "can't access the input textfield")
        
        self.util.inputTextIntoField(object_name, self.element.response_title)

        self.saveObjectData()

    def openCreateNewObjectWindowFromLhn(self, grc_object):
       
        object_left_nav_section_object_link = self.element.left_nav_expand_object_section_link.replace("OBJECT", grc_object)
        self.assertTrue(self.util.waitForElementToBePresent(object_left_nav_section_object_link), "ERROR inside openCreateNewObjectWindowFromLhn():can't see the LHN link for "+ grc_object)
        result=self.util.clickOn(object_left_nav_section_object_link)
        self.assertTrue(result,"ERROR in openCreateNewObjectWindowFromLhn(): could not click on LHN link for "+grc_object)
        object_left_nav_section_object_add_button = self.element.left_nav_object_section_add_button.replace("OBJECT", grc_object)
        self.assertTrue(self.util.waitForElementToBePresent(object_left_nav_section_object_add_button), "ERROR inside openCreateNewObjectWindowFromLhn():can't see the LHN Create New link for "+ grc_object)
        result=self.util.clickOn(object_left_nav_section_object_add_button)
        self.assertTrue(result,"ERROR in openCreateNewObjectWindowFromLhn(): could not click on LHN Create New link for "+grc_object)
        


        
    def populateNewObjectData(self, object_title, owner=""):
        self.closeOtherWindows()
        # Make sure window is there
        self.util.waitForElementToBeVisible(self.element.modal_window)
        self.assertTrue(self.util.isElementPresent(self.element.modal_window), "can't see modal dialog window for create new object")

        #self.assertTrue(self.util.isElementPresent(self.element.modal), "can't see the modal body")
        
        # Populate title
        self.util.waitForElementToBeVisible(self.element.object_title)
        self.assertTrue(self.util.isElementPresent(self.element.object_title), "can't access the input textfield")
        
        self.util.inputTextIntoField(object_title, self.element.object_title)
        ##self.util.waitForElementToBeVisible(self.element.object_owner)
        ##self.assertTrue(self.util.isElementPresent(self.element.object_owner), "can't access the owner input textfield")
        ##self.util.inputTextIntoField(owner, self.element.object_owner) #need this click to activate Save button
        # *** END code for inputting owner *** #
        """
        owner_email = "testrecip@gmail.com"
        self.util.inputTextIntoField(
            owner_email,
            Elements.object_owner
        )
        matching_email_selector = self.element.autocomplete_list_element_with_email.replace("EMAIL",owner_email)
        self.util.waitForElementToBeVisible(matching_email_selector)
        self.util.clickOn(matching_email_selector)
        # *** END code for inputting owner *** #

        # Populate Description
        #self.util.typeIntoFrame("description-"+object_title)
        """
        
        
    def saveObjectData(self):
        #self.util.inputTextIntoField("testrecip@gmail.com", self.element.modal_owner_textfield) #need this click to activate Save button
        self.util.waitForElementToBePresent(self.element.modal_window_save_button)
        self.assertTrue(self.util.isElementPresent(self.element.modal_window_save_button), "do not see the Save button")
        self.util.clickOnSave(self.element.modal_window_save_button)
        #status=self.util.waitForElementNotToBePresent(self.element.modal_window,100)
        #self.assertTrue(status,"Save operation taking too long, modal window still visible after 100 seconds")
        #self.waitForLeftNavToLoad()

        

        
    def verifyObjectIsCreatedinLHN(self, widget, object_title): 
        #this helper method is generic for any type and verifies that object is created and can be clicked in LHN
        
        # Refresh the page
        
        self.util.refreshPage()
        
        # Wait for the object section link to appear in the left nav (e.g. Programs, Products, Policies, etc.)
        
        object_left_nav_section_object_link = self.element.left_nav_expand_object_section_link.replace("OBJECT", widget)
        self.assertTrue(self.util.waitForElementToBePresent(object_left_nav_section_object_link), "ERROR inside verifyObjectIsCreatedinLHN(): do not see the LHN link for " + widget)

        # Click on the object section link in the left nav
        
        result=self.util.clickOn(object_left_nav_section_object_link)
        self.assertTrue(result,"ERROR in verifyObjectIsCreatedinLHN(): could not click on LHN link for "+widget)
        
        # Wait for the newly-created object link to appear in the left nav (e.g. System-auto-test_2013_08_25_13_47_50)

        last_created_object_link = self.element.left_nav_last_created_object_link.replace("SECTION", widget).replace("OBJECT_TITLE", object_title)
        self.assertTrue(self.util.waitForElementToBePresent(last_created_object_link), "ERROR inside verifyObjectIsCreatedinLHN(), do not see the newly created object in " + widget)
        return last_created_object_link
    
    
    def verifyObjectIsCreatedInSections(self, object_title):
        self.util.waitForElementToBePresent(self.element.mapping_modal_selector_list_first_object_link)
        self.assertTrue(self.util.isElementPresent(self.element.mapping_modal_selector_list_first_object_link), "can't see the first link in the mapping modal window")
        last_created_object_link =  self.util.getTextFromXpathString(self.element.mapping_modal_selector_list_first_object_link)
        print "the newly created object is " + last_created_object_link
        self.assertEquals(last_created_object_link, object_title, "the newly created object is not in Mapping Modal Window")
        return last_created_object_link
    
    
    def createSectionFor(self, object,object_id,section_title):
        section_add_link = self.element.mapped_object_area_section_add_link.replace("OBJECT", object).replace("ID", object_id)
        self.util.waitForElementToBePresent(section_add_link)
        self.assertTrue(self.util.isElementPresent(section_add_link), "cannot see section add + link")
        self.util.hoverOverAndWaitFor(section_add_link,self.element.section_create_link)
        self.util.clickOn(section_add_link)
        self.assertTrue(self.util.isElementPresent(self.element.section_create_link), "cannot see section create link")
        self.util.clickOn(self.element.section_create_link)
        # Make sure window is there
        self.util.waitForElementToBeVisible(self.element.modal_window)
        self.assertTrue(self.util.isElementPresent(self.element.modal_window), "can't see modal dialog window for create new object")

        #self.assertTrue(self.util.isElementPresent(self.element.modal), "can't see the modal body")
        
        # Populate title
        self.util.waitForElementToBeVisible(self.element.object_title)
        self.assertTrue(self.util.isElementPresent(self.element.object_title), "can't access the input textfield")
        self.util.inputTextIntoField(section_title, self.element.object_title)
        self.util.waitForElementToBeVisible(self.element.object_title)
        #entering the descriptiom
        frame_element = self.element.object_iFrame.replace("FRAME_NAME","description")

        self.util.typeIntoFrame(self.element.theLongTextDescription1, frame_element) 
        self.saveObjectData()
        
        
    def createObjectives(self, objective_title, description):
        self.util.waitForElementToBeVisible(self.element.modal_window)
        self.assertTrue(self.util.isElementPresent(self.element.modal_window), "can't see modal dialog window for create new object")

        #self.assertTrue(self.util.isElementPresent(self.element.modal), "can't see the modal body")
        
        # Populate title
        self.util.waitForElementToBeVisible(self.element.object_title)
        self.assertTrue(self.util.isElementPresent(self.element.object_title), "can't access the input textfield")
        self.util.inputTextIntoField(objective_title, self.element.object_title)
        self.util.waitForElementToBeVisible(self.element.object_title)
        #entering the descriptiom
        frame_element = self.element.object_iFrame.replace("FRAME_NAME","description")
        self.util.typeIntoFrame(description, frame_element) 
        self.saveObjectData()
        
        
    def navigateToObject(self, section, object_title_link):
           # Refresh the page
        
        #self.util.refreshPage()
        
        # Wait for the object section link to appear in the left nav (e.g. Programs, Products, Policies, etc.)
        
        object_left_nav_section_object_link = self.element.left_nav_expand_object_section_link.replace("OBJECT", section)
        self.assertTrue(self.util.waitForElementToBePresent(object_left_nav_section_object_link),"ERROR in navigateToObject(): can't see LHN link for "+section)
        
        # Click on the object section link in the left nav
        
        #result=self.util.clickOn(object_left_nav_section_object_link)
        #self.assertTrue(result,"ERROR in navigateToObject(): could not click on LHN link for "+section)        

        # Wait for the newly-edited object link to appear, then click on it        
        
        self.assertTrue(self.util.waitForElementToBePresent(object_title_link), "ERROR inside navigateToObject(): do not see object  " + object_title_link + " in lhn" )       
        result=self.util.clickOn(object_title_link)
        self.assertTrue(result,"ERROR in navigateToObject(): could not click on object in LHN "+object_title_link)
        
        
    def navigateToObjectWithExpadingLhnSection(self, section, object_title_link):
           # Refresh the page
        
        #self.util.refreshPage()
        
        # Wait for the object section link to appear in the left nav (e.g. Programs, Products, Policies, etc.)
        
        self.uncheckMyWork()
        
        object_left_nav_section_object_link = self.element.left_nav_expand_object_section_link.replace("OBJECT", section)
        self.assertTrue(self.util.waitForElementToBePresent(object_left_nav_section_object_link),"ERROR in navigateToObject(): can't see LHN link for "+section)
        
        # Click on the object section link in the left nav
        
        self.util.clickOn(object_left_nav_section_object_link)
        #self.assertTrue(result,"ERROR in navigateToObject(): could not click on LHN link for "+section)        

        # Wait for the newly-edited object link to appear, then click on it        
        self.util.scrollIntoView(object_title_link)
        self.assertTrue(self.util.waitForElementToBePresent(object_title_link), "ERROR inside navigateToObject(): do not see object  " + object_title_link + " in lhn" )       
        result=self.util.clickOn(object_title_link)
        self.assertTrue(result,"ERROR in navigateToObject(): could not click on object in LHN "+object_title_link)
        
    def navigateToObjectWithSearch(self, search_term, section):
        #self.searchFor(search_term)
        object_left_nav_section_object_link_with_one_result = self.element.left_nav_expand_object_section_link_one_result_after_search.replace("OBJECT", section)
        self.searchFor(search_term)
        self.util.waitForElementToBePresent(object_left_nav_section_object_link_with_one_result)
        self.assertTrue(self.util.isElementPresent(object_left_nav_section_object_link_with_one_result), "the search did not return one result as it's supposed to" )
        object_left_nav_section_object_link = self.element.left_nav_expand_object_section_link.replace("OBJECT", section)
        
        self.assertTrue(self.util.waitForElementToBePresent(object_left_nav_section_object_link),"ERROR in navigateToObject(): can't see LHN link for "+section)
        
        # Click on the object section link in the left nav
        self.util.clickOn(object_left_nav_section_object_link)        
        
        object_title_link = self.element.left_nav_last_created_object_link.replace("SECTION", section).replace("OBJECT_TITLE", search_term)       
        self.util.waitForElementToBePresent(object_title_link)
        self.assertTrue(self.util.isElementPresent(object_title_link), "ERROR inside navigateToObject(): do not see object  " + object_title_link + " in lhn" )
        result=self.util.clickOn(object_title_link)
        self.assertTrue(result,"ERROR in navigateToObject(): could not click on object in LHN "+object_title_link)
        
    
    def navigateToObjectAndOpenObjectEditWindow(self,section,object_title_link, refresh_page=True):

        self.closeOtherWindows()
        # Wait for the object section link to appear in the left nav (e.g. Programs, Products, Policies, etc.)
        
        object_left_nav_section_object_link = self.element.left_nav_expand_object_section_link.replace("OBJECT", section)
        self.assertTrue(self.util.waitForElementToBePresent(object_left_nav_section_object_link),"ERROR inside navigateToObjectAndOpenObjectEditWindow(): can't see object_left_nav_section_object_link")
        
        # Click on the object section link in the left nav
        
        #result=self.util.clickOn(object_left_nav_section_object_link)
        #self.assertTrue(True,"ERROR in navigateToObjectAndOpenObjectEditWindow(): could not click on link for "+section)        

        # Wait for the newly-edited object link to appear, then click on it        
        self.util.scrollIntoView(object_title_link)
        self.assertTrue(self.util.waitForElementToBePresent(object_title_link), "ERROR inside navigateToObjectAndOpenObjectEditWindow(): do not see the just edited object link " )       
        result=self.util.clickOn(object_title_link)
        self.assertTrue(result,"ERROR in navigateToObjectAndOpenObjectEditWindow(): could not click on just edited object link: "+object_title_link)
        
        # Wait for the object detail page info section on the right side to appear, then hover over it to enable the Edit button
        
        self.assertTrue(self.util.waitForElementToBePresent(self.element.object_detail_page_info_section), "ERROR inside navigateToObjectAndOpenObjectEditWindow(): do not see object info section")
        self.util.hoverOver(self.element.object_detail_page_info_section)
        
        # Wait for the Edit button in the object detail page info section, then click on it
        
        self.assertTrue(self.util.waitForElementToBePresent(self.element.object_info_page_edit_link), "ERROR inside navigateToObjectAndOpenObjectEditWindow(): do not see the Edit button")
        result=self.util.clickOn(self.element.object_info_page_edit_link)
        self.assertTrue(result,"ERROR in navigateToObjectAndOpenObjectEditWindow(): could not click on Edit button "+self.element.object_info_page_edit_link)
        
        # Wait for the modal window to appear
        
        self.assertTrue(self.util.waitForElementToBePresent(self.element.modal_window),"ERROR inside navigateToObjectAndOpenObjectEditWindow(): modal window does not become visible")
        
        # Wait for the field object title to appear
        
        self.assertTrue(self.util.waitForElementToBePresent(self.element.object_title), "ERROR inside navigateToObjectAndOpenObjectEditWindow(): do not see field [title] in the edit window")
        
    def openObjectEditWindow(self):
        self.closeOtherWindows()
        self.util.hoverOver(self.element.object_detail_page_info_section)  
        self.assertTrue(self.util.waitForElementToBePresent(self.element.object_info_page_edit_link), "ERROR inside openObjectEditWindow(): do not see the Edit button")
        result=self.util.clickOn(self.element.object_info_page_edit_link)
        self.assertTrue(result,"ERROR in openObjectEditWindow(): could not click on Edit button "+self.element.object_info_page_edit_link)
        self.assertTrue(self.util.waitForElementToBePresent(self.element.modal_window),"ERROR inside openObjectEditWindow(): can't see modal window")
        self.assertTrue(self.util.waitForElementToBePresent(self.element.object_title), "ERROR inside openObjectEditWindow(): do not see object_title in the edit window")
       
    
    def showHiddenValues(self): 
        self.util.waitForElementToBePresent(self.element.modal_window_show_hidden_fields_link, 5)
        if (self.util.isElementPresent(self.element.modal_window_show_hidden_fields_link)):
            result=self.util.clickOn(self.element.modal_window_show_hidden_fields_link)
            self.assertTrue(result,"ERROR in showHiddenValues(): could not click on "+self.element.modal_window_show_hidden_fields_link)
        #this step is needed to make sure that the hidden fileds are presented 
        #self.util.waitForElementToBePresent(self.element.object_code)
        #self.assertTrue(self.element.object_code, "do not see the expanded area code input field")
        #self.assertTrue(self.element.modal_window_hidden_fields_area, "do not see the expanded hidden fields area")
    
    def populateObjectInEditWindow(self, name, grcobject_elements,grcobject_values ):
        self.util.waitForElementToBeVisible(self.element.object_title)
        self.showHiddenValues() 
        self.closeOtherWindows()
        for key,xpath in grcobject_elements.iteritems():  
            #print key, xpath ,  grcobject_values[key] 
            
            if key in ["network_zone","kind","fraud_related","key_control", "means","type"]:
                dropdown_element = self.element.object_dropdown.replace("NAME",key )
                self.util.waitForElementToBePresent(dropdown_element) 
                self.assertTrue(self.util.isElementPresent(dropdown_element), "do not see the dropdown for "+ key)
                dropdown_option = dropdown_element + "/option[" + str(grcobject_values[key]) + "]"
                self.util.waitForElementToBePresent(dropdown_option) 
                option = self.util.getTextFromXpathString(dropdown_option)  
                print "the option for the dropdown " + key + " that should be selected is " + option
                #self.util.selectFromDropdownUntilSelected(dropdown_element, dropdown_option)
                self.selectFromDropdownOption(dropdown_element, grcobject_values[key])
                grcobject_values[key]=option
          
            if key=="code":
                self.util.waitForElementToBePresent(xpath) 
                self.util.waitForElementToBeVisible(xpath) 
                grcobject_values[key] = self.util.getAnyAttribute(self.element.object_code, "value") + "_edited"
                self.util.inputTextIntoField(grcobject_values[key] ,xpath)
                
            if key in ["title","scope","organization"]:
                self.util.waitForElementToBePresent(xpath)
                self.util.waitForElementToBeVisible(xpath) 
                grcobject_values[key] = name + "_edited" 
                self.util.inputTextIntoField(grcobject_values[key] ,xpath)
            if key == "owner":
                self.util.waitForElementToBePresent(xpath) 
                self.util.waitForElementToBeVisible(xpath) 
                grcobject_values[key] = "testrecip@gmail.com"
                owner_email = "testrecip@gmail.com"
                self.util.inputTextIntoField(
                                               owner_email,
                                               self.element.object_owner
                                               )
                matching_email_selector = self.element.autocomplete_list_element_with_email.replace("EMAIL",owner_email)
                self.util.waitForElementToBeVisible(matching_email_selector)
                self.util.clickOn(matching_email_selector)
                        
            """
                self.util.waitForElementToBePresent(xpath)
                self.util.waitForElementToBeVisible(xpath) 
                grcobject_values[key] = "testrecip@gmail.com" 
                self.util.inputTextIntoField(grcobject_values[key] ,xpath)
                matching_email_selector = self.element.autocomplete_list_element_with_email.replace("EMAIL", grcobject_values[key])
                self.util.waitForElementToBePresent(matching_email_selector)
                self.util.waitForElementToBeVisible(matching_email_selector)
                self.util.clickOn(matching_email_selector)
                """
            if key in ["description","notes"]:          
                time.sleep(3)  
                frame_element = self.element.object_iFrame.replace("FRAME_NAME",key)
                self.util.waitForElementToBeVisible(frame_element)
                #self.util.waitForIframe(frame_element)  
                grcobject_values[key]=key+"_"+name+ "_edited"
                self.util.typeIntoFrame(grcobject_values[key], frame_element) 
            if key=="url":
                self.util.waitForElementToBePresent(xpath)
                self.util.waitForElementToBeVisible(xpath) 
                grcobject_values[key] = "http://www.google.com"
                self.util.inputTextIntoField(grcobject_values[key] ,xpath)

        self.assertTrue(self.util.isElementPresent(self.element.modal_window_save_button), "do not see the Save button")
        self.util.waitForElementToBeVisible(self.element.modal_window_save_button) 
        self.saveObjectData()
        
    def selectFromDropdownOption(self,select_element,option_number):
        self.assertTrue(self.util.isElementPresent(select_element), "do not see the dropdown")
        self.util.waitForElementToBeVisible(select_element)
        option_to_be_selected = self.util.getTextFromXpathString(select_element + "/option[" + str(option_number) + "]")
        #print option_to_be_selected
        self.util.selectFromDropdownUntilSelected(select_element, option_to_be_selected)
        #time.sleep(3)
        
       
 
    def verifyObjectValues(self, grcobject_elements,grcobject_values):
        self.closeOtherWindows()
        for key,xpath in grcobject_elements.iteritems(): 
            #print "Inside verifyObjectValues, key=" + key + ", value="+grcobject_values[key]
            if key in ["description","notes"]:
                time.sleep(3)  
                frame_element = self.element.object_iFrame.replace("FRAME_NAME",key)
                self.util.waitForElementToBePresent(frame_element)
                self.util.waitForElementToBeVisible(frame_element)
                new_value = self.util.getTextFromFrame(frame_element)
                self.assertTrue(new_value == grcobject_values[key], "Verification ERROR: the value of " + key + " should be " + grcobject_values[key] + " but it is " + new_value )
            if key in ["network_zone","kind","fraud_related","key_control", "means","type"]:
                dropdown_element = self.element.object_dropdown.replace("NAME",key )
                dropdown_element_selected_option= self.element.object_dropdown_selected_option.replace("NAME",key )
                self.util.waitForElementToBePresent(dropdown_element)                
                self.assertTrue(self.util.isElementPresent(dropdown_element),"ERROR inside verifyObjectValues(): can't see dropdown element "+ key)
                self.util.waitForElementToBePresent(dropdown_element_selected_option)
                self.assertTrue(self.util.isElementPresent(dropdown_element_selected_option),"ERROR inside verifyObjectValues(): can't see dropdown selected option for "+ key)
                new_value = self.util.getTextFromXpathString(dropdown_element_selected_option)
                self.assertTrue(new_value == grcobject_values[key], "Verification ERROR: the value of " + key + " should be [" + grcobject_values[key] + "] but it is " + new_value )
            if key in ["title","owner","code","url", "organization", "scope"]:
                    self.util.waitForElementToBePresent(xpath)
                    self.util.waitForElementToBeVisible(xpath)
                    self.assertTrue(self.util.isElementPresent(xpath),"ERROR inside verifyObjectValues(): can't see element "+key)
                    new_value = self.util.getAnyAttribute(xpath, "value")
                    if not new_value:
                        self.assertTrue(False, "Verification ERROR: could not retrieve the value of " + xpath)
                    #print "new_value="+new_value
                    else:
                        self.assertTrue(new_value == grcobject_values[key], "Verification ERROR: the value of " + key + " should be " + grcobject_values[key] + " but it is " + new_value )
            print "Verification OK: the value of " + key + " is "+str(grcobject_values[key]) +", as expected." 
    
    def deleteObject(self):
        self.util.waitForElementToBePresent(self.element.modal_window_delete_button)
        self.assertTrue(self.util.isElementPresent(self.element.modal_window_delete_button), "ERROR: Could not delete object: Can not see the Delete button")
        result=self.util.clickOn(self.element.modal_window_delete_button)
        self.assertTrue(result,"ERROR in deleteObject(): could not click on Delete button "+self.element.modal_window_delete_button)
        
        
        status=self.util.waitForElementToBePresent(self.element.modal_window_confirm_delete_button)
        self.assertTrue(status, "ERROR inside deleteObject(): Could not delete object: Could not find "+ self.element.modal_window_confirm_delete_button)
        
        self.assertTrue(self.util.isElementPresent(self.element.modal_window_confirm_delete_button), "Can not see the Confirm Delete button")
        result=self.util.clickOn(self.element.modal_window_confirm_delete_button)
        self.assertTrue(result,"ERROR inside deleteObject(): could not click Confirm Delete button "+self.element.modal_window_confirm_delete_button)
        
        if self.util.isElementPresent(self.element.modal_window_confirm_delete_button):
            result=self.util.clickOn(self.element.modal_window_confirm_delete_button)
            self.assertTrue(result,"ERROR inside deleteObject(): could not click Confirm Delete button "+self.element.modal_window_confirm_delete_button)
        
        status=self.util.waitForElementNotToBePresent(self.element.modal_window)
        self.assertTrue(status, "ERROR inside deleteObject(): Could not delete object: Modal window " + self.element.modal_window + " is still present")
        
        print "Object deleted successfully."
     

            
        
        
        
    def  getObjectIdFromHref(self, link):
        href = self.util.getAnyAttribute(link, "href")
        id = href.split("/")[-1]
        return id
    
    def mapAObjectLHN(self, object):
        print "Start mapping LHN "+ object
        self.closeOtherWindows()
        self.expandLeftNavMenuForObject(object)
        first_link_of_the_section_link = self.element.left_nav_first_object_link_in_the_section.replace("SECTION",object )
        self.assertTrue(self.util.waitForElementToBePresent(first_link_of_the_section_link), "ERROR inside mapAObjectLHN(): cannot see the first "+ object+ " in LHN")
        idOfTheObject = self.getObjectIdFromHref(first_link_of_the_section_link)
       # print "the first "+ object + " id is " +  idOfTheObject
        self.util.hoverOverAndWaitFor(first_link_of_the_section_link,self.element.map_to_this_object_link)
        self.assertTrue(self.util.isElementPresent(self.element.map_to_this_object_link), "no Map to link")
        result=self.util.clickOn(self.element.map_to_this_object_link)
        self.assertTrue(result,"ERROR in mapAObjectLHN(): could not click on Map to link for "+object)
        self.verifyObjectIsMapped(object,idOfTheObject )
        
    def navigateToMappingWindowForObject(self, object):
        EXPANDABLES = ["Control"]
        self.assertTrue(self.util.waitForElementToBePresent(self.element.inner_nav_section),"ERROR inside mapAObjectWidget(): can't see inner_nav_section")
            
        #click on the inner nav and wait for the corresponding widhet section to become active
        
        inner_nav_object_link = self.element.inner_nav_object_link.replace("OBJECT", object.lower())
        self.assertTrue(self.util.waitForElementToBePresent(inner_nav_object_link),"ERROR mapAObjectWidget XXX(): can't see inner_nav_object_link for "+object)
        self.util.waitForElementToBeVisible(inner_nav_object_link)

        #self.util.waitForElementToBeClickable(inner_nav_object_link)
        #self.assertTrue(self.util.isElementPresent(inner_nav_object_link), "no inner nav link for "+ object)

        result=self.util.clickOn(inner_nav_object_link)
        self.assertTrue(result,"ERROR in mapAObjectWidget(): could not click "+inner_nav_object_link + " for object "+object)
        active_section = self.element.section_active.replace("SECTION", object.lower())
        self.assertTrue(self.util.waitForElementToBePresent(active_section), "ERROR inside mapAObjectWidget(): no active section for "+ object)
        
        #click on the object link in the widget to  search for other objects modal
        if object in EXPANDABLES:
            open_mapping_modal_window_link = self.element.section_widget_expanded_join_link1.replace("OBJECT", object)
        else: 
            open_mapping_modal_window_link = self.element.section_widget_join_object_link.replace("OBJECT", object)
        self.util.waitForElementToBePresent(open_mapping_modal_window_link)
        self.assertTrue(self.util.isElementPresent(open_mapping_modal_window_link),"ERROR inside mapAObjectWidget(): can't see the + link for "+ object)

        print "the link that should be clicked to open the mapping modal window is " + open_mapping_modal_window_link
        # if footer is expandable, hover first, then click on submenu
        if object in EXPANDABLES:
        # hover before clicking in case expander must act
            self.util.hoverOver(open_mapping_modal_window_link)
            expanded_button = self.element.section_widget_expanded_join_link2.replace("OBJECT", object)
            self.util.waitForElementToBeVisible(expanded_button)
            self.util.clickOn(expanded_button)
        else:
            result=self.util.clickOn(open_mapping_modal_window_link)
        self.assertTrue(result,"ERROR in mapAObjectWidget(): could not click on "+open_mapping_modal_window_link+" for object "+object)
        self.assertTrue(self.util.waitForElementToBePresent(self.element.mapping_modal_window), "ERROR inside mapAObjectWidget(): cannot see the mapping modal window")
  
  
        

    def mapFirstObject(self, object, is_program=False):
        self.util.waitForElementToBePresent(self.element.mapping_modal_selector_list_first_object)
        self.assertTrue(self.util.waitForElementToBePresent(self.element.mapping_modal_selector_list_first_object), "ERROR inside mapAObjectWidget(): cannot see first object in the selector")
        
        # for program/person mapping, extract email for later
        if is_program and object == "Person":
            emailOfPersonToBeMapped = self.util.getTextFromXpathString(self.element.mapping_modal_selector_list_first_object_email)
            print "the first Person's email is " + emailOfPersonToBeMapped
        else:  # otherwise, get ID
            idOfTheObjectToBeMapped = self.util.getAnyAttribute(self.element.mapping_modal_selector_list_first_object, "data-id")
            print "the first "+ object + " id is " +  idOfTheObjectToBeMapped
        
        self.util.waitForElementToBePresent(self.element.mapping_modal_selector_list_first_object_link)
        self.util.clickOn(self.element.mapping_modal_selector_list_first_object_link)
        self.util.waitForElementToBePresent(self.element.mapping_modal_window_map_button)
        self.assertTrue(self.util.isElementPresent(self.element.mapping_modal_window_map_button), "no Map button")
        result = self.util.clickOn(self.element.mapping_modal_window_map_button)
        self.assertTrue(result, "ERROR in mapAObjectWidget(): could not click on Map button for " + object)
        
        self.util.waitForElementNotToBePresent(self.element.mapping_modal_window)
        
        if is_program and object == "Person":
            mapped_object_link = self.verifyObjectIsMapped(object, emailOfPersonToBeMapped, is_program=is_program)
            return emailOfPersonToBeMapped
        else:
            mapped_object_link = self.verifyObjectIsMapped(object, idOfTheObjectToBeMapped, is_program=is_program)
            return idOfTheObjectToBeMapped
        
        
    def mapPerson(self, person):
        self.util.waitForElementToBePresent(self.element.mapping_modal_window)
        self.assertTrue(self.util.isElementPresent(self.element.mapping_modal_window), "do not see the modal window")
        self.util.waitForElementToBePresent(self.element.mapping_modal_input_textfiled)
        self.util.inputTextIntoField(person,self.element.mapping_modal_input_textfiled)

        self.util.waitForElementToBePresent(self.element.mapping_modal_selector_list_first_object)
        self.assertTrue(self.util.waitForElementToBePresent(self.element.mapping_modal_selector_list_first_object), "ERROR inside mapAObjectWidget(): cannot see first object in the selector")
        
        # for program/person mapping, extract email for later
       
        emailOfPersonToBeMapped = self.util.getTextFromXpathString(self.element.mapping_modal_selector_list_first_object_email)
        print "the first Person's email is " + emailOfPersonToBeMapped
    
        self.util.waitForElementToBePresent(self.element.mapping_modal_selector_list_first_object_link)
        self.util.clickOn(self.element.mapping_modal_selector_list_first_object_link)
        self.util.waitForElementToBePresent(self.element.mapping_modal_window_map_button)
        self.assertTrue(self.util.isElementPresent(self.element.mapping_modal_window_map_button), "no Map button")
        self.util.clickOn(self.element.mapping_modal_window_map_button)
        #self.assertTrue(result, "ERROR in mapAObjectWidget(): could not click on Map button for " + object)
        
        self.util.waitForElementNotToBePresent(self.element.mapping_modal_window)
        return emailOfPersonToBeMapped

        
        
        
        
        

    def mapAObjectWidget(self, object, is_program=False):
        self.closeOtherWindows()
        self.navigateToMappingWindowForObject(object)
        
        """
        self.assertTrue(self.util.waitForElementToBePresent(self.element.inner_nav_section),"ERROR inside mapAObjectWidget(): can't see inner_nav_section")
            
        #click on the inner nav and wait for the corresponding widhet section to become active
        
        inner_nav_object_link = self.element.inner_nav_object_link.replace("OBJECT", object.lower())
        self.assertTrue(self.util.waitForElementToBePresent(inner_nav_object_link),"ERROR mapAObjectWidget XXX(): can't see inner_nav_object_link for "+object)
        self.util.waitForElementToBeVisible(inner_nav_object_link)

        #self.util.waitForElementToBeClickable(inner_nav_object_link)
        #self.assertTrue(self.util.isElementPresent(inner_nav_object_link), "no inner nav link for "+ object)

        result=self.util.clickOn(inner_nav_object_link)
        self.assertTrue(result,"ERROR in mapAObjectWidget(): could not click "+inner_nav_object_link + " for object "+object)
        active_section = self.element.section_active.replace("SECTION", object.lower())
        self.assertTrue(self.util.waitForElementToBePresent(active_section), "ERROR inside mapAObjectWidget(): no active section for "+ object)
        
        #click on the object link in the widget to the search for other objects modal 
        join_object_link = self.element.section_widget_join_object_link.replace("OBJECT", object)
        self.assertTrue(self.util.waitForElementToBePresent(join_object_link),"ERROR inside mapAObjectWidget(): can't see join_object_link")

        #self.util.waitForElementToBeClickable(join_object_link)
        #self.assertTrue(self.util.isElementPresent(join_object_link), "cannot see the link for object "+ object+ " in widget section")
        
        result=self.util.clickOn(join_object_link)
        self.assertTrue(result,"ERROR in mapAObjectWidget(): could not click on "+join_object_link+" for object "+object)
        self.assertTrue(self.util.waitForElementToBePresent(self.element.mapping_modal_window), "ERROR inside mapAObjectWidget(): cannot see the mapping modal window")
        """
        #select the first object from the search results and map it
        self.mapFirstObject(object, is_program=is_program)
        
       
       
    def verifyObjectIsMapped(self, object, objIdentifier, is_program=False, mapped_email=None):
        if is_program and object == "Person":
            objectEmail = objIdentifier
        else:
            objectId = objIdentifier
        self.assertTrue(self.util.waitForElementToBePresent(self.element.inner_nav_section),"ERROR inside verifyObjectIsMapped(): can't see inner_nav_section")
        #inner_nav_object_link_with_one_object_mapped = self.element.inner_nav_object_with_one_mapped_object.replace("OBJECT", object.lower())
        #self.util.waitForElementToBePresent(inner_nav_object_link_with_one_object_mapped)
        inner_nav_object_link = self.element.inner_nav_object_link.replace("OBJECT", object.lower())
        self.assertTrue(self.util.waitForElementToBePresent(inner_nav_object_link),"ERROR inside verifyObjectIsMapped(): can't see inner_nav_object_link")
        self.util.waitForElementToBeVisible(inner_nav_object_link)
        #self.util.waitForElementToBeClickable(inner_nav_object_link)
        self.assertTrue(self.util.isElementPresent(inner_nav_object_link), "no inner nav link for "+ object)
        #time.sleep(2)
        result=self.util.clickOn(inner_nav_object_link)
        self.assertTrue(result,"ERROR in verifyObjectIsMapped(): could not click on "+inner_nav_object_link + " for object "+object)
        active_section = self.element.section_active.replace("SECTION", object.lower())
        self.assertTrue(self.util.waitForElementToBePresent(active_section), "ERROR inside verifyObjectIsMapped(): no active section for "+ object)
        if is_program and object == "Person":
            mapped_object = self.element.mapped_person_program_email.replace("EMAIL", objectEmail)
            print "the mapped object is "+ mapped_object
            # check whether the person appears in the list at all
            self.assertTrue(self.util.waitForElementToBePresent(mapped_object), "ERROR inside verifyObjectIsMapped(): Person does not appear in Program list")
            # TODO: find a way to check whether the label is "Mapped"; the below didn't work
            #relationship_label = mapped_object + self.element.mapped_person_program_mapped_label
            #self.assertTrue(self.util.waitForElementToBePresent(relationship_label), 'ERROR inside verifyObjectIsMapped(): person relationship is not called "Mapped"')
        else:
            mapped_object = self.element.mapped_object.replace("OBJECT", object.lower()).replace("ID", objectId)
            print "the mapped object is "+ mapped_object
            self.assertTrue(self.util.waitForElementToBePresent(mapped_object), "ERROR inside verifyObjectIsMapped(): no mapped object")
        print "Object " + object + " is mapped successfully"
        return mapped_object
        
        
    #def waitForInnerNavToLoad(self):
    def navigateToAuditSectionViaInnerNavSection(self, object):
        inner_nav_object_link = self.element.inner_nav_object_link.replace("OBJECT", object.lower())
        self.assertTrue(self.util.waitForElementToBePresent(inner_nav_object_link),"ERROR mapAObjectWidget XXX(): can't see inner_nav_object_link for "+object)
        self.util.waitForElementToBeVisible(inner_nav_object_link)

        #self.util.waitForElementToBeClickable(inner_nav_object_link)
        #self.assertTrue(self.util.isElementPresent(inner_nav_object_link), "no inner nav link for "+ object)

        result=self.util.clickOn(inner_nav_object_link)
        self.assertTrue(result,"ERROR in mapAObjectWidget(): could not click "+inner_nav_object_link + " for object "+object)
        active_section = self.element.section_active.replace("SECTION", object.lower())
        self.assertTrue(self.util.waitForElementToBePresent(active_section), "ERROR inside mapAObjectWidget(): no active section for "+ object)
        
    def createAudit(self, audit_title):
        #verify modal window
        self.util.waitForElementToBeVisible(self.element.modal_window)
        self.assertTrue(self.util.isElementPresent(self.element.modal_window), "can't see modal dialog window for create new object")
        
        #verify audit titel textbox
        self.util.waitForElementToBeVisible(self.element.object_title)
        self.assertTrue(self.util.isElementPresent(self.element.object_title), "can't access the input textfield")
        
        #verification the title is correctly auto-populated     
        audit_auto_populated_title = self.util.getAnyAttribute(self.element.object_title,"value")
        #self.assertTrue(audit_title  in audit_auto_populated_title,"not correct auto-populated audit title")
        self.util.clickOn(self.element.audit_modal_autogenerate_checkbox)
        
        #calculate the dates - Fill in start date (current date), Planned End Date (+2months), Planned Report date from(+1month from start), Planned report date to (Planned end date + 1 week)
        start_date= self.convertDateIntoFormat(date.today())
        end_date = self.convertDateIntoFormat(self.add_months(datetime.date.today(), 2))
        
        report_start_date_in_date_format = self.add_months(datetime.date.today(), 1)
        report_start_date_in_sting_format = self.convertDateIntoFormat(report_start_date_in_date_format) 
        report_end_date_in_date_format = report_start_date_in_date_format + datetime.timedelta(days=7)
        report_end_date_in_string_format = self.convertDateIntoFormat(report_end_date_in_date_format)

        #populate the dates
        self.util.waitForElementToBePresent(self.element.audit_modal_start_date_input)
        self.assertTrue(self.util.isElementPresent(self.element.audit_modal_start_date_input), "can't see start date input field")
        self.util.inputTextIntoField(start_date, self.element.audit_modal_start_date_input)
        
        self.util.waitForElementToBePresent(self.element.audit_modal_end_date_input)
        self.assertTrue(self.util.isElementPresent(self.element.audit_modal_end_date_input), "can't see end date input field")
        self.util.inputTextIntoField(end_date, self.element.audit_modal_end_date_input)
        
        self.util.waitForElementToBePresent(self.element.audit_modal_report_start_date_input)
        self.assertTrue(self.util.isElementPresent(self.element.audit_modal_report_start_date_input), "can't see start report date input field")
        self.util.inputTextIntoField(report_start_date_in_sting_format, self.element.audit_modal_report_start_date_input)
        
        self.util.waitForElementToBePresent(self.element.audit_modal_report_end_date_input)
        self.assertTrue(self.util.isElementPresent(self.element.audit_modal_report_end_date_input), "can't see end report date input field")
        self.util.inputTextIntoField(report_end_date_in_string_format, self.element.audit_modal_report_end_date_input)
        
        #click on Advanced link
        self.showHiddenValues()
        frame_element = self.element.object_iFrame.replace("FRAME_NAME","description")
        
        # type the description 
        self.util.waitForElementToBePresent(frame_element)
        self.assertTrue(self.util.isElementPresent(frame_element), "can't see the description frame")
        self.util.typeIntoFrame(self.element.audit_modal_description_text, frame_element)
        
         # type the Firm name
        self.util.waitForElementToBePresent(self.element.audit_modal_firm_input_field)
        self.assertTrue(self.util.isElementPresent(self.element.audit_modal_firm_input_field), "can't see the firm name input field")
        self.util.inputTextIntoField(self.element.audit_modal_firm_text, self.element.audit_modal_firm_input_field)
        
        #verifying the auto-populated Audit Lead email
        self.util.waitForElementToBePresent(self.element.audit_modal_audit_lead_input_field)
        self.assertTrue(self.util.isElementPresent(self.element.audit_modal_audit_lead_input_field), "can't see the Audit Lead input field")
        audit_auto_populated_audit_lead = self.util.getAnyAttribute(self.element.audit_modal_audit_lead_input_field,"value")
        self.assertTrue(self.element.audit_modal_audit_lead_value  in audit_auto_populated_audit_lead,"not correct Audit Lead value")
        
        self.saveObjectData()
        return audit_auto_populated_title
        
        
    def expandCollapseRequest(self,request_title_text):
        self.closeOtherWindows()
        expand_link = self.element.audit_pbc_request_expand_collapse_button.replace("TITLE",request_title_text ) 
        self.util.waitForElementToBePresent(expand_link)
        self.assertTrue(self.util.isElementPresent(expand_link), "can't see the expand link") 
        self.util.hoverOver(expand_link)
        self.util.clickOn(expand_link)
        #response_element = self.element.audit_pbc_request_response.replace("TITLE",request_title_text )
        #self.util.waitForElementValueToBePresent(response_element)
        #self.assertTrue(self.util.isElementPresent(response_element), "can't see the expanded contetnt for the request link") 
 
 
    def createResponse(self, description):
        
        self.util.waitForElementToBeVisible(self.element.modal_window)
        self.assertTrue(self.util.isElementPresent(self.element.modal_window), "can't see modal dialog window for create new object")
        frame_element = self.element.object_iFrame.replace("FRAME_NAME","description")
        
        # type the description 
        self.util.waitForElementToBePresent(frame_element)
        self.assertTrue(self.util.isElementPresent(frame_element), "can't see the description frame")
        self.util.typeIntoFrame(description, frame_element)
        self.saveObjectData()
        
        
        
        
    def convertDateIntoFormat(self, date):
        correct_format_date = str(date.month) + "/" + str(date.day) + "/"+ str(date.year) 
        return correct_format_date

    def add_months(self,sourcedate,months):
        month = sourcedate.month - 1 + months
        year = sourcedate.year + month / 12
        month = month % 12 + 1
        day = min(sourcedate.day,calendar.monthrange(year,month)[1])
        return datetime.date(year,month,day)
    
    
    def getTheIdOfTheLastCreated(self, newly_created_object_type):
        object_element = self.element.data_object_element.replace("DATA_OBJECT", newly_created_object_type)
        self.util.waitForElementToBePresent(object_element)
        self.assertTrue(self.util.isElementPresent(object_element), "no " + newly_created_object_type +" have been created")
        overall_number_of_objects = str(self.util.getNumberOfOccurences(object_element))
        print "  " + str(overall_number_of_objects) + " " + newly_created_object_type + " have been created"
        last_created_object_element = self.element.data_object_element_with_index.replace("DATA_OBJECT", newly_created_object_type).replace("INDEX",overall_number_of_objects )
        self.util.waitForElementToBePresent(last_created_object_element)
        self.assertTrue(self.util.isElementPresent(last_created_object_element), "cannot see the last created object")
        print last_created_object_element
        last_created_object_element_id = self.util.getAnyAttribute(last_created_object_element, "data-object-id")
        print last_created_object_element_id
        return last_created_object_element_id
    
    def getTheIdOfTheLastCreatedObjective(self, link):
       
        #overall_number_of_objectives = str(self.util.getNumberOfOccurences(self.element.objective_elemet_in_the_inner_tree))
        #print str(overall_number_of_objectives) + " objectives have been created so far"
        #last_created_object_element = self.element.objective_elemet_in_the_inner_tree_with_index.replace("INDEX",overall_number_of_objectives )
        print link
        last_created_object_element_id = self.util.getAnyAttribute(link, "data-object-id")
        print last_created_object_element_id
        return last_created_object_element_id

    def uncheckMyWork(self):
        my_work_parent = self.util.driver.find_element_by_xpath(self.element.my_work_parent)
        if 'btn-success' in my_work_parent.get_attribute('class'):
            self.util.clickOn(self.element.my_work_checkbox)

    def closeOtherWindows(self):
        current_window = self.util.driver.current_window_handle
        all_windows = self.util.driver.window_handles
        for window in all_windows:
            if window != current_window:
                self.util.driver.switch_to_window(window)
                self.util.driver.close()
        self.util.driver.switch_to_window(current_window)
        
    def searchFor(self, search_term):
        self.util.waitForElementToBePresent(self.element.search_inputfiled)
        self.assertTrue(self.util.isElementPresent(self.element.search_inputfiled), "no search input field")
        search_term = '"' + search_term +'"' 
        self.util.inputTextIntoFieldAndPressEnter(search_term, self.element.search_inputfiled)
        
    def scheduleMeeting(self,title, date, start_time, end_time):
        self.util.waitForElementToBeVisible(self.element.modal_window)
        self.assertTrue(self.util.isElementPresent(self.element.modal_window), "can't see modal dialog window for meeting")
        
        self.util.waitForElementToBeVisible(self.element.meeting_title_input_textfield)
        self.assertTrue(self.util.isElementPresent(self.element.meeting_title_input_textfield), "can't see meeting title input")
        self.util.inputTextIntoField(title, self.element.meeting_title_input_textfield)
        
        self.util.waitForElementToBeVisible(self.element.meeting_date)
        self.assertTrue(self.util.isElementPresent(self.element.meeting_date), "can't see meeting Date input")
        self.util.inputTextIntoField(date, self.element.meeting_date)
        
        self.util.waitForElementToBeVisible(self.element.meeting_start_time_dropdown)
        self.assertTrue(self.util.isElementPresent(self.element.meeting_start_time_dropdown), "can't see meeting start time input")
        self.util.selectFromDropdownUntilSelected(self.element.meeting_start_time_dropdown, start_time)
        time.sleep(5)
        self.util.waitForElementToBeVisible(self.element.meeting_end_time_dropdown)
        self.assertTrue(self.util.isElementPresent(self.element.meeting_end_time_dropdown), "can't see meeting start time input")
        self.util.selectFromDropdownUntilSelected(self.element.meeting_end_time_dropdown, end_time)
        time.sleep(5)
        self.saveObjectData()
            

