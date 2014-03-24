'''
Created on Jun 19, 2013

@author: diana.tzinov
'''
import sys
from Elements import Elements
from WebdriverUtilities import WebdriverUtilities
import time, calendar
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

    def setUtils(self, util, object_type=None):
        self.util = util
        self.object_type = object_type

    def runTest(self):
        pass
    
    def getTimeId(self):
        return strftime("_%Y_%m_%d_%H_%M_%S")

    def current_user_email(self):
        if config.url == "http://localhost:8080/":
            return "user@example.com"
        else:
            return config.username

    def currentObjectId(self):
        from urlparse import urlparse as up
        return up(self.util.driver.current_url).path.split('/')[-1]

    def submitGoogleCredentials(self):
        self.util.inputTextIntoField(config.username, self.element.gmail_userid_textfield)
        self.assertTrue(self.util.isElementPresent(self.element.gmail_password_textfield), "can't see the password textfield")
        self.util.inputTextIntoField(config.password, self.element.gmail_password_textfield)
        self.util.clickOn(self.element.gmail_submit_credentials_button)

    def authorizeGAPI(self):
        # if GAPI modal is present, click the Authorize button
        try:  # but wait first
            self.util.waitForElementToBeVisible(self.element.gapi_modal, 5)
        except:
            pass
        if not self.util.isElementVisible(self.element.gapi_modal):
            return  # phrased as "not" to free up indentation
        self.closeOtherWindows()
        self.util.clickOn(self.element.gapi_modal_authorize_button)
        # after clicked, a login or permission window pops up
        # this will be the only window left; other is for login
        main_window = self.util.driver.current_window_handle
        self.loginGAPI(main_window)  # login if it's a login request
        self.grantPermissionGAPI(main_window)  # approve app requests
        self.util.driver.switch_to_window(main_window)

    def grantPermissionGAPI(self, main_window):
        # grab the other window, enter credentials
        popup_windows = [w for w in self.util.driver.window_handles if w != main_window]
        if len(popup_windows) == 0:
            return
        popup_window = popup_windows[0]
        self.util.driver.switch_to_window(popup_window)
        if self.util.isElementVisible(self.element.gapi_app_permission_form):
            self.assertTrue(self.util.isElementVisible(self.element.gapi_app_permission_authorize_button), "Can't see App authorization button")
            self.util.clickOn(self.element.gapi_app_permission_authorize_button)

    def loginGAPI(self, main_window):
        # grab the other window, enter credentials
        popup_windows = [w for w in self.util.driver.window_handles if w != main_window]
        if len(popup_windows) == 0:
            return
        popup_window = popup_windows[0]
        self.util.driver.switch_to_window(popup_window)
        if self.util.isElementPresent(self.element.gmail_userid_textfield):
            self.submitGoogleCredentials()

    def login(self):
        self.assertTrue(self.util.isElementPresent(self.element.login_button), "can't see the login button")
        if "localhost" in config.url:
            self.util.clickOnAndWaitFor(self.element.login_button, self.element.dashboard_title)
            self.authorizeGAPI()  # in case it's present
        else:
            self.util.clickOnAndWaitFor(self.element.login_button, self.element.gmail_password_textfield)
            self.submitGoogleCredentials()
            
        # need to check for permission screen, and if it's there
        # de-select "Remember..." if checked; then click on "Allow"
        if self.util.isElementPresent(self.element.g_accounts_login_prompt):
            checkbox = self.util.driver.find_element_by_xpath(self.element.g_accounts_remember_box)
            if checkbox.is_selected():
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
        # finally, need to check for GAPI modal
        self.authorizeGAPI()
        self.util.waitForElementToBePresent(self.element.dashboard_title)
    def isLHNSectionExpanded(self, section):
        section_status_link = self.element.left_nav_expand_status.replace("OBJECT", section)
        return self.util.isElementPresent(section_status_link)

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
            self.uncheckMyWorkBox()
            last_created_object_link = self.verifyObjectIsCreatedinLHN(grc_object, grc_object_name)
            return last_created_object_link
        else:
            print "verifying create object in mapping window"
            #commented the verifycation for now
            last_created_object_link = self.verifyObjectIsCreatedInSections(grc_object_name)
        print "Object created successfully."
        
        
    def NewResponseCreate(self, object_name):
        #self.closeOtherWindows()
        # Make sure window is there
        self.util.waitForElementToBeVisible(self.element.modal_window)
        self.assertTrue(self.util.isElementPresent(self.element.modal_window), "can't see modal dialog window for create new object")

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

    def saveObjectData(self):
        #self.util.inputTextIntoField("testrecip@gmail.com", self.element.modal_owner_textfield) #need this click to activate Save button
        self.util.waitForElementToBePresent(self.element.modal_window_save_button)
        self.assertTrue(self.util.isElementPresent(self.element.modal_window_save_button), "do not see the Save button")
        self.util.clickOnSave(self.element.modal_window_save_button)
        self.util.waitForElementNotToBePresent(self.element.modal_window)

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
        #self.verifyObjectIsCreatedinLHNViaSearch(object_title, widget)
        self.showObjectLinkWithSearch(object_title, widget)
        return last_created_object_link

    def verifyObjectIsCreatedinLHNViaSearch(self, search_term, section):
        object_left_nav_section_object_link_with_one_result = self.element.left_nav_expand_object_section_link_one_result_after_search.replace("OBJECT", section)
        self.searchFor(search_term)
        self.util.waitForElementToBePresent(object_left_nav_section_object_link_with_one_result)
        self.assertTrue(self.util.isElementPresent(object_left_nav_section_object_link_with_one_result), "the search did not return one result as it's supposed to" )
        object_left_nav_section_object_link = self.element.left_nav_expand_object_section_link.replace("OBJECT", section)

        self.assertTrue(self.util.waitForElementToBePresent(object_left_nav_section_object_link),"ERROR in navigateToObject(): can't see LHN link for "+section)

        # Expand the section if it is not already expanded
        if not self.isLHNSectionExpanded(section):
            self.util.clickOn(object_left_nav_section_object_link)
        object_title_link = self.element.left_nav_last_created_object_link.replace("SECTION", section).replace("OBJECT_TITLE", search_term)
        self.util.waitForElementToBePresent(object_title_link)
        self.assertTrue(self.util.isElementPresent(object_title_link), "ERROR inside navigateToObject(): do not see object  " + object_title_link + " in lhn" )

    def verifyObjectIsCreatedInSections(self, object_title):
        self.util.waitForElementToBePresent(self.element.mapping_modal_selector_list_first_object_link)
        self.assertTrue(self.util.isElementPresent(self.element.mapping_modal_selector_list_first_object_link), "can't see the first link in the mapping modal window")
        last_create_object_link_on_the_first_spot = self.element.mapping_modal_selector_list_first_object_link_with_specific_title.replace("TITLE",object_title)
        self.util.waitForElementToBePresent(last_create_object_link_on_the_first_spot)
        self.assertTrue(self.util.isElementPresent(last_create_object_link_on_the_first_spot), "the newly create object" +object_title + " is not on the first spot or doesn't eexist")
        last_created_object_link =  self.util.getTextFromXpathString(last_create_object_link_on_the_first_spot)
        print "the newly created object is " + last_created_object_link
        self.assertEquals(last_created_object_link, object_title, "the newly created object is not in Mapping Modal Window")
        return last_created_object_link
    
    
    def createSectionFor(self, object,object_id,section_title):
        section_add_link = self.element.mapped_object_area_section_add_link.replace("OBJECT", object).replace("ID", object_id)
        self.util.waitForElementToBePresent(section_add_link)
        self.assertTrue(self.util.isElementPresent(section_add_link), "cannot see section add + link")
       
        self.util.scrollIntoView(section_add_link)
        self.util.hoverOver(section_add_link)
        self.util.clickOn(self.element.section_create_link)
        """
        self.util.hoverOverAndWaitFor(section_add_link,self.element.section_create_link)
        self.util.clickOn(section_add_link)
        self.assertTrue(self.util.isElementPresent(self.element.section_create_link), "cannot see section create link")
        self.util.clickOn(self.element.section_create_link)
        """
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
        
        self.uncheckMyWorkBox()
        
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
        

    def showObjectLinkWithSearch(self, search_term, section):
        object_left_nav_section_object_link_with_one_result = self.element.left_nav_expand_object_section_link_one_result_after_search.replace("OBJECT", section)
        self.searchFor(search_term)
        self.util.waitForElementToBePresent(object_left_nav_section_object_link_with_one_result)
        self.assertTrue(self.util.isElementPresent(object_left_nav_section_object_link_with_one_result), "the search did not return one result as it's supposed to" )
        object_left_nav_section_object_link = self.element.left_nav_expand_object_section_link.replace("OBJECT", section)

        self.assertTrue(self.util.waitForElementToBePresent(object_left_nav_section_object_link),"ERROR in navigateToObject(): can't see LHN link for "+section)
        # Click on the object section link in the left nav
        if not self.isLHNSectionExpanded(section):
            self.util.clickOn(object_left_nav_section_object_link)
        object_title_link = self.element.left_nav_last_created_object_link.replace("SECTION", section).replace("OBJECT_TITLE", search_term)
        self.util.waitForElementToBePresent(object_title_link)
        self.assertTrue(self.util.isElementPresent(object_title_link), "ERROR inside navigateToObject(): do not see object " + object_title_link + " in lhn" )

    def navigateToObjectWithSearch(self, search_term, section):
        self.showObjectLinkWithSearch(search_term, section)
        object_title_link = self.element.left_nav_last_created_object_link.replace("SECTION", section).replace("OBJECT_TITLE", search_term)
        result = self.util.clickOn(object_title_link)
        self.assertTrue(result, "ERROR in navigateToObject(): could not click on object in LHN " + object_title_link)

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
                self.util.inputTextIntoField(owner_email, self.element.object_owner)
                matching_email_selector = self.element.autocomplete_list_element_with_text.replace("TEXT", owner_email)
                self.util.waitForElementToBeVisible(matching_email_selector)
                self.util.clickOn(matching_email_selector)

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
        self.util.refreshPage()
        
    def selectFromDropdownOption(self,select_element,option_number):
        self.assertTrue(self.util.isElementPresent(select_element), "do not see the dropdown")
        self.util.waitForElementToBeVisible(select_element)
        option_to_be_selected = self.util.getTextFromXpathString(select_element + "/option[" + str(option_number) + "]")
        self.util.selectFromDropdownUntilSelected(select_element, option_to_be_selected)
        
       
 
    def verifyObjectValues(self, grcobject_elements, grcobject_values):
        self.closeOtherWindows()
        for key,xpath in grcobject_elements.iteritems(): 
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
        self.uncheckMyWorkBox()
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
        
    def navigateToMappingWindowForObject(self, object, expandables=()):
        """Set expandables to the list of object types whose footer expands when you hover over the "add" button.
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
        
        #click on the object link in the widget to  search for other objects modal
        if object in expandables:
            open_mapping_modal_window_link = self.element.section_widget_expanded_join_link1.replace("OBJECT", object.lower())
        else: 
            open_mapping_modal_window_link = self.element.section_widget_join_object_link.replace("OBJECT", object)
        self.util.waitForElementToBePresent(open_mapping_modal_window_link)
        self.assertTrue(self.util.isElementPresent(open_mapping_modal_window_link),"ERROR inside mapAObjectWidget(): can't see the + link for "+ object)

        print "the link that should be clicked to open the mapping modal window is " + open_mapping_modal_window_link
        # if footer is expandable, hover first, then click on submenu
        if object in expandables:
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
        if object == self.object_type:
            # if same object type, make sure id != this object's id
            first_acceptable_map_link = self.element.mapping_modal_selector_first_nonself_object_link.replace("OBJECTID", self.currentObjectId())
        else:  # otherwise, just grab first
            first_acceptable_map_link = self.element.mapping_modal_selector_list_first_object_link
        self.util.waitForElementToBePresent(first_acceptable_map_link)
        self.util.clickOn(first_acceptable_map_link)
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


    def mapAObjectWidget(self, object, is_program=False, expandables=()):
        self.closeOtherWindows()
        self.navigateToMappingWindowForObject(object, expandables)
        
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
        start_date = date.today()
        end_date = self.add_months(start_date, 2)
        
        report_start_date = self.add_months(datetime.date.today(), 1)
        report_end_date = report_start_date + datetime.timedelta(days=7)

        # populate the dates
        self.enterDateWithCalendar(self.element.audit_modal_start_date_input, start_date, "start date")
        self.enterDateWithCalendar(self.element.audit_modal_end_date_input, end_date, "end date")
        self.enterDateWithCalendar(self.element.audit_modal_report_start_date_input, report_start_date, "reporting start date")
        self.enterDateWithCalendar(self.element.audit_modal_report_end_date_input, report_end_date, "reporting end date")
        
        #click on Advanced link
        self.showHiddenValues()
        frame_element = self.element.object_iFrame.replace("FRAME_NAME","description")
        
        # type the description 
        self.util.waitForElementToBePresent(frame_element)
        self.assertTrue(self.util.isElementPresent(frame_element), "can't see the description frame")
        self.util.typeIntoFrame(self.element.audit_modal_description_text, frame_element)
        
        # type the Firm name and select from drop-down
        self.util.waitForElementToBePresent(self.element.audit_modal_firm_input_field)
        self.assertTrue(self.util.isElementPresent(self.element.audit_modal_firm_input_field), "can't see the firm name input field")
        self.util.inputTextIntoField(self.element.audit_modal_firm_text, self.element.audit_modal_firm_input_field)
        firm_autocomplete = self.element.autocomplete_list_element_with_text2.replace("TEXT", self.element.audit_modal_firm_text)
        self.util.waitForElementToBePresent(firm_autocomplete)
        self.util.clickOn(firm_autocomplete)
        
        #verifying the auto-populated Audit Lead email
        self.util.waitForElementToBePresent(self.element.audit_modal_audit_lead_input_field)
        self.assertTrue(self.util.isElementPresent(self.element.audit_modal_audit_lead_input_field), "can't see the Audit Lead input field")
        audit_auto_populated_audit_lead = self.util.getAnyAttribute(self.element.audit_modal_audit_lead_input_field,"value")
        self.assertTrue(self.current_user_email()  in audit_auto_populated_audit_lead,"not correct Audit Lead value")
        
        self.saveObjectData()
        return audit_auto_populated_title

    def expandCollapseRequest(self, request_title_text):
        #self.closeOtherWindows()
        expand_link = self.element.audit_pbc_request_expand_collapse_button2.replace("TITLE", request_title_text) 
        expanded_section = self.element.audit_pbc_request_expanded.replace("TITLE",request_title_text ) 
        self.util.waitForElementToBePresent(expand_link)
        self.assertTrue(self.util.isElementPresent(expand_link), "can't see the expand link") 
        self.util.hoverOver(expand_link)
        self.util.clickOn(expand_link)
        #response_element = self.element.audit_pbc_request_response.replace("TITLE",request_title_text )
        self.util.waitForElementToBePresent(expanded_section)
        if self.util.isElementPresent(expanded_section) ==False:
            self.util.hoverOver(expand_link)
            self.util.clickOn(expand_link)
        self.assertTrue(self.util.isElementPresent(expanded_section), "can't expand the request section for " + request_title_text)

    def setRequestToRespondable(self, request_title_text):
        target_state_button = self.element.audit_pbc_request_state_button.replace("TITLE", request_title_text)
        state_element = self.util.driver.find_element_by_xpath(target_state_button)
        self.util.waitForElementToBePresent(target_state_button)
        status = state_element.get_attribute('data-value')
        if status == "Requested":
            self.util.clickOn(target_state_button)

    def createResponse2(self, response_dict):
        self.util.waitForElementToBePresent(self.element.modal_window)
        self.assertTrue(self.util.isElementPresent(self.element.modal_window), "can't see modal dialog window for create new object")

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

    def calendarDateSelector(self, date):
        day_dict = {
            'day': date.day,
            'month': date.month - 1,
            'year': date.year,
        }
        return '//table[@class="ui-datepicker-calendar"]//td[@data-month="{month}"][@data-year="{year}"]/a[text()="{day}"]'.format(**day_dict)

    def selectMonthYear(self, date):
        self.util.selectFromDropdownByValue(self.element.datepicker_month_dropdown, str(date.month - 1))
        self.util.selectFromDropdownByValue(self.element.datepicker_year_dropdown, str(date.year))

    def enterDateWithCalendar(self, date_field, date, field_name="the date field"):
        self.util.waitForElementToBePresent(date_field)
        self.assertTrue(self.util.isElementPresent(date_field), "can't see {} input field".format(field_name))
        # click on date field to summon calendar
        self.util.clickOnAndWaitFor(date_field, self.element.datepicker_calendar)
        # select the right month and year
        self.selectMonthYear(date)
        # select date within calendar
        self.util.clickOn(self.calendarDateSelector(date))

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

    def checkMyWorkBox(self):
        """ensures "My Work" box is checked, regardless of current state"""
        self.util.waitForElementToBePresent(self.element.my_work_checkbox)
        checkbox = self.util.driver.find_element_by_xpath(self.element.my_work_checkbox)
        if not checkbox.is_selected():
            self.util.clickOn(self.element.my_work_checkbox)

    def uncheckMyWorkBox(self):
        """ensures "My Work" box is UNchecked, regardless of current state"""
        self.util.waitForElementToBePresent(self.element.my_work_checkbox)
        checkbox = self.util.driver.find_element_by_xpath(self.element.my_work_checkbox)
        if checkbox.is_selected():
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
        self.util.waitForElementToBePresent(self.element.search_inputfield)
        self.assertTrue(self.util.isElementPresent(self.element.search_inputfield), "no search input field")
        search_term = '"' + search_term +'"' 
        self.util.inputTextIntoFieldAndPressEnter(search_term, self.element.search_inputfield)
        
    def scheduleMeeting(self,title, date, start_time, end_time):
        self.util.waitForElementToBeVisible(self.element.modal_window)
        self.assertTrue(self.util.isElementPresent(self.element.modal_window), "can't see modal dialog window for meeting")
        
        self.util.waitForElementToBeVisible(self.element.meeting_start_time_dropdown)
        self.assertTrue(self.util.isElementPresent(self.element.meeting_start_time_dropdown), "can't see meeting start time input")
        self.util.selectFromDropdownUntilSelected(self.element.meeting_start_time_dropdown, start_time)
        
        self.util.waitForElementToBeVisible(self.element.meeting_end_time_dropdown)
        self.assertTrue(self.util.isElementPresent(self.element.meeting_end_time_dropdown), "can't see meeting start time input")
        self.util.selectFromDropdownUntilSelected(self.element.meeting_end_time_dropdown, end_time)
        
        self.util.waitForElementToBeVisible(self.element.meeting_title_input_textfield)
        self.assertTrue(self.util.isElementPresent(self.element.meeting_title_input_textfield), "can't see meeting title input")
        self.util.inputTextIntoField(title, self.element.meeting_title_input_textfield)
        
        self.util.waitForElementToBeVisible(self.element.meeting_date)
        self.assertTrue(self.util.isElementPresent(self.element.meeting_date), "can't see meeting Date input")
        self.util.inputTextIntoField(date, self.element.meeting_date)
        #self.meetingSelectParticipants()
        self.saveObjectData()
        
    def meetingSelectParticipants(self):

        self.util.waitForElementToBePresent(self.element.meeting_participant_select)
        self.util.waitForElementToBePresent(self.element.meeting_participant_select_first)
        self.util.waitForElementToBePresent(self.element.meeting_participant_select_second)
        
        self.util.shift_key_down()
        self.util.selectFromDropdownByValue(self.element.meeting_participant_select, "2")
        self.util.clickOn(self.element.meeting_participant_select_first)
        self.util.shift_key_up()
        """
        self.util.waitForElementToBeVisible(self.element.meeting_title_input_textfield)
        self.assertTrue(self.util.isElementPresent(self.element.meeting_title_input_textfield), "can't see meeting title input")
        self.util.inputTextIntoField(title, self.element.meeting_title_input_textfield)
        """
        
    def verifyMeetingData(self, data, start_time, end_time):
          
        self.util.isElementPresent(self.element.meeting_gcal_link)
        self.util.isElementPresent('//li[@data-object-type="meeting"]//div[@class="tree-description short"]')
        
        dates=self.util.getTextFromXpathString('//li[@data-object-type="meeting"]//div[@class="tree-description short"]')
        dates=dates.strip()  
        # Example dates string:
        # 'Starts at: 01/25/2014 03:00:00 PM\nEnds at: 01/25/2014 04:00:00 PM'
        
        date1=dates.split("\n")[0]  # 'Starts at: 01/25/2014 03:00:00 PM' 
        date2=dates.split("\n")[1]  # 'Ends at: 01/25/2014 04:00:00 PM'
        
        meeting_date=date1.split(" ")[2] # '01/25/2014'
        
        meeting_start_time=date1.split(" ")[3] + " " + date1.split(" ")[4] # '03:00:00 PM'
        meeting_end_time=  date2.split(" ")[3] + " " + date2.split(" ")[4] # '04:00:00 PM'
        
        self.assertTrue(meeting_date==data,"Meeting dates do NOT match; expected meeting date:"+data+", actual meeting date:"+meeting_date)
        self.assertTrue(meeting_start_time == start_time,"Meeting start times do NOT match; expected meeting start time:"+start_time+", actual meeting start time:"+meeting_start_time)
        self.assertTrue(meeting_end_time == end_time,"Meeting end times do NOT match; expected meeting end time:"+end_time+", actual meeting end time:"+meeting_end_time)

    def dismissFlashMessages(self):
        try:
            self.util.waitForElementToBePresent(self.element.flash_box)
        except:
            return
        for type_ in self.element.flash_types:
            dismiss_btn = self.element.flash_box_type_dismiss.replace("TYPE", type_)
            if self.util.isElementPresent(dismiss_btn):
                self.util.clickOn(dismiss_btn)

    def waitForAlertSuccessMessages(self):
        self.util.waitForElementToBePresent('//div[@class="alert alert-success"]')
        self.util.waitForElementToBePresent('//span[contains(.,"Creating Drive folder for Objective 2 for Auto Test of Audit -- Done")]')
        self.util.waitForElementToBePresent('//span[contains(.,"Creating Drive folder for Objective 1 for Auto Test of Audit -- Done")]')
        self.util.waitForElementToBePresent('//span[contains(.,"Creating Drive folder for Objective 3 for Auto Test of Audit -- Done")]')
        #self.util.waitForElementToBePresent('//span[contains(.,"Linking folder \"Objective 3 for Auto Test of Audit\" to Request -- Done")]')
        self.util.waitForElementToBePresent('//span[contains(.,"Linking folder")][1]')
        self.util.waitForElementToBePresent('//span[contains(.,"Linking folder")][2]')
        self.util.waitForElementToBePresent('//span[contains(.,"Linking folder")][3]')
        #self.util.waitForElementToBePresent('//span[contains(.,"Linking folder "Objective 1 for Auto Test of Audit" to Request -- Done")]')
        #self.util.waitForElementToBePresent('//span[contains(.,"Linking folder "Objective 2 for Auto Test of Audit" to Request -- Done")]')
        #self.util.switch_to_active_element()
        self.util.clickOn('//a[@class="close"]')
        self.closeOtherWindows()
        