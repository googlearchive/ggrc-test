'''
Created on Jun 19, 2013

@author: diana.tzinov
'''

from datetime import date, timedelta, datetime as dt
import datetime
from fileinput import close
import json
from os import remove, close
import os
from random import randint
from shutil import move
import string
import sys
from tempfile import mkstemp
from time import strftime
import time, calendar
import unittest

from Elements import Elements as elem
from WebdriverUtilities import WebdriverUtilities
import config
from testcase import WebDriverTestCase


# ON OTHER DEPLOYMENTS, CHANGE THIS to the server user name
SERVER_USER = 'jenkins'

def log_time(f):
    """decorator that records function time and stores it to the self.test.benchmark dict with key = function name and value = list of durations of all invocations of that function"""
    def benched_function(*args, **kwargs):
        t_start = dt.now()
        output = f(*args, **kwargs)
        t_end = dt.now()
        t_total = (t_end - t_start).total_seconds()
        # args[0] = what would otherwise be self
        # Store the results dict in a var to save space
        if getattr(args[0], 'test', None):  # avoid if no TestCase
            result_dict = args[0].test.benchmarks['results']
            # Append to list at that key or start new one
            if f.func_name in result_dict:
                result_dict[f.func_name].append(t_total)
            else:
                result_dict[f.func_name] = [t_total]
        return output

    return benched_function


class Helpers(unittest.TestCase):
    util = WebdriverUtilities()

    def __init__(self, test=None):
        # hack to make sure this is only called for WebDriverTestCase
        # TODO: Make this less coupled to other parts of the code.
        if test and isinstance(test, WebDriverTestCase):
            self.test = test  # enable it to access unit test object
            self.main_timestamp = strftime("%Y_%m_%d_%H_%M_%S")
            self.test.benchmarks['timestamp'] = self.main_timestamp
        from os.path import abspath, dirname, join
        THIS_ABS_PATH = abspath(dirname(__file__))
        JS_DIR = join(THIS_ABS_PATH, '../JavaScripts/')
        LOADED_SCRIPT_FILE = join(JS_DIR, 'load_signaler.html')
        MAP_LOADED_SCRIPT_FILE = join(JS_DIR, 'map_load_signaler.html')
        with open(LOADED_SCRIPT_FILE, 'r') as f:
            self.loaded_script = f.read().strip().replace('\n', " ")
        with open(MAP_LOADED_SCRIPT_FILE, 'r') as f:
            self.map_loaded_script = f.read().strip().replace('\n', " ")

        super(Helpers, self).__init__()

    def setUtils(self, util, object_type=None):
        self.util = util
        self.object_type = object_type
        
    def getUtils(self):
        return self.util;

    def runTest(self):
        pass

    def getTimeId(self):
        # Always return the value generated at the start of the test;
        # Prefix with "_" because it appends to names
        return "_" + self.main_timestamp

    def current_user_email(self):
        if config.url == "http://localhost:8080/":
            return "user@example.com"
        else:
            return config.username

    def currentObjectId(self):
        from urlparse import urlparse as up
        return up(self.util.driver.current_url).path.split('/')[-1]

    @log_time
    def submitGoogleCredentials(self):
        self.util.inputTextIntoField(config.username, elem.gmail_userid_textfield)
        self.assertTrue(self.util.isElementPresent(elem.gmail_password_textfield), "can't see the password textfield")
        self.util.inputTextIntoField(config.password, elem.gmail_password_textfield)
        self.util.clickOn(elem.gmail_submit_credentials_button)

    @log_time
    def authorizeGAPI(self, delay=5):
        # if GAPI modal is present, click the Authorize button
        try:  # but wait first
            self.util.waitForElementToBeVisible(elem.gapi_modal, 5)
        except:
            pass
        if not self.util.isElementVisible(elem.gapi_modal):
            return  # phrased as "not" to free up indentation
        self.closeOtherWindows()
        self.util.clickOn(elem.gapi_modal_authorize_button)
        # after clicked, a login or permission window pops up
        # this will be the only window left; other is for login
        main_window = self.util.driver.current_window_handle
        self.loginGAPI(main_window)  # login if it's a login request
        self.grantPermissionGAPI(main_window)  # approve app requests
        self.util.driver.switch_to_window(main_window)

    @log_time
    def grantPermissionGAPI(self, main_window):
        # grab the other window, enter credentials
        popup_windows = [w for w in self.util.driver.window_handles if w != main_window]
        if len(popup_windows) == 0:
            return
        popup_window = popup_windows[0]
        self.util.driver.switch_to_window(popup_window)
        if self.util.isElementVisible(elem.gapi_app_permission_form):
            self.assertTrue(self.util.isElementVisible(elem.gapi_app_permission_authorize_button), "Can't see App authorization button")
            self.util.clickOn(elem.gapi_app_permission_authorize_button)

    @log_time
    def loginGAPI(self, main_window):
        # grab the other window, enter credentials
        popup_windows = [w for w in self.util.driver.window_handles if w != main_window]
        if len(popup_windows) == 0:
            return
        popup_window = popup_windows[0]
        self.util.driver.switch_to_window(popup_window)
        if self.util.isElementPresent(elem.gmail_userid_textfield):
            self.submitGoogleCredentials()

    @log_time
    def login(self):
        self.assertTrue(self.util.waitForElementToBePresent(elem.login_button, 30))
        if "localhost" in config.url:
            self.util.clickOnAndWaitFor(elem.login_button, elem.dashboard_title)
            self.authorizeGAPI()  # in case it's present
        else:
            self.util.clickOnAndWaitFor(elem.login_button, elem.gmail_password_textfield)
            self.submitGoogleCredentials()
            
        # need to check for permission screen, and if it's there
        # de-select "Remember..." if checked; then click on "Allow"
        if self.util.isElementPresent(elem.g_accounts_login_prompt):
            checkbox = self.util.driver.find_element_by_xpath(elem.g_accounts_remember_box)
            if checkbox.is_selected():
                self.util.clickOn(elem.g_accounts_remember_box)
            self.util.clickOn(elem.g_accounts_allow)
        # need to check for chrome login screen, 
        # and if it's there, click on "skip for now"
        if self.util.isElementPresent(elem.chrome_login_prompt):
            self.util.clickOn(elem.chrome_login_skip_button)
            if self.util.isElementPresent(elem.google_permission_prompt):
                self.util.clickOn(elem.google_permission_remember)
                self.util.clickOn(elem.google_permission_yes)
        self.assertTrue(self.util.waitForElementToBePresent(elem.dashboard_title),"ERROR inside login(): can't see dashboard_title")
        # finally, need to check for GAPI modal
        self.authorizeGAPI()
        self.util.waitForElementToBePresent(elem.dashboard_title)

    def ensureLHNSectionExpanded(self, section, expandMode=True):
        """expand LHN section if not already expanded; not logging because currently no "wait" step
        """
        object_left_nav_section_object_link = elem.left_nav_expand_object_section_link.replace("OBJECT", section)
        self.assertTrue(self.util.waitForElementToBePresent(object_left_nav_section_object_link),"ERROR in navigateToObject(): can't see LHN link for "+section)
        
        if expandMode == True:
            if not self.isLHNSectionExpanded(section):
                self.util.clickOn(object_left_nav_section_object_link)
        else:
            if self.isLHNSectionExpanded(section):
                self.util.clickOn(object_left_nav_section_object_link) #collapse it
        time.sleep(1)

    def isLHNSectionExpanded(self, section):
        section_status_link = str(elem.left_nav_expand_status).replace("OBJECT", section)
        return self.util.isElementPresent(section_status_link)

    @log_time
    def waitForLeftNavToLoad(self):
        # temporary method that waits for the '...) to be replaced with numbers
        self.util.waitForElementNotToBePresent(elem.left_nav_governance_controls_numbers_not_loaded)
        self.util.waitForElementNotToBePresent(elem.left_nav_governance_contracts_numbers_not_loaded)
        self.util.waitForElementNotToBePresent(elem.left_nav_governance_policies_numbers_not_loaded)
        self.util.waitForElementNotToBePresent(elem.left_nav_governance_regulations_numbers_not_loaded)
        self.util.scroll()  # temporary workaround to refresh the page which will make the title appear (known bug)

    def generateNameForTheObject(self,grc_object):
        random_number= self.getTimeId()
        name = grc_object + "-auto-test"+random_number
        return name

    #@log_time
    def createObject(self, grc_object, object_name="", private_checkbox="unchecked", open_new_object_window_from_lhn = True, owner=""):
        print "Start creating object: " + grc_object
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
            self.util.clickOn(elem.modal_window_private_checkbox)
        self.saveNewObjectAndWait()
        #in the standard create object flow, verify the new object is created happens vi LHN, for audits tests this verification should happen in the mapping modal window
        if open_new_object_window_from_lhn:
            # uncheck box if it is checked
            self.uncheckMyWorkBox()
            last_created_object_link = self.verifyObjectIsCreatedinLHN(grc_object, grc_object_name)
            time.sleep(2)
            return last_created_object_link
        else:
            print "verifying create object in mapping window"
            #commented the verifycation for now
            last_created_object_link = self.verifyObjectIsCreatedInSections(grc_object_name)
        print "Object created successfully."

    @log_time
    # @author: Ukyo. Create program with input parameter as object
    # usage:  do.createDetailedObject(standard_object, "Standard")
    def createDetailedObject(self, myObject, object_type="", private_checkbox="unchecked", open_new_object_window_from_lhn = True, owner=""):
        self.closeOtherWindows()
        if myObject.program_elements.get("title") == "":
            grc_object_name = self.generateNameForTheObject(object_type)
        else:
            if object_type == 'Program':
                grc_object_name = myObject.program_elements['title']
            elif object_type == 'Standard':
                grc_object_name = myObject.standard_elements['title']

            
        #in the standard create object flow, a new window gets open via Create link in the LHN, in audit tests the new object gets created via + link, and that's why
        #openCreateNewObjectWindowFromLhn have to be skipped
        if open_new_object_window_from_lhn:
            self.openCreateNewObjectWindowFromLhn(object_type) 
        self.populateNewDetailedObjectData(myObject)
        if private_checkbox == "checked":
            self.util.clickOn(elem.modal_window_private_checkbox)
        self.saveNewObjectAndWait()
        #in the standard create object flow, verify the new object is created happens vi LHN, for audits tests this verification should happen in the mapping modal window
        if open_new_object_window_from_lhn:
            # uncheck box if it is checked
            self.uncheckMyWorkBox()
            last_created_object_link = self.verifyObjectIsCreatedinLHN(object_type, grc_object_name)
            return last_created_object_link
        else:
            print "verifying create object in mapping window"
            #commented the verifycation for now
            last_created_object_link = self.verifyObjectIsCreatedInSections(grc_object_name)
        print "Object created successfully."
        

    # @log_time
    # @author: Ukyo. Create program with input parameter as object
    # usage:  do.createDetailedObject(standard_object, "Standard")
    # you can add 10 objects, say Standard1 .... Standard10 by setting loopManyTimes=10
    def createObjectIncrementingNaming(self, myObject, object_type="", loopManyTimes=0, firstEntryName="", private_checkbox="unchecked", open_new_object_window_from_lhn = True, owner=""):
        self.closeOtherWindows()
                        
        #in the standard create object flow, a new window gets open via Create link in the LHN, in audit tests the new object gets created via + link, and that's why
        #openCreateNewObjectWindowFromLhn have to be skipped
        if open_new_object_window_from_lhn:
            self.openCreateNewObjectWindowFromLhn(object_type) 
        self.populateNewDetailedObjectDataIncrementing(myObject, object_type, loopManyTimes, firstEntryName)
        time.sleep(2) #allows time to save

        

        

    @log_time
    def saveNewObjectAndWait(self):
        """Thin wrapper around a saveObjectData function to indicate this is saving a new object rather than an edited one
        """
        self.saveObjectData()

    @log_time
    def saveEditedObjectAndWait(self):
        """Thin wrapper around a saveObjectData function to indicate this is saving a new object rather than an edited one
        """
        self.saveObjectData()

    @log_time
    def NewResponseCreate(self, object_name):
        # Make sure window is there
        self.util.waitForElementToBeVisible(elem.modal_window)
        self.assertTrue(self.util.isElementPresent(elem.modal_window), "can't see modal dialog window for create new object")

        frame_element = elem.response_title.replace("FRAME_NAME", "description")

        # Populate title        
        self.assertTrue(self.util.waitForElementToBeVisible(frame_element))
        #self.util.inputTextIntoField(object_name, elem.response_title)
        self.util.typeIntoFrame(object_name, frame_element)
        self.saveNewObjectAndWait()

    @log_time
    def openCreateNewObjectWindowFromLhn(self, grc_object):
        object_left_nav_section_object_link = elem.left_nav_expand_object_section_link.replace("OBJECT", grc_object)
        self.assertTrue(self.util.waitForElementToBePresent(object_left_nav_section_object_link), "ERROR inside openCreateNewObjectWindowFromLhn():can't see the LHN link for "+ grc_object)
        result = self.util.clickOn(object_left_nav_section_object_link)
        self.assertTrue(result,"ERROR in openCreateNewObjectWindowFromLhn(): could not click on LHN link for "+grc_object)
        object_left_nav_section_object_add_button = elem.left_nav_object_section_add_button.replace("OBJECT", grc_object)
        self.assertTrue(self.util.waitForElementToBePresent(object_left_nav_section_object_add_button), "ERROR inside openCreateNewObjectWindowFromLhn():can't see the LHN Create New link for "+ grc_object)
        result = self.util.clickOn(object_left_nav_section_object_add_button)
        self.assertTrue(result, "ERROR in openCreateNewObjectWindowFromLhn(): could not click on LHN Create New link for " + grc_object)
        self.waitForCreateModalToAppear()

    # Return TRUE if the 'Add New' link exists for the specified object, e.g., "Program".  First character is capitalized and the rest is in lowercase.
    @log_time
    def doesCreateNewExist(self, grc_object):
        object_left_nav_section_object_link = elem.left_nav_expand_object_section_link.replace("OBJECT", grc_object)
        self.assertTrue(self.util.waitForElementToBePresent(object_left_nav_section_object_link), "ERROR inside openCreateNewObjectWindowFromLhn():can't see the LHN link for "+ grc_object)
        result = self.util.clickOn(object_left_nav_section_object_link)
        self.assertTrue(result,"ERROR in openCreateNewObjectWindowFromLhn(): could not click on LHN link for "+grc_object)
        object_left_nav_section_object_add_button = elem.left_nav_object_section_add_button.replace("OBJECT", grc_object)
        exist = self.util.waitForElementToBePresentNoExceptionPrinting(object_left_nav_section_object_add_button, 10)

        if exist:
            return True
        else:
            return False

    @log_time
    def waitForCreateModalToAppear(self):
        self.util.waitForElementToBeVisible(elem.modal_window)
        self.assertTrue(self.util.isElementPresent(elem.modal_window), "can't see modal dialog window for create new object")

    @log_time
    def populateNewObjectData(self, object_title, owner=""):
        self.closeOtherWindows()
        # Make sure window is there
        self.util.waitForElementToBeVisible(elem.modal_window)
        self.assertTrue(self.util.isElementPresent(elem.modal_window), "can't see modal dialog window for create new object")
        time.sleep(2)
        # Populate title
        self.util.waitForElementToBeVisible(elem.object_title)
        self.assertTrue(self.util.isElementPresent(elem.object_title), "can't access the input textfield")
        
        self.util.inputTextIntoField(object_title, elem.object_title)

    @log_time
    def populateNewDetailedObjectData(self, myObject):
        self.closeOtherWindows()
        # Make sure window is there
        self.util.waitForElementToBeVisible(elem.modal_window)
        self.assertTrue(self.util.isElementPresent(elem.modal_window), "can't see modal dialog window for create new object")

        # Populate title
        self.util.waitForElementToBeVisible(elem.object_title)
        self.assertTrue(self.util.isElementPresent(elem.object_title), "can't access the input textfield")
        
        print myObject.program_elements.get("title")
        print myObject.program_elements.get("description")
        
        self.util.inputTextIntoField(myObject.program_elements.get("title"), elem.object_title)
       
        frame_element = elem.object_iFrame.replace("FRAME_NAME","description")
        self.util.waitForElementToBeVisible(frame_element)                
        self.util.typeIntoFrame(myObject.program_elements.get("description"), frame_element)
        # TODO
       # self.util.inputTextIntoField(myObject.program_elements.get("description"), elem.object_description)


    @log_time
    # @author: Ukyo
    # Create title composing "object type" concatenated with a number, if it already exist, a next higher number is used until 1000
    # PRE-REQUISITE:  myObject['title'] should start with object type, e.g., Program, Standard, or Objective...
    def populateNewDetailedObjectDataIncrementing(self, myObject, object_type, loopManyTimes=0, pol_reg_std=""):
        title = object_type
        
        self.closeOtherWindows()
        # Make sure window is there
        self.util.waitForElementToBeVisible(elem.modal_window)
        self.assertTrue(self.util.isElementPresent(elem.modal_window), "can't see modal dialog window for create new object")

            
        # Populate title
        self.util.waitForElementToBeVisible(elem.object_title)
        self.assertTrue(self.util.isElementPresent(elem.object_title), "can't access the input textfield") 
        
        # if there already exist the duplicate title, use a next higher number
        for number in range(1, 1000):
            auto_title = title + "-auto-test" + str(datetime.datetime.now().time())
            self.util.inputTextIntoField(auto_title, elem.object_title)
            print "DEBUG : " + auto_title      
            frame_element = elem.object_iFrame.replace("FRAME_NAME","description")
            self.util.waitForElementToBeVisible(frame_element)                
            
            # TODO expand to include more
            if title == "Section":
                self.util.typeIntoFrame(myObject.section_elements.get("description"), frame_element)
                
                # policy_regulation_standard is a required field and click&select
                self.util.inputTextIntoFieldAndPressEnter(pol_reg_std, elem.section_pol_reg_std)
                matching_email_selector = elem.autocomplete_list_element_with_text2.replace("TEXT", pol_reg_std)
                self.util.waitForElementToBeVisible(matching_email_selector)
                self.util.clickOn(matching_email_selector)
                
                
            elif title == "Standard":
                self.util.typeIntoFrame(myObject.standard_elements.get("description"), frame_element)  
            elif title == "Program":
                self.util.typeIntoFrame(myObject.program_elements.get("description"), frame_element)
            elif title == "Objective":
                self.util.typeIntoFrame(myObject.objective_elements.get("description"), frame_element)      
            elif title == "Control":
                self.util.typeIntoFrame(myObject.control_elements.get("description"), frame_element)      
                
                
            self.util.clickOn(elem.modal_window_save_button)
            time.sleep(5); # allow marginal delay

            if (self.util.isElementVisible(elem.title_duplicate_warning) == False):
                self.util.waitForElementNotToBePresent(elem.modal_window, 2)
                
                if (number == loopManyTimes) or (number > loopManyTimes):
                    break;
                elif (loopManyTimes > 0) and (number < loopManyTimes):                   
                    self.openCreateNewObjectWindowFromLhn(object_type)
            else:  # duplicate
                if (number == loopManyTimes) or (number > loopManyTimes):
                    self.util.clickOn(elem.modal_window_X_button)
                    break;
                
                continue
                    
            
            

    @log_time
    def saveObjectData(self):
        self.util.waitForElementToBePresent(elem.modal_window_save_button)
        self.assertTrue(self.util.isElementPresent(elem.modal_window_save_button), "do not see the Save button")
        self.util.clickOnSave(elem.modal_window_save_button)
        self.util.waitForElementNotToBePresent(elem.modal_window)

    @log_time
    def verifyObjectIsCreatedinLHN(self, section, object_title): 
        """this helper method is generic for any type and verifies that object is created and can be clicked in LHN"""
        # Refresh the page
        self.util.refreshPage()
        
        # Wait for the object section link to appear in the left nav (e.g. Programs, Products, Policies, etc.)
        self.ensureLHNSectionExpanded(section, False)
        # -- work around for ticket 15614155 , set it to False  ----
        
        
        # Wait for the newly-created object link to appear in the left nav (e.g. System-auto-test_2013_08_25_13_47_50)
        last_created_object_link = elem.left_nav_last_created_object_link.replace("SECTION", section).replace("OBJECT_TITLE", object_title)
        self.showObjectLinkWithSearch(object_title, section)
        return last_created_object_link

    @log_time
    def verifyObjectIsCreatedinLHNViaSearch(self, search_term, section):
        object_left_nav_section_object_link_with_one_result = elem.left_nav_expand_object_section_link_one_result_after_search.replace("OBJECT", section)
        self.util.waitForElementToBePresent(elem.left_nav_sections_loaded)  # due to quick-lookup bug
        self.searchFor(search_term)
        self.util.waitForElementToBePresent(object_left_nav_section_object_link_with_one_result)
        self.assertTrue(self.util.isElementPresent(object_left_nav_section_object_link_with_one_result), "the search did not return one result as it's supposed to" )
        self.ensureLHNSectionExpanded(section)
        object_title_link = elem.left_nav_last_created_object_link.replace("SECTION", section).replace("OBJECT_TITLE", search_term)
        self.util.waitForElementToBePresent(object_title_link)
        self.assertTrue(self.util.isElementPresent(object_title_link), "ERROR inside navigateToObject(): do not see object  " + object_title_link + " in lhn" )

    @log_time
    def verifyObjectIsCreatedInSections(self, object_title):
        self.util.waitForElementToBePresent(elem.mapping_modal_selector_list_first_object_link)
        self.assertTrue(self.util.isElementPresent(elem.mapping_modal_selector_list_first_object_link), "can't see the first link in the mapping modal window")
        last_create_object_link_on_the_first_spot = elem.mapping_modal_selector_list_first_object_link_with_specific_title.replace("TITLE",object_title)
        self.util.waitForElementToBePresent(last_create_object_link_on_the_first_spot)
        self.assertTrue(self.util.isElementPresent(last_create_object_link_on_the_first_spot), "the newly create object" +object_title + " is not on the first spot or doesn't eexist")
        last_created_object_link =  self.util.getTextFromXpathString(last_create_object_link_on_the_first_spot)
        print "the newly created object is " + last_created_object_link
        self.assertEquals(last_created_object_link, object_title, "the newly created object is not in Mapping Modal Window")
        return last_created_object_link

    @log_time
    def createSectionFor(self, object,object_id,section_title):
        section_add_link = elem.mapped_object_area_section_add_link.replace("OBJECT", object).replace("ID", object_id)
        self.util.waitForElementToBePresent(section_add_link)
        self.assertTrue(self.util.isElementPresent(section_add_link), "cannot see section add + link")
       
        self.util.scrollIntoView(section_add_link)
        self.util.hoverOver(section_add_link)
        self.util.clickOn(elem.section_create_link)
        # Make sure window is there
        self.util.waitForElementToBeVisible(elem.modal_window)
        self.assertTrue(self.util.isElementPresent(elem.modal_window), "can't see modal dialog window for create new object")

        # Populate title
        self.util.waitForElementToBeVisible(elem.object_title)
        self.assertTrue(self.util.isElementPresent(elem.object_title), "can't access the input textfield")
        self.util.inputTextIntoField(section_title, elem.object_title)
        self.util.waitForElementToBeVisible(elem.object_title)
        #entering the descriptiom
        frame_element = elem.object_iFrame.replace("FRAME_NAME","description")
        self.util.typeIntoFrame(elem.theLongTextDescription1, frame_element) 
        self.saveNewObjectAndWait()

    @log_time
    def createObjectives(self, objective_title, description):
        self.util.waitForElementToBeVisible(elem.modal_window)
        self.assertTrue(self.util.isElementPresent(elem.modal_window), "can't see modal dialog window for create new object")

        # Populate title
        self.util.waitForElementToBeVisible(elem.object_title)
        self.assertTrue(self.util.isElementPresent(elem.object_title), "can't access the input textfield")
        self.util.inputTextIntoField(objective_title, elem.object_title)
        self.util.waitForElementToBeVisible(elem.object_title)
        #entering the descriptiom
        frame_element = elem.object_iFrame.replace("FRAME_NAME","description")
        self.util.typeIntoFrame(description, frame_element) 
        self.saveNewObjectAndWait()

    @log_time
    def navigateToObject(self, section, object_title_link):
        # Wait for the object section link to appear in the left nav (e.g. Programs, Products, Policies, etc.)
        object_left_nav_section_object_link = elem.left_nav_expand_object_section_link.replace("OBJECT", section)
        self.assertTrue(self.util.waitForElementToBePresent(object_left_nav_section_object_link),"ERROR in navigateToObject(): can't see LHN link for "+section)

        # Click on the object section link in the left nav
        # Wait for the newly-edited object link to appear, then click on it
        self.assertTrue(self.util.waitForElementToBePresent(object_title_link), "ERROR inside navigateToObject(): do not see object  " + object_title_link + " in lhn" )       
        result=self.util.clickOn(object_title_link)
        self.assertTrue(result,"ERROR in navigateToObject(): could not click on object in LHN "+object_title_link)
        
    @log_time
    def navigateToObjectWithExpadingLhnSection(self, section, object_title_link):
        # Wait for the object section link to appear in the left nav (e.g. Programs, Products, Policies, etc.)
        self.uncheckMyWorkBox()
        object_left_nav_section_object_link = elem.left_nav_expand_object_section_link.replace("OBJECT", section)
        self.assertTrue(self.util.waitForElementToBePresent(object_left_nav_section_object_link),"ERROR in navigateToObject(): can't see LHN link for "+section)

        # Click on the object section link in the left nav
        self.util.clickOn(object_left_nav_section_object_link)

        # Wait for the newly-edited object link to appear, then click on it
        self.util.scrollIntoView(object_title_link)
        self.assertTrue(self.util.waitForElementToBePresent(object_title_link), "ERROR inside navigateToObject(): do not see object  " + object_title_link + " in lhn" )       
        result=self.util.clickOn(object_title_link)
        self.assertTrue(result,"ERROR in navigateToObject(): could not click on object in LHN "+object_title_link)

    @log_time
    def getFirstItemFromASection(self, section):
        # Wait for the object section link to appear in the left nav (e.g. Programs, Products, Policies, etc.)
        self.uncheckMyWorkBox()
        # Click on the object section link in the left nav
        self.ensureLHNSectionExpanded(section)   
        self.util.waitForElementToBePresent(str(elem.first_item_from_a_section).replace("OBJECT", section), 10) 
        first_item_name = self.util.getTextFromXpathString(str(elem.first_item_from_a_section).replace("OBJECT", section))
        return first_item_name

    @log_time
    def showObjectLinkWithSearch(self, search_term, section):
        object_left_nav_section_object_link_with_one_result = elem.left_nav_expand_object_section_link_one_result_after_search.replace("OBJECT", section)
        self.util.waitForElementToBePresent(elem.left_nav_sections_loaded)  # due to quick-lookup bug
        time.sleep(6) # extra delay for margin of error
        self.searchFor(search_term)
        time.sleep(5) # hard wait for solving issue of ticket 15614155
        self.util.waitForElementToBePresent(object_left_nav_section_object_link_with_one_result)
        self.assertTrue(self.util.isElementPresent(object_left_nav_section_object_link_with_one_result), "the search did not return one result as it's supposed to" )
        self.ensureLHNSectionExpanded(section)
        object_title_link = elem.left_nav_last_created_object_link.replace("SECTION", section).replace("OBJECT_TITLE", search_term)
        self.util.waitForElementToBePresent(object_title_link)
        self.assertTrue(self.util.isElementPresent(object_title_link), "ERROR inside navigateToObject(): do not see object " + object_title_link + " in lhn" )

    @log_time
    # Search a specified entry from a section, e.g., "Program", and click on it
    def navigateToObjectWithSearch(self, search_term, section):
        self.showObjectLinkWithSearch(search_term, section)
        object_title_link = elem.left_nav_last_created_object_link.replace("SECTION", section).replace("OBJECT_TITLE", search_term)
        result = self.util.clickOn(object_title_link)
        time.sleep(2)
        self.assertTrue(result, "ERROR in navigateToObject(): could not click on object in LHN " + object_title_link)

    @log_time
    # Search a specified entry from a section, e.g., "Program", and click on it
    def navigateToObjectWithSearchWithNoAssertion(self, search_term, section):
        object_left_nav_section_object_link_with_one_result = elem.left_nav_expand_object_section_link_one_result_after_search.replace("OBJECT", section)
        self.util.waitForElementToBePresent(elem.left_nav_sections_loaded)  # due to quick-lookup bug
        time.sleep(6) # extra delay for margin of error
        self.searchFor(search_term)
        time.sleep(5)



    @log_time
    def navigateToObjectAndOpenObjectEditWindow(self,section,object_title_link, refresh_page=True):

        self.closeOtherWindows()

        # Wait for the object section link to appear in the left nav (e.g. Programs, Products, Policies, etc.)
        object_left_nav_section_object_link = elem.left_nav_expand_object_section_link.replace("OBJECT", section)
        self.assertTrue(self.util.waitForElementToBePresent(object_left_nav_section_object_link),"ERROR inside navigateToObjectAndOpenObjectEditWindow(): can't see object_left_nav_section_object_link")

        self.util.scrollIntoView(object_title_link)
        self.assertTrue(self.util.waitForElementToBePresent(object_title_link), "ERROR inside navigateToObjectAndOpenObjectEditWindow(): do not see the just edited object link " )       
        result=self.util.clickOn(object_title_link)
        self.assertTrue(result,"ERROR in navigateToObjectAndOpenObjectEditWindow(): could not click on just edited object link: "+object_title_link)

        # Wait for the object detail page info section on the right side to appear, then hover over it to enable the Edit button
        self.assertTrue(self.util.waitForElementToBePresent(elem.object_detail_page_info_section), "ERROR inside navigateToObjectAndOpenObjectEditWindow(): do not see object info section")
        self.util.hoverOver(elem.object_detail_page_info_section)

        # Wait for the Edit button in the object detail page info section, then click on it
        self.assertTrue(self.util.waitForElementToBePresent(elem.object_info_page_edit_link), "ERROR inside navigateToObjectAndOpenObjectEditWindow(): do not see the Edit button")
        result=self.util.clickOn(elem.object_info_page_edit_link)
        self.assertTrue(result,"ERROR in navigateToObjectAndOpenObjectEditWindow(): could not click on Edit button "+elem.object_info_page_edit_link)
        
        # Wait for the modal window to appear
        self.assertTrue(self.util.waitForElementToBePresent(elem.modal_window),"ERROR inside navigateToObjectAndOpenObjectEditWindow(): modal window does not become visible")
        
        # Wait for the field object title to appear
        self.assertTrue(self.util.waitForElementToBePresent(elem.object_title), "ERROR inside navigateToObjectAndOpenObjectEditWindow(): do not see field [title] in the edit window")

    @log_time
    def openObjectEditWindow(self):
        self.closeOtherWindows()
        self.util.hoverOver(elem.object_detail_page_info_section)
        self.assertTrue(self.util.waitForElementToBePresent(elem.object_info_page_edit_link), "ERROR inside openObjectEditWindow(): do not see the Edit button")
        result=self.util.clickOn(elem.object_info_page_edit_link)
        self.assertTrue(result,"ERROR in openObjectEditWindow(): could not click on Edit button "+elem.object_info_page_edit_link)
        self.assertTrue(self.util.waitForElementToBePresent(elem.modal_window),"ERROR inside openObjectEditWindow(): can't see modal window")
        self.assertTrue(self.util.waitForElementToBePresent(elem.object_title), "ERROR inside openObjectEditWindow(): do not see object_title in the edit window")
        time.sleep(1)

    @log_time
    def showHiddenValues(self): 
        self.util.waitForElementToBePresent(elem.modal_window_show_hidden_fields_link, 5)
        if (self.util.isElementPresent(elem.modal_window_show_hidden_fields_link)):
            result=self.util.clickOn(elem.modal_window_show_hidden_fields_link)
            self.assertTrue(result,"ERROR in showHiddenValues(): could not click on "+elem.modal_window_show_hidden_fields_link)

    @log_time
    def populateObjectInEditWindow(self, name, grcobject_elements,grcobject_values, ownerEmail="testrecip@gmail.com"):

        print "Start populate data in Edit window for object: " + name

        self.util.waitForElementToBeVisible(elem.object_title)
        self.showHiddenValues() 
        self.closeOtherWindows()
        time.sleep(3)
        for key,xpath in grcobject_elements.iteritems():
            if key in ["network_zone","kind","fraud_related","key_control", "means","type"]:
                dropdown_element = elem.object_dropdown.replace("NAME",key )
                self.util.waitForElementToBePresent(dropdown_element) 
                self.assertTrue(self.util.isElementPresent(dropdown_element), "do not see the dropdown for "+ key)
                dropdown_option = dropdown_element + "/option[" + str(grcobject_values[key]) + "]"
                self.util.waitForElementToBePresent(dropdown_option) 
                option = self.util.getTextFromXpathString(dropdown_option)
                print "the option for the dropdown " + key + " that should be selected is " + option
                self.selectFromDropdownOption(dropdown_element, grcobject_values[key])
                grcobject_values[key]=option
            if key in ["description","notes"]:                 
                frame_element = elem.object_iFrame.replace("FRAME_NAME",key)
                self.util.waitForElementToBeVisible(frame_element)
                grcobject_values[key]=key+"_"+name+ "_edited"
                self.util.typeIntoFrame(grcobject_values[key], frame_element)
            if key=="code":
                self.util.waitForElementToBePresent(xpath) 
                self.util.waitForElementToBeVisible(xpath) 
                grcobject_values[key] = self.util.getAnyAttribute(elem.object_code, "value") + "_edited"
                self.util.inputTextIntoField(grcobject_values[key] ,xpath)
            if key in ["title","scope","organization"]:
                self.util.waitForElementToBePresent(xpath)
                self.util.waitForElementToBeVisible(xpath) 
                grcobject_values[key] = name + "_edited" 
                self.util.inputTextIntoField(grcobject_values[key] ,xpath)
            if key == "owner":
                self.util.waitForElementToBePresent(xpath) 
                self.util.waitForElementToBeVisible(xpath) 
                grcobject_values[key] = ownerEmail
                owner_email = ownerEmail
                self.util.inputTextIntoField(owner_email, elem.object_owner)
                matching_email_selector = elem.autocomplete_list_element_with_text.replace("TEXT", owner_email)               
                self.util.waitForElementToBeVisible(matching_email_selector)
                self.util.hoverOver(elem.object_owner)
                self.util.clickOn(matching_email_selector)
            if key=="url":
                self.util.waitForElementToBePresent(xpath)
                self.util.waitForElementToBeVisible(xpath) 
                grcobject_values[key] = "http://www.google.com"
                self.util.inputTextIntoField(grcobject_values[key] ,xpath)
        self.assertTrue(self.util.isElementPresent(elem.modal_window_save_button), "do not see the Save button")
        self.util.waitForElementToBeVisible(elem.modal_window_save_button)
        self.saveEditedObjectAndWait()
        self.util.refreshPage()

    @log_time
    def selectFromDropdownOption(self,select_element,option_number):
        self.assertTrue(self.util.isElementPresent(select_element), "do not see the dropdown")
        self.util.waitForElementToBeVisible(select_element)
        option_to_be_selected = self.util.getTextFromXpathString(select_element + "/option[" + str(option_number) + "]")
        self.util.selectFromDropdownUntilSelected(select_element, option_to_be_selected)

    @log_time
    def verifyObjectValues(self, grcobject_elements, grcobject_values, module=""):
        self.closeOtherWindows()
        time.sleep(2) 
        for key,xpath in grcobject_elements.iteritems(): 
            
            if key in ["description","notes"]:                 
                frame_element = elem.object_iFrame.replace("FRAME_NAME",key)
                self.util.waitForElementToBePresent(frame_element)
                self.util.waitForElementToBeVisible(frame_element)
                new_value = self.util.getTextFromFrame(frame_element)
                time.sleep(5)
                print "verifyObjectValues: grcobject_values[key] : " + grcobject_values[key]
                print "verifyObjectValues:             new_value : " + new_value
                
                self.assertTrue(new_value == grcobject_values[key], "Verification ERROR: the value of " + key + " should be " + grcobject_values[key] + " but it is " + new_value )
            if key in ["network_zone","kind","fraud_related","key_control", "means","type"]:
                dropdown_element = elem.object_dropdown.replace("NAME",key )
                dropdown_element_selected_option= elem.object_dropdown_selected_option.replace("NAME",key )
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

    @log_time
    # This function click on the Delete button after Edit window is already popped up
    def deleteObject(self):
        print "Start deleting object."
        self.util.waitForElementToBePresent(elem.modal_window_delete_button)
        self.assertTrue(self.util.isElementPresent(elem.modal_window_delete_button), "ERROR: Could not delete object: Can not see the Delete button")
        result=self.util.clickOn(elem.modal_window_delete_button)
        self.assertTrue(result,"ERROR in deleteObject(): could not click on Delete button "+elem.modal_window_delete_button)
        self.waitForDeleteConfirmToAppear()
        result=self.util.clickOn(elem.modal_window_confirm_delete_button)
        self.assertTrue(result,"ERROR inside deleteObject(): could not click Confirm Delete button "+elem.modal_window_confirm_delete_button)
        self.waitForDeletionToComplete()
        print "Object deleted successfully."

    @log_time
    def waitForDeleteConfirmToAppear(self):
        status = self.util.waitForElementToBePresent(elem.modal_window_confirm_delete_button)
        self.assertTrue(status, "ERROR inside deleteObject(): Could not delete object: Could not find " + elem.modal_window_confirm_delete_button)

    @log_time
    def waitForDeletionToComplete(self):
        status=self.util.waitForElementNotToBePresent(elem.modal_window)
        self.assertTrue(status, "ERROR inside deleteObject(): Could not delete object: Modal window " + elem.modal_window + " is still present")

    @log_time
    def  getObjectIdFromHref(self, link):
        href = self.util.getAnyAttribute(link, "href")
        id = href.split("/")[-1]
        return id

    @log_time
    # Select a passed-in object category, e.g., "Standard", then select the first entry and map to it after the filtering by search
    def mapAObjectLHN(self, object, title=""):
        print "Start mapping LHN "+ object
        self.closeOtherWindows()
        self.uncheckMyWorkBox()
        # empty out search field due to LHN persistence
        self.util.inputTextIntoFieldAndPressEnter(title, elem.search_inputfield)
        self.ensureLHNSectionExpanded(object)
        first_link_of_the_section_link = elem.left_nav_first_object_link_in_the_section.replace("SECTION",object )
        print first_link_of_the_section_link
        self.assertTrue(self.util.waitForElementToBePresent(first_link_of_the_section_link), "ERROR inside mapAObjectLHN(): cannot see the first "+ object+ " in LHN")
        idOfTheObject = self.getObjectIdFromHref(first_link_of_the_section_link)      
        self.util.hoverOverAndWaitFor(first_link_of_the_section_link,elem.map_to_this_object_link)
        self.assertTrue(self.util.isElementPresent(elem.map_to_this_object_link), "no Map to link")
        result=self.util.clickOn(elem.map_to_this_object_link)
        self.assertTrue(result,"ERROR in mapAObjectLHN(): could not click on Map to link for "+object)        
        self.verifyObjectIsMapped(object,idOfTheObject )
        
    @log_time
    # Select a passed-in object category, e.g., "Standard", then select the first entry and map to it after the filtering by search
    def unmapAObjectFromWidget(self, object):
        print "Start un-mapping LHN "+ object
        objectLowercase = str(object).lower()
        
        # make sure your are on the object in inner-nav to be able to un-map it
        self.navigateToInnerNavSection(object)
        time.sleep(4)
        
        if objectLowercase == "data":
            objectLowercase = "data_asset"
        if objectLowercase == "group":
            objectLowercase = "org_group"    
        
        
        countBefore = self.countOfAnyObjectInWidget(objectLowercase)
        self.expandFirstItemInWidget(objectLowercase)
        time.sleep(2)
        self.clickOnUnmapButton()
        time.sleep(5)
        countAfter = self.countOfAnyObjectInWidget(objectLowercase)
        
        if countAfter==countBefore-1:
            print "Object " + object + " is un-mapped successfully"
            return True
        else:
            return False

    @log_time
    def waitForWidgetListToLoad(self, list_xpath):
        self.util.waitForElementToBePresent(list_xpath)
        self.util.waitForElementToBePresent(list_xpath + elem.list_loaded_suffix)

    @log_time
    def navigateToWidget(self, object):
        #click on the inner nav and wait for the corresponding widget section to become active
        inner_nav_object_link = elem.inner_nav_object_link.replace("OBJECT", object.lower())
        self.assertTrue(self.util.waitForElementToBePresent(inner_nav_object_link),"ERROR mapAObjectWidget XXX(): can't see inner_nav_object_link for " + object)
        self.util.waitForElementToBeVisible(inner_nav_object_link)
        # inject event handler before clicking
        self.util.driver.execute_script('$("body").append("{}");'.format(self.loaded_script))
        result = self.util.clickOn(inner_nav_object_link)
        self.assertTrue(result, "ERROR in mapAObjectWidget(): could not click " + inner_nav_object_link + " for object "+object)
        widget_tree = elem.section_widget_tree.replace("OBJECT", object.lower())
        self.waitForWidgetListToLoad(widget_tree)

    def navigateToMappingWindowForObject(self, object, expandables=()):
        """Set expandables to the list of object types whose footer expands when you hover over the "add" button.
        """
        self.assertTrue(self.util.waitForElementToBePresent(elem.inner_nav_section),"ERROR inside mapAObjectWidget(): can't see inner_nav_section")
        self.authorizeGAPI(1)
        self.navigateToWidget(object)
        #click on the object link in the widget to  search for other objects modal
        if object in expandables:
            open_mapping_modal_window_link = elem.section_widget_expanded_join_link1.replace("OBJECT", object.lower())
        else: 
            open_mapping_modal_window_link = elem.section_widget_join_object_link.replace("OBJECT", object).replace("_", "")
        self.util.waitForElementToBePresent(open_mapping_modal_window_link)
        self.assertTrue(self.util.isElementPresent(open_mapping_modal_window_link),"ERROR inside mapAObjectWidget(): can't see the + link for "+ object)

        print "the link that should be clicked to open the mapping modal window is " + open_mapping_modal_window_link
        # if footer is expandable, hover first, then click on submenu
        if object in expandables:
        # hover before clicking in case expander must act
            self.util.hoverOver(open_mapping_modal_window_link)
            expanded_button = elem.section_widget_expanded_join_link2.replace("OBJECT", object)
            self.util.waitForElementToBeVisible(expanded_button)
            open_map_modal_button = expanded_button
        else:
            open_map_modal_button = open_mapping_modal_window_link
        # inject event modal list catcher
        self.util.driver.execute_script('$("body").append("{}");'.format(self.map_loaded_script))
        result = self.util.clickOn(open_map_modal_button)
        self.assertTrue(result,"ERROR in mapAObjectWidget(): could not click on " + open_map_modal_button + " for object " + object)
        self.waitForFullMapModal(object)

    @log_time
    def waitForFullMapModal(self, object):
        self.waitForMapModalToAppear()
        self.waitForMapModalListToLoad()

    @log_time
    def waitForMapModalToAppear(self):
        self.assertTrue(self.util.waitForElementToBePresent(elem.mapping_modal_window), "ERROR inside mapAObjectWidget(): cannot see the mapping modal window")

    @log_time
    def waitForMapModalListToLoad(self):
        self.assertTrue(self.util.waitForElementToBePresent(elem.map_modal_loaded), "ERROR inside mapAObjectWidget(): map modal list never loads")

    @log_time
    def mapFirstObject(self, object, is_program=False):
        self.util.waitForElementToBePresent(elem.mapping_modal_selector_list_first_object)
        self.assertTrue(self.util.waitForElementToBePresent(elem.mapping_modal_selector_list_first_object), "ERROR inside mapAObjectWidget(): cannot see first object in the selector")

        # for program/person mapping, extract email for later
        if is_program and object == "Person":
            emailOfPersonToBeMapped = self.util.getTextFromXpathString(elem.mapping_modal_selector_list_first_object_email)
            print "the first Person's email is " + emailOfPersonToBeMapped
        else:  # otherwise, get ID
            idOfTheObjectToBeMapped = self.util.getAnyAttribute(elem.mapping_modal_selector_list_first_object, "data-id")
            print "the first "+ object + " id is " +  idOfTheObjectToBeMapped
        if object == self.object_type:
            # if same object type, make sure id != this object's id
            first_acceptable_map_link = elem.mapping_modal_selector_first_nonself_object_link.replace("OBJECTID", self.currentObjectId())
        else:  # otherwise, just grab first
            first_acceptable_map_link = elem.mapping_modal_selector_list_first_object_link
        self.util.waitForElementToBePresent(first_acceptable_map_link)
        self.util.clickOn(first_acceptable_map_link)
        self.util.waitForElementToBePresent(elem.mapping_modal_window_map_button)
        self.assertTrue(self.util.isElementPresent(elem.mapping_modal_window_map_button), "no Map button")
        result = self.util.clickOn(elem.mapping_modal_window_map_button)
        self.assertTrue(result, "ERROR in mapAObjectWidget(): could not click on Map button for " + object)
        
        self.util.waitForElementNotToBePresent(elem.mapping_modal_window)

        if is_program and object == "Person":
            mapped_object_link = self.verifyObjectIsMapped(object, emailOfPersonToBeMapped, is_program=is_program)
            return emailOfPersonToBeMapped
        else:
            mapped_object_link = self.verifyObjectIsMapped(object, idOfTheObjectToBeMapped, is_program=is_program)
            return idOfTheObjectToBeMapped

    @log_time
    def mapPerson(self, person):
        self.util.waitForElementToBePresent(elem.mapping_modal_window)
        self.assertTrue(self.util.isElementPresent(elem.mapping_modal_window), "do not see the modal window")
        self.util.waitForElementToBePresent(elem.mapping_modal_input_textfiled)
        self.util.inputTextIntoField(person,elem.mapping_modal_input_textfiled)

        self.util.waitForElementToBePresent(elem.mapping_modal_selector_list_first_object)
        self.assertTrue(self.util.waitForElementToBePresent(elem.mapping_modal_selector_list_first_object), "ERROR inside mapAObjectWidget(): cannot see first object in the selector")

        # for program/person mapping, extract email for later
        emailOfPersonToBeMapped = self.util.getTextFromXpathString(elem.mapping_modal_selector_list_first_object_email)
        print "the first Person's email is " + emailOfPersonToBeMapped
        self.util.waitForElementToBePresent(elem.mapping_modal_selector_list_first_object_link)
        self.util.clickOn(elem.mapping_modal_selector_list_first_object_link)
        self.util.waitForElementToBePresent(elem.mapping_modal_window_map_button)
        self.assertTrue(self.util.isElementPresent(elem.mapping_modal_window_map_button), "no Map button")
        self.util.clickOn(elem.mapping_modal_window_map_button)
        
        self.util.waitForElementNotToBePresent(elem.mapping_modal_window)
        return emailOfPersonToBeMapped

    @log_time
    def mapAObjectWidget(self, object, is_program=False, expandables=()):
        self.closeOtherWindows()
        self.navigateToMappingWindowForObject(object, expandables)
        #select the first object from the search results and map it
        self.mapFirstObject(object, is_program=is_program)
        
    @log_time
    # Unmap the first row.
    # object : singular form, lower case, e.g., data_access, org_group, 
    def unmapAnObjectFromWidget(self, object, is_program=False, expandables=()):
        # singular form, lower-case,
        # special case: data_access, org_group
        first_row = '//li[@class="tree-item governance cms_controllers_tree_view_node" and @data-object-type="OBJECT"]'
        
        self.closeOtherWindows()
        self.self.navigateToWidget(object)
        #select the first row from widget
        

    @log_time
    def verifyObjectIsMapped(self, object, objIdentifier, is_program=False, mapped_email=None):
        if is_program and object == "Person":
            objectEmail = objIdentifier
        else:
            objectId = objIdentifier
        self.assertTrue(self.util.waitForElementToBePresent(elem.inner_nav_section),"ERROR inside verifyObjectIsMapped(): can't see inner_nav_section")
        #inner_nav_object_link_with_one_object_mapped = elem.inner_nav_object_with_one_mapped_object.replace("OBJECT", object.lower())
        #self.util.waitForElementToBePresent(inner_nav_object_link_with_one_object_mapped)
        inner_nav_object_link = elem.inner_nav_object_link.replace("OBJECT", object.lower())
        self.assertTrue(self.util.waitForElementToBePresent(inner_nav_object_link),"ERROR inside verifyObjectIsMapped(): can't see inner_nav_object_link")
        self.util.waitForElementToBeVisible(inner_nav_object_link)
        #self.util.waitForElementToBeClickable(inner_nav_object_link)
        self.assertTrue(self.util.isElementPresent(inner_nav_object_link), "no inner nav link for "+ object)
        #time.sleep(2)
        result=self.util.clickOn(inner_nav_object_link)
        self.assertTrue(result,"ERROR in verifyObjectIsMapped(): could not click on "+inner_nav_object_link + " for object "+object)
        active_section = elem.section_active.replace("SECTION", object.lower())
        self.assertTrue(self.util.waitForElementToBePresent(active_section), "ERROR inside verifyObjectIsMapped(): no active section for "+ object)
        if is_program and object == "Person":
            mapped_object = elem.mapped_person_program_email.replace("EMAIL", objectEmail)
            print "the mapped object is "+ mapped_object
            # check whether the person appears in the list at all
            self.assertTrue(self.util.waitForElementToBePresent(mapped_object), "ERROR inside verifyObjectIsMapped(): Person does not appear in Program list")
            # TODO: find a way to check whether the label is "Mapped"; the below didn't work
            #relationship_label = mapped_object + elem.mapped_person_program_mapped_label
            #self.assertTrue(self.util.waitForElementToBePresent(relationship_label), 'ERROR inside verifyObjectIsMapped(): person relationship is not called "Mapped"')
        else:
            mapped_object = elem.mapped_object.replace("OBJECT", object.lower()).replace("ID", objectId)
            print "the mapped object is "+ mapped_object
            self.assertTrue(self.util.waitForElementToBePresent(mapped_object), "ERROR inside verifyObjectIsMapped(): no mapped object")
        print "Object " + object + " is mapped successfully"
        return mapped_object

    @log_time
    def navigateToInnerNavSection(self, object):
        inner_nav_object_link = elem.inner_nav_object_link.replace("OBJECT", object.lower())
        self.assertTrue(self.util.waitForElementToBePresent(inner_nav_object_link),"ERROR mapAObjectWidget XXX(): can't see inner_nav_object_link for "+object)
        self.util.waitForElementToBeVisible(inner_nav_object_link)

        result=self.util.clickOn(inner_nav_object_link)
        self.assertTrue(result,"ERROR in mapAObjectWidget(): could not click "+inner_nav_object_link + " for object "+object)
        active_section = elem.section_active.replace("SECTION", object.lower())
        self.assertTrue(self.util.waitForElementToBePresent(active_section), "ERROR inside mapAObjectWidget(): no active section for "+ object)
        
    @log_time
    def createAudit(self, program_name):
        #verify modal window
        self.util.waitForElementToBeVisible(elem.modal_window)
        self.assertTrue(self.util.isElementPresent(elem.modal_window), "can't see modal dialog window for create new object")

        #verify audit title textbox
        self.util.waitForElementToBeVisible(elem.object_title)
        self.assertTrue(self.util.isElementPresent(elem.object_title), "can't access the input textfield")

        #set a unique title
        audit_auto_populated_title = program_name + " Audit" + self.getTimeId()
        self.util.inputTextIntoField(audit_auto_populated_title, elem.object_title)
        self.util.clickOn(elem.audit_modal_autogenerate_checkbox)

        #calculate the dates - Fill in start date (current date), Planned End Date (+2months), Planned Report date from(+1month from start), Planned report date to (Planned end date + 1 week)
        start_date = date.today()
        end_date = self.add_months(start_date, 2)
          
        report_start_date = self.add_months(datetime.date.today(), 1)
        report_end_date = report_start_date + datetime.timedelta(days=7)
  
        # populate the dates
        self.enterDateWithCalendar(elem.audit_modal_start_date_input, start_date, "start date")
        self.enterDateWithCalendar(elem.audit_modal_end_date_input, end_date, "end date")
        self.enterDateWithCalendar(elem.audit_modal_report_start_date_input, report_start_date, "reporting start date")
        self.enterDateWithCalendar(elem.audit_modal_report_end_date_input, report_end_date, "reporting end date")
         
        #click on Advanced link
        self.showHiddenValues()
        frame_element = elem.object_iFrame.replace("FRAME_NAME","description")
         
        # type the description 
        self.util.waitForElementToBePresent(frame_element)
        self.assertTrue(self.util.isElementPresent(frame_element), "can't see the description frame")
        self.util.typeIntoFrame(elem.audit_modal_description_text, frame_element)
         
        # type the Firm name and select from drop-down
        self.util.waitForElementToBePresent(elem.audit_modal_firm_input_field)
        self.assertTrue(self.util.isElementPresent(elem.audit_modal_firm_input_field), "can't see the firm name input field")
        self.util.inputTextIntoField(elem.audit_modal_firm_text, elem.audit_modal_firm_input_field)
        firm_autocomplete = elem.autocomplete_list_element_with_text2.replace("TEXT", elem.audit_modal_firm_text)
        self.util.waitForElementToBePresent(firm_autocomplete)
        self.util.clickOn(firm_autocomplete)
        
        #verifying the auto-populated Audit Lead email
        self.util.waitForElementToBePresent(elem.audit_modal_audit_lead_input_field)
        self.assertTrue(self.util.isElementPresent(elem.audit_modal_audit_lead_input_field), "can't see the Audit Lead input field")
        audit_auto_populated_audit_lead = self.util.getAnyAttribute(elem.audit_modal_audit_lead_input_field,"value")
        self.assertTrue(self.current_user_email()  in audit_auto_populated_audit_lead,"not correct Audit Lead value")
        
        self.saveNewObjectAndWait()
        return audit_auto_populated_title

    @log_time
    def expandCollapseRequest(self, request_title_text):
        expand_link = str(elem.audit_pbc_request_expand_collapse_button2).replace("TITLE", request_title_text) 
        expanded_section = str(elem.audit_pbc_request_expanded).replace("TITLE",request_title_text ) 
        self.util.waitForElementToBePresent(expand_link)
        self.assertTrue(self.util.isElementPresent(expand_link), "can't see the expand link") 
        self.util.hoverOver(expand_link)
        self.util.clickOn(expand_link)
        self.util.waitForElementToBePresent(expanded_section)
        if self.util.isElementPresent(expanded_section) ==False:
            self.util.hoverOver(expand_link)
            self.util.clickOn(expand_link)
        self.assertTrue(self.util.isElementPresent(expanded_section), "can't expand the request section for " + request_title_text)

    @log_time
    def setRequestToRespondable(self, request_title_text):
        target_state_button = str(elem.audit_pbc_request_state_button).replace("TITLE", request_title_text)
        state_element = self.util.driver.find_element_by_xpath(target_state_button)
        self.util.waitForElementToBePresent(target_state_button)
        status = state_element.get_attribute('data-value')
        if status == "Requested":
            self.util.clickOn(target_state_button)

    @log_time
    def createResponse2(self, response_dict):
        self.util.waitForElementToBePresent(elem.modal_window)
        self.assertTrue(self.util.isElementPresent(elem.modal_window), "can't see modal dialog window for create new object")

    @log_time
    def createResponse(self, description):
        
        self.util.waitForElementToBeVisible(elem.modal_window)
        self.assertTrue(self.util.isElementPresent(elem.modal_window), "can't see modal dialog window for create new object")
        frame_element = elem.object_iFrame.replace("FRAME_NAME","description")
        
        # type the description 
        self.util.waitForElementToBePresent(frame_element)
        self.assertTrue(self.util.isElementPresent(frame_element), "can't see the description frame")
        self.util.typeIntoFrame(description, frame_element)
        self.saveNewObjectAndWait()

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

    @log_time
    def selectMonthYear(self, date):
        self.util.selectFromDropdownByValue(elem.datepicker_month_dropdown, str(date.month - 1))
        self.util.selectFromDropdownByValue(elem.datepicker_year_dropdown, str(date.year))

    @log_time
    def enterDateWithCalendar(self, date_field, date, field_name="the date field"):
        self.util.waitForElementToBePresent(date_field)
        self.assertTrue(self.util.isElementPresent(date_field), "can't see {} input field".format(field_name))

        # click on date field to summon calendar        
        self.util.clickOnAndWaitFor(date_field, elem.datepicker_calendar)
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

    @log_time
    def getTheIdOfTheLastCreated(self, newly_created_object_type):
        object_element = elem.data_object_element.replace("DATA_OBJECT", newly_created_object_type)
        self.util.waitForElementToBePresent(object_element)
        self.assertTrue(self.util.isElementPresent(object_element), "no " + newly_created_object_type +" have been created")
        overall_number_of_objects = str(self.util.getNumberOfOccurences(object_element))
        print "  " + str(overall_number_of_objects) + " " + newly_created_object_type + " have been created"
        last_created_object_element = elem.data_object_element_with_index.replace("DATA_OBJECT", newly_created_object_type).replace("INDEX",overall_number_of_objects )
        self.util.waitForElementToBePresent(last_created_object_element)
        self.assertTrue(self.util.isElementPresent(last_created_object_element), "cannot see the last created object")
        print last_created_object_element
        last_created_object_element_id = self.util.getAnyAttribute(last_created_object_element, "data-object-id")
        print last_created_object_element_id
        return last_created_object_element_id
    
    def getTheIdOfTheLastCreatedObjective(self, link):
       
        #overall_number_of_objectives = str(self.util.getNumberOfOccurences(elem.objective_elemet_in_the_inner_tree))
        #print str(overall_number_of_objectives) + " objectives have been created so far"
        #last_created_object_element = elem.objective_elemet_in_the_inner_tree_with_index.replace("INDEX",overall_number_of_objectives )
        print link
        last_created_object_element_id = self.util.getAnyAttribute(link, "data-object-id")
        print last_created_object_element_id
        return last_created_object_element_id

    @log_time
    def checkMyWorkBox(self):
        """ensures "My Work" box is checked, regardless of current state"""
        self.util.waitForElementToBePresent(elem.my_work_checkbox)
        checkbox = self.util.driver.find_element_by_xpath(elem.my_work_checkbox)
        if not checkbox.is_selected():
            self.util.clickOn(elem.my_work_checkbox)

    @log_time
    def uncheckMyWorkBox(self):
        time.sleep(2)
        """ensures "My Work" box is UNchecked, regardless of current state"""
        self.util.waitForElementToBePresent(elem.my_work_checkbox)
        checkbox = self.util.driver.find_element_by_xpath(elem.my_work_checkbox)
        if checkbox.is_selected():
            self.util.clickOn(elem.my_work_checkbox)
        

    @log_time
    def closeOtherWindows(self):
        current_window = self.util.driver.current_window_handle
        all_windows = self.util.driver.window_handles
        for window in all_windows:
            if window != current_window:
                self.util.driver.switch_to_window(window)
                self.util.driver.close()
        self.util.driver.switch_to_window(current_window)
        time.sleep(1)

    @log_time
    def searchFor(self, search_term):
        self.util.waitForElementToBePresent(elem.search_inputfield)
        self.assertTrue(self.util.isElementPresent(elem.search_inputfield), "no search input field")
        self.util.inputTextIntoFieldAndPressEnter(search_term, elem.search_inputfield)

    @log_time
    def scheduleMeeting(self,title, date, start_time, end_time):
        self.util.waitForElementToBeVisible(elem.modal_window)
        self.assertTrue(self.util.isElementPresent(elem.modal_window), "can't see modal dialog window for meeting")

        self.util.waitForElementToBeVisible(elem.meeting_start_time_dropdown)
        self.assertTrue(self.util.isElementPresent(elem.meeting_start_time_dropdown), "can't see meeting start time input")
        self.util.selectFromDropdownUntilSelected(elem.meeting_start_time_dropdown, start_time)

        self.util.waitForElementToBeVisible(elem.meeting_end_time_dropdown)
        self.assertTrue(self.util.isElementPresent(elem.meeting_end_time_dropdown), "can't see meeting start time input")
        self.util.selectFromDropdownUntilSelected(elem.meeting_end_time_dropdown, end_time)

        self.util.waitForElementToBeVisible(elem.meeting_title_input_textfield)
        self.assertTrue(self.util.isElementPresent(elem.meeting_title_input_textfield), "can't see meeting title input")
        self.util.inputTextIntoField(title, elem.meeting_title_input_textfield)

        self.util.waitForElementToBeVisible(elem.meeting_date)
        self.assertTrue(self.util.isElementPresent(elem.meeting_date), "can't see meeting Date input")
        self.util.inputTextIntoField(date, elem.meeting_date)
        self.saveNewObjectAndWait()

    @log_time
    def meetingSelectParticipants(self):
        self.util.waitForElementToBePresent(elem.meeting_participant_select)
        self.util.waitForElementToBePresent(elem.meeting_participant_select_first)
        self.util.waitForElementToBePresent(elem.meeting_participant_select_second)
        
        self.util.shift_key_down()
        self.util.selectFromDropdownByValue(elem.meeting_participant_select, "2")
        self.util.clickOn(elem.meeting_participant_select_first)
        self.util.shift_key_up()

    @log_time
    def verifyMeetingData(self, data, start_time, end_time):
          
        self.util.isElementPresent(elem.meeting_gcal_link)
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

    @log_time
    def dismissFlashMessages(self):
        try:
            self.util.waitForElementToBePresent(elem.flash_box)
        except:
            return
        for type_ in elem.flash_types:
            dismiss_btn = str(elem.flash_box_type_dismiss).replace("TYPE", type_)

            if self.util.isElementPresent(dismiss_btn):
                self.util.clickOn(dismiss_btn)

    @log_time
    def waitForAlertSuccessMessages(self):
        self.util.waitForElementToBePresent('//div[@class="alert alert-success"]')
        self.util.waitForElementToBePresent('//span[contains(.,"Creating Drive folder for Objective 2 for Auto Test of Audit -- Done")]')
        self.util.waitForElementToBePresent('//span[contains(.,"Creating Drive folder for Objective 1 for Auto Test of Audit -- Done")]')
        self.util.waitForElementToBePresent('//span[contains(.,"Creating Drive folder for Objective 3 for Auto Test of Audit -- Done")]')
        self.util.waitForElementToBePresent('//span[contains(.,"Linking folder")][1]')
        self.util.waitForElementToBePresent('//span[contains(.,"Linking folder")][2]')
        self.util.waitForElementToBePresent('//span[contains(.,"Linking folder")][3]')
        self.util.clickOn('//a[@class="close"]')
        self.closeOtherWindows()
        
    @log_time
    #Create a new person object from the LHN
    def createPeopleLHN(self, grcObject, save=True):
        self.util.waitForElementToBePresent(elem.new_person_name)
        self.util.inputTextIntoField(grcObject.people_elements.get("name"), elem.new_person_name)
        self.util.inputTextIntoField(grcObject.people_elements.get("email"), elem.new_person_email)
        self.util.inputTextIntoField(grcObject.people_elements.get("company"), elem.new_person_company)
        
        # default to save, unless you want to test the Cancel button
        if save==True: 
            self.util.clickOn(elem.modal_window_save_button)
        else:
            self.util.clickOn(elem.modal_window_cancel_button)

    @log_time
    #Create a new person object from the LHN
    def createPersonLHN(self, name, email, company, save=True):
        print ""
        print "Start creating person : " + name
        self.openCreateNewObjectWindowFromLhn("Person") 
        
        self.util.waitForElementToBePresent(elem.new_person_name)
        self.util.inputTextIntoField(name, elem.new_person_name)
        self.util.inputTextIntoField(email, elem.new_person_email)
        self.util.inputTextIntoField(company, elem.new_person_company)
        
        # default to save, unless you want to test the Cancel button
        if save==True: 
            self.util.clickOn(elem.modal_window_save_button)
        else:
            self.util.clickOn(elem.modal_window_cancel_button)

    @log_time
    # + Section button is already visible and displayed         
    def createSectionFromInnerNavLink(self, theName="mySectionX"):
        
        time.sleep(1)
        self.util.waitForElementToBePresent(elem.section_add_link_from_inner_nav, 20)
        
        for x in range(1,10):
            try:
                self.util.hoverOver(elem.section_add_link_from_inner_nav)      
                self.util.clickOn(elem.section_create_link_from_inner_nav)
                time.sleep(1)
                
                # is modal windom comes up, it's good.  Let's exist
                if (self.util.isElementPresent(elem.modal_window)):
                    break               
            except:
                print "Try to click on section-create link ..."
                pass
            
        
        self.populateNewObjectData(theName)
        #self.populateNewObjectData(ggrcObject.section_elements.get("title"), ggrcObject.section_elements.get("owner"))
        self.saveNewObjectAndWait()

    @log_time
    # From Inner Nav panel, with Section already created, just click on a section to do objective mapping
    def mapObjectToSectionFromInnerNav(self, theName):
        map_bt = '//div[@class="confirm-buttons"]//a'
        
        #expand the section item
        self.util.clickOn(elem.first_item_section_link_from_nav)
        self.util.waitForElementToBePresent(elem.map_object_to_section_from_nav)
 
        for x in range(1,10):
            try:
                self.util.hoverOver(elem.map_object_to_section_from_nav)
                self.util.clickOn(elem.map_object_to_section_from_nav)
                time.sleep(1)
                
                # is modal windom comes up, it's good.  Let's exist
                if (self.util.isElementPresent(map_bt)):
                    break               
            except:
                print "Try to map object ..."
                pass       
 
    @log_time
    # hover on element1 and click on element2
    def hoverAndClick(self, hoverOn, clickOn, expectedElement):         
        
        for x in range(1,10):
            try:
                self.util.hoverOver(hoverOn)
                self.util.clickOn(clickOn)
                time.sleep(1)
                
                # is modal windom comes up, it's good.  Let's exist
                if (self.util.isElementPresent(expectedElement)):
                    break               
            except:
                print "Try to hover and click on element ..."
                pass           

    # This is from, Program -> Regulation -> Section -> Object 
    # objectCategory = {Control, Objective, DataAsset, Facility, Market, Process, Product, Project, System, Person, OrgGroup}     
    def mapObjectFormFilling(self, objectCategory, searchTerm):
        map_bt = '//div[@class="confirm-buttons"]//a'
        cancel_bt = '//div[@class="deny-buttons"]//a'
        
        self._searchInMapObjectModalWindow(objectCategory, searchTerm)
        self.util.clickOn(map_bt)
        time.sleep(3)

    # Specify a category label, and title to search
    def _searchInMapObjectModalWindow(self, label, title):
        xpath = '//select[@class="input-block-level option-type-selector"]/'
        search_count_label =  '//div[@class="search-title"]/div/div/h4'
        row = '//div[@class="selector-list cms_controllers_infinite_scroll"]//li[INDEX]//div[@class="tree-title-area"]/span'

        # click on the dropdown for category
        if label == "Objectives":
            self.util.clickOn(xpath + '/option[@label="' + label + '"]')
        elif label == "Controls":
            self.util.clickOn(xpath + '/option[@label=' + label + ']')
        elif label == "Data Assets":
            self.util.clickOn(xpath + '/option[@label=' + label + ']')
        elif label == "Facilities":
            self.util.clickOn(xpath + '/option[@label=' + label + ']')
        elif label == "Org Groups":
            self.util.clickOn(xpath + '/option[@label=' + label + ']')            
        elif label == "":
            self.util.clickOn(xpath + '/option[@label=' + label + ']')            
        elif label == "Markets":
            self.util.clickOn(xpath + '/option[@label=' + label + ']')
        elif label == "Processes":
            self.util.clickOn(xpath + '/option[@label=' + label + ']')            
        elif label == "Products":
            self.util.clickOn(xpath + '/option[@label=' + label + ']')             
        elif label == "Projects":
            self.util.clickOn(xpath + '/option[@label=' + label + ']')
        elif label == "Systems":
            self.util.clickOn(xpath + '/option[@label=' + label + ']')            
        elif label == "People":
            print "xpath : " + xpath + '/option[@label=\"' + label + '\"]'
            self.util.clickOn(xpath + '/option[@label=\"' + label + '\"]')     
        
        self.util.inputTextIntoField(title, '//input[@id="search"]')
        time.sleep(6) # it auto completes and return matches
        
        count = self._countInsideParenthesis(self.util.getTextFromXpathString(search_count_label))
        
        for indx in range(1, count+1):
            row = row.replace("INDEX", str(indx))
            text = self.util.getTextFromXpathString(row)
            
            if text==title:
                self.util.clickOn(row)

    @log_time
    # Unmap from object (third) level:  from this scheme, Program->Regulation->Section->Object
    def unMapObjectFromWidgetIn3rdLevel(self, title):
            self._searchObjectIn3rdLevelAndClickOnIt(title)
        
    @log_time
    # Return xpath of row for this item if found else return False
    def _searchObjectIn3rdLevelAndClickOnIt(self, title):

        # to find out how many rows
        for x in range(500):
            xpath = '//li[@class="tree-item cms_controllers_tree_view_node" and @data-object-id="' + x + '"]'
            try:
                self.driver.find_element_by_xpath(xpath)
                continue
            except:
                return x
            
        # x is the number of count
        
        for row in range(x):
            xp = '//li[@class="tree-item cms_controllers_tree_view_node" and @data-object-id="' + row + '"]//span[@class="person-tooltip-trigger"]'
            atitle = self.util.getTextFromXpathString(xp)
            if atitle == title:
                #found it so click the row not the link
                self.util.clickOn('//li[@class="tree-item cms_controllers_tree_view_node" and @data-object-id="' + row + '"]')
                
    @log_time
    # Expand first tier, and then click on Unmap button
    def unMapObjectFromWidget(self, object_level=True):
        
        if object_level==False:
            print "Start un-mapping object from widget in the 2nd tier"
            self.util.clickOn(elem.unmap_button_from_2nd_level_regulation)
        else: 
            print "Start un-mapping object from widget in the 3rd tier"  
            self.util.waitForElementToBePresent(elem.unmap_button_from_3rd_level_object, 8) 
            self.util.clickOn(elem.unmap_button_from_3rd_level_object)
        time.sleep(4)
            
    @log_time
    # Unmap from object (third) level or from regulation (second) level, from this scheme, Program->Regulation->Section->Object
    # If not tier two then tier then 3
    def clickOnUnmapButton(self, secondTier=True):
        if secondTier==True:
            self.clickOnUnmapLink() # from second tier
        else:   
            self.util.waitForElementToBePresent(elem.unmap_button_from_3rd_level_object, 8) 
            self.util.clickOn(elem.unmap_button_from_3rd_level_object)
        
    @log_time
    # This delete function is to be used in the case, e.g., Program->Regulation->Section, and now you want to delete "Section"
    # TODO search for the named section item and delete it

    def deleteObjectFromSectionAfterMapping(self):
        self.util.waitForElementToBePresent(elem.edit_section_link_from_inner_mapping, 5)
        self.util.clickOn(elem.edit_section_link_from_inner_mapping)
        self.deleteObject()
        time.sleep(4)
        
    @log_time
    #  object is singular and lowercase
    def expandFirstItemInWidget(self, object):
        xpath = '//section[@id="' + object + '_widget"]//li[1]//div[@class="row-fluid"]'
        self.util.waitForElementToBePresent(xpath, 20)
        self.util.clickOn(xpath)
         
    @log_time
    # Object is singular, lowercase, and can be program, control, etc.  
    def expandItemWidget(self, object, title):
        xpath = '//div[@id="middle_column"]//li[INDEX]//ul[@class="tree-action-list"]/../div//div[@class="tree-title-area"][1]'
        count = self.countOfAnyObjectInWidget(object)
        
        for indx in range(1, count+1):
            xpath = xpath.replace("INDEX", str(indx))
            text = self.util.getTextFromXpathString(xpath)
            
            if text==title:
                self.util.clickOn(xpath)
                time.sleep(3)# marginal wait for the world to be acknowledged
                return True
        
        return False # can't find it
   
    @log_time
    # Expand 4th tier from mapping recursion
    def expandWidget4thTier(self, title):
        person_email_link = '//div[@id="middle_column"]//li[@class="tree-item cms_controllers_tree_view_node"]//div[@class="tree-title-area"]/span'
        row = '//div[@id="middle_column"]//li[@class="tree-item cms_controllers_tree_view_node"]//div[@class="openclose"]'
        self.util.waitForElementToBePresent(row, 20)
        text = self.util.getTextFromXpathString(row)       
        self.util.clickOn(row)
        time.sleep(2)
   
    # Click on the unmap link        
    def clickOnUnmapLink(self):
        unmap_lk = '//a[@data-toggle="unmap"]'
        self.util.waitForElementToBePresent(unmap_lk, 10)
        self.util.clickOn(unmap_lk)

    @log_time
    # Select an action to perform (Logout?  Admin Dashboard?
    def selectMenuInTopRight(self, option):
        toggle_dropdown = '//ul[@class="menu"]/li[@class="user dropdown dropdown-black black-link"]/a'
        self.util.clickOn(toggle_dropdown)       
        time.sleep(2)
        
        if option == "My Work":
            self.util.clickOn('//ul[@class="dropdown-menu"]/li[1]/a')
        elif option == "Admin Dashboard":
            self.util.waitForElementToBePresent('//ul[@class="dropdown-menu"]/li[2]/a')
            self.util.clickOn('//ul[@class="dropdown-menu"]/li[2]/a')
        elif option == "Email notifications":
            self.util.waitForElementToBePresent('//ul[@class="dropdown-menu"]/li[3]//label[1]')
            self.util.clickOn('//ul[@class="dropdown-menu"]/li[3]//label[1]')
        elif option == "Daily email digest":
            self.util.waitForElementToBePresent('//ul[@class="dropdown-menu"]/li[3]//label[2]')
            self.util.clickOn('//ul[@class="dropdown-menu"]/li[3]//label[2]')    
        elif option == "Calendar notifications":
            self.util.waitForElementToBePresent('//ul[@class="dropdown-menu"]/li[3]//label[3]')
            self.util.clickOn('//ul[@class="dropdown-menu"]/li[3]//label[3]')              
        elif option == "Save Layout":
            self.util.waitForElementToBePresent('//ul[@class="dropdown-menu"]/li[4]/a[1]')
            self.util.clickOn('//ul[@class="dropdown-menu"]/li[4]/a[1]')
        elif option == "Reset Layout":
            self.util.waitForElementToBePresent('//ul[@class="dropdown-menu"]/li[4]/a[2]')
            self.util.clickOn('//ul[@class="dropdown-menu"]/li[4]/a[2]')    
        elif option == "Logout":
            self.util.waitForElementToBePresent('//ul[@class="dropdown-menu"]/li[5]/a')
            self.util.clickOn('//ul[@class="dropdown-menu"]/li[5]/a')
        time.sleep(3)     
        
    @log_time
    # select menu items on inner nav on Admin Dashboard
    def selectMenuItemInnerNavDashBoard(self, item):       
        xpath = '//div[@class="object-nav"]/ul[@class="nav internav  cms_controllers_inner_nav ui-sortable"]'
        self.util.waitForElementToBePresent(xpath)
        
        if item=="People":
            self.util.clickOn(xpath + '/li/a[@href="#people_list_widget"]')
        elif item=="Roles":
            self.util.clickOn(xpath + '/li/a[@href="#roles_list_widget"]')
        elif item=="Events":
            self.util.clickOn(xpath + '/li/a[@href="#events_list_widget"]')
            
        time.sleep(2)        
               
    @log_time
    # Return correct count of any object
    # theObject is a singular form, e.g., Person, Objective, Standard, etc. 
    def countOfAnyObjectLHS(self, theObject):
        xpath = '//a[contains(@data-object-singular,"OBJECT")]/small/span'
        xpath = xpath.replace("OBJECT", theObject)
        self.util.waitForElementToBePresent(xpath, 15)
        
        return int(self.util.getTextFromXpathString(xpath))
    
    @log_time
    #User Role Assignment inside Admin Dashboard
    def assignUserRole(self, role):
        time.sleep(1)
        xpath = '//div[@class="selector-list people-selector"]/ul/li[INDEX]//div[@class="tree-title-area"]'
        radio_bt = '//div[@class="selector-list people-selector"]/ul/li[INDEX]//input[@type="radio"]'
        roleAssignmentCount = '//div[@class="modal modal-selector hide ui-draggable in ggrc_controllers_user_roles_modal_selector"]//div[@class="option_column"]/div[@class="search-title"]/div/div/h4'
        done = '//div[@class="confirm-buttons"]/a'
        
        text = self.util.getTextFromXpathString(roleAssignmentCount)   
        count = self._countInsideParenthesis(text)
        role = str(role).lower()
        
        for indx in range(1, count+1):
            text = self.util.getTextFromXpathString(str(xpath).replace("INDEX", str(indx))).lower()
        
            if role == text:
                self.util.clickOn(str(radio_bt).replace("INDEX", str(indx)))
                time.sleep(1)
                self.util.clickOn(done)
                time.sleep(2)
                return True
        
        return False # fail to assign
            
     
    
    
    @log_time
    # Return correct count of object in the Inner Nav
    # theObject is a singular form, and lowercase. For two words: use underscore instead of space 
    def countOfAnyObjectInnerNav(self, singularLower):
        xpath = '//div[@class="object-nav"]//li/a[@href="#' + singularLower + '_widget"]/div'
        raw_text = self.util.getTextFromXpathString(xpath)
        count = self._countInsideParenthesis(raw_text)        
        return int(count)    
    
    @log_time
    # Return correct count of object in the widget section
    # theObject is a singular form, and lowercase. For two words: use underscore instead of space 
    def countOfAnyObjectInWidget(self, singularLower):
        
        singularLower = str(singularLower).lower() #make sure lowercase
        xpath = '//section[@id="'  + singularLower + '_widget"]//span[@class="object_count"]'
        self.util.waitForElementToBePresent(xpath, 10)
        raw_text = self.util.getTextFromXpathString(str(xpath))
        count = self._countInsideParenthesis(raw_text)        
        return int(count)       
 
    @log_time
    # Add person in Admin DashBoard and return True if successful, otherwise return False
    # To test Cancel, just set Save=False
    def addPersonInAdminDB(self, name="", email="", company="", Save=True):
        
        add_person_bt = '//a[@class="btn-add" and @data-object-plural="people"]'
        pName_txtbx = '//input[@id="person_name"]'
        pEmail_txtbx = '//input[@id="person_email"]'
        pCompany_txtbx = '//input[@id="person_company"]'
        save_bt = '//div[@class="confirm-buttons"]//a[@data-toggle="modal-submit"]'
        cancel_bt = '//div[@class="deny-buttons"]//a'
        
        countBefore = self._countOfPeopleFromAdminDB()
        
        self.util.waitForElementToBePresent(add_person_bt, 10)
        self.util.clickOn(add_person_bt)
        self.util.waitForElementToBePresent(pName_txtbx, 10)  
        self.util.inputTextIntoField(name, pName_txtbx)
        self.util.inputTextIntoField(email, pEmail_txtbx)
        self.util.inputTextIntoField(company, pCompany_txtbx)
           
        if Save==True:
            self.util.clickOn(save_bt)
        else:
            self.util.clickOn(cancel_bt)
        
        self.util.waitForElementToBeVisible(add_person_bt, 10)
        time.sleep(2)
        countAfter = self._countOfPeopleFromAdminDB()       
                                            
        if (countAfter == countBefore+1):
            return True
        else:
            return False
    
    def _countOfPeopleFromAdminDB(self):
        xpathCount = '//div[@class="object-nav"]//li/a[@href="#people_list_widget"]/div'
        countText = self.util.getTextFromXpathString(xpathCount)
        count = self._countInsideParenthesis(countText)
        return count

    # count for people, roles, or events ?
    def _countOfObjectsFromAdminDB(self, item):
        
        xpathCount = '//div[@class="object-nav"]//li/a[@href="#ITEM_list_widget"]/div'
        
        if item == "people":
            xpathCount = str(xpathCount).replace("ITEM", item)
        elif item == "roles":
            xpathCount = str(xpathCount).replace("ITEM", item)
        elif item == "events":
            xpathCount = str(xpathCount).replace("ITEM", item)
                   
        countText = self.util.getTextFromXpathString(xpathCount)
        count = self._countInsideParenthesis(countText)
        return count
    
    @log_time
    # Search for person and return True if found, otherwise return False    
    def searchPersonInAdminDB(self, personName):
    # NOTE: As of Sprint 34, Dan Ring said the search function has bug and not auto filter or retur sometimes
#         search_txtbx = '//input[@name="search" and @type="text"]'
#         search_bt = '//div[@class="advanced-filters search-filters"]//button[@class="btn btn-primary" and @type="submit"]'
#         fisrt_row_email = '//section[@class="content ggrc_controllers_list_view"]/ul[@class="tree-structure new-tree tree-open"]//span[@class="email"]'
#         first_row_name = '//section[@class="content ggrc_controllers_list_view"]//span[@class="person-holder"]/a/span'      
#         self.util.waitForElementToBePresent(search_txtbx, 10)
#         self.util.inputTextIntoFieldAndPressEnter(personName, search_txtbx)
#         time.sleep(10) # do not remove, auto filter first, then search. Definitely nail it.
#         self.util.waitForElementToBePresent(search_bt, 10)
#         self.util.clickOn(search_bt)
#         self.util.waitForElementToBePresent(first_row_name, 10)
#         text =  self.util.getTextFromXpathString(first_row_name)
        
    # alternative way: search it myself
        xpathCount = '//div[@class="object-nav"]//li/a[@href="#people_list_widget"]/div'
        row = '//section[@id="people_list_widget"]//ul[@class="tree-structure new-tree"]/li[INDEX]//div[@class="tree-title-area"]/span[@class="person-holder"]/a/span'
        
        countText = self.util.getTextFromXpathString(xpathCount)
        #count = self._countInsideParenthesis(countText) + 1
        count = self._countOfPeopleFromAdminDB() + 1
        
        for indx in range(1, count):
            rowX =  str(row).replace("INDEX", str(indx))
            name = self.util.getTextFromXpathString(rowX)
              
            if personName == name:
                return True
               
        return False # outside of loop,
        
    @log_time
    # Search for the specified role and return True if found, otherwise return False    
    def searchRoleInAdminDB(self, title):
               
    # alternative way: search it myself
        xpathCount = '//div[@class="object-nav"]//li/a[@href="#roles_list_widget"]/div'
        row = '//section[@id="roles_list_widget"]/section/ul/li[INDEX]//ul[@class="tree-action-list"]/../div[@class="item-data"]/div'
        
        countText = self.util.getTextFromXpathString(xpathCount)
        count = self._countOfObjectsFromAdminDB("roles") + 1
        
        for indx in range(1, count):
            rowX =  str(row).replace("INDEX", str(indx))
            name = self.util.getTextFromXpathString(rowX)
              
            if title == name:
                print title + " role is found in the in the database."
                return True
               
        return False # outside of loop,        
        
        
    @log_time
    # Expand person row if found and return its index
    # Note: This function should not be used when text is entered in the searchbox and auto filtered because xpath is different  
    def _expandPersonInAdminDB(self, personName):
        #xpath = '//section[@id="people_list_widget"]//ul[@class="tree-structure new-tree"]/li[INDEX]//div[@class="tree-title-area"]/span[@class="email"]'
        #first_row_name = '//section[@class="content ggrc_controllers_list_view"]//span[@class="person-holder"]/a/span'
        
        xpathCount = '//div[@class="object-nav"]//li/a[@href="#people_list_widget"]/div'
        xpath = '//section[@id="people_list_widget"]//ul[@class="tree-structure new-tree"]/li[INDEX]//div[@class="tree-title-area"]/span[@class="person-holder"]/a/span'
        row = '//section[@id="people_list_widget"]//ul[@class="tree-structure new-tree"]/li[INDEX]//div[@class="tree-title-area"]'
        
        countText = self.util.getTextFromXpathString(xpathCount)
        #count = self._countInsideParenthesis(countText) + 1
        count = self._countOfPeopleFromAdminDB() + 1
        
        for index in range (1,count):
            myXPath = xpath.replace("INDEX", str(index))
            text = self.util.getTextFromXpathString(myXPath)
            if (personName == text):
                self.util.clickOn(str(row).replace("INDEX", str(index))) #click on it to expand
                time.sleep(2)
                return index
            
    @log_time
    # Expand person row if found and return its index
    # Note: This function should not be used when text is entered in the searchbox and auto filtered because xpath is different  
    def _expandPersonFirstRowInAdminDB(self, personName):
        first_row_name = '//section[@class="content ggrc_controllers_list_view"]//span[@class="person-holder"]/a/span'
        self.util.waitForElementToBePresent(first_row_name, 10)
        self.util.clickOn(first_row_name)
        return 1 #index
        
        
            
            
    @log_time
    # It will seach for the person name and click Edit Authorization link from it  
    # Pre-condition: you are already on the Admin Dashboard view
    def clickOnEditAuthorization(self, personName):
        indx = self._expandPersonInAdminDB(personName)
        #indx = self._expandPersonFirstRowInAdminDB(personName)          
        edit_auth = '//div[@id="middle_column"]//ul[@class="tree-structure new-tree tree-open"]/li[' + str(indx) + ']//div[@class="pull-right"]/a[@class="info-edit"]'
        self.util.waitForElementToBePresent(edit_auth, 15)
        self.util.clickOn(edit_auth)
        time.sleep(2)
        
    @log_time
    # It will seach for the person name and click Edit Person link from it 
    # Pre-condition: you are already on the Admin Dashboard view 
    def clickOnEditPerson(self, personName):
        indx = self._expandPersonInAdminDB(personName)       
        edit_person = '//div[@id="middle_column"]//ul[@class="tree-structure new-tree tree-open"]/li[' + str(indx) + ']//a[@data-original-title="Edit Person"]/span'
        self.util.waitForElementToBeVisible(edit_person, 15)
        self.util.clickOn(edit_person)
        time.sleep(2)

    @log_time
    # Change username and email in the log_in text file
    def changeUsernameEmail(self, usernameOld, usernameNew, emailOld, emailNew, filePath):
        # WARNING: do not attempt to remove usernameOld and emailOld, indentation will be messed up
        # and can't log back in once noop.py is not compliant to Python indentation stardard
                
        # format looks like this in noop.py file
        oldUsername = "default_user_name = \'" + usernameOld + "\'"
        oldEmail =    "default_user_email = \'" + emailOld + "\'"
        newUsername = "default_user_name = \'" + usernameNew + "\'\n"  #add new line
        newEmail =    "default_user_email = \'" + emailNew + "\'\n"
        
        #Create temp file
        fh, abs_path = mkstemp()
        new_file = open(abs_path,'w')
        old_file = open(filePath)
        
        for line in old_file:
            if oldUsername in line:
                line = newUsername
                   
            elif oldEmail in line:
                line = newEmail
            
            sys.stdout.write(line)
            new_file.write(line)
            
        new_file.close()
        close(fh)
        old_file.close()
        #Remove original file
        remove(filePath)
        #Move new file
        move(abs_path, filePath)
     
    @log_time
    # Verify that the info exists in the exported file
    def verifyPeopleExportFile(self, user, email, company, filePath):

        info = user + "," + email + "," + company

        file = open(filePath, 'r')
        return self.verifyDataInExportFile(info, filePath)
        
#         for line in file:
#             if info in line:
#                 print "This data exists in the export file: " + info
#                 file.close()
#                 return True #found
#                    
#         file.close()
#         return False #not found
 
    @log_time
    # Verify that the info exists in the exported file
    def verifyDataInExportFile(self, text2BVerified, filePath):

        file = open(filePath, 'r')
        
        for line in file:
            if text2BVerified in line:
                print text2BVerified + " is found in the exported file."
                file.close()
                return True #found
                   
        file.close()
        return False #not found   
        
    @log_time
    # Return true if data is logged to Event Log Table
    # By default, top row (index=0) is selected 
    def verifyInfoInEventLogTable(self, text2Match, index=1):
        print "Start verifying event log for text: \"" + text2Match + "\"" 
        xpath = '//ul[@class="tree-structure new-tree event-tree"]/li[' + str(index) + ']//div[@class="tree-title-area"]/ul/li[' + str(index) + ']/strong'
        self.util.waitForElementToBePresent(xpath, 10)
        text = self.util.getTextFromXpathString(xpath)
        
        if text2Match in text:
            print ""
            print text2Match + " is found in the Event Log table."
            return True
        else:
            return False
        
    
    @log_time
    # Create a rolein Admin DashBoard and return True if successful, otherwise return False
    # To test Cancel, just set Save=False
    def createRoleInAdminDB(self, role, desc="",Save=True):  #TODO expand more
        print ""
        print "Start creating role ..."
        
        create_role_bt = '//section[@id="roles_list_widget"]//ul/li//a[@class="btn-add"]'     
        role_txtbx = '//div[@id="undefined"]//input[@class="input-block-level"]'
        desc_txtbx = '//div[@id="undefined"]//ul[@id="role_description-wysihtml5-toolbar"]/../iframe'   
        save_bt = '//a[@data-toggle="modal-submit"]'
        cancel_bt = '//a[@data-dismiss="modal-reset"]'   
        
        self.util.waitForElementToBePresent(create_role_bt)
        self.util.clickOn(create_role_bt)
        time.sleep(2)
        self.util.waitForElementToBePresent(role_txtbx)   
        self.util.inputTextIntoField(role, role_txtbx)
#         self.util.clickOn(desc_txtbx)
#         self.util.hoverOver(desc_txtbx)
#         self.util.inputTextIntoField(desc, desc_txtbx)
       
        if Save==True:
            self.util.clickOn(save_bt)
            time.sleep(2)
            return True
        else:
            self.util.clickOn(cancel_bt)
            return False
            
    @log_time
    # Return number of counts for Roles
    def roleCount(self):
        xpath = '//ul[@class="nav internav  cms_controllers_inner_nav ui-sortable"]/li/a[@href="#roles_list_widget"]/div'
        text = self.util.getTextFromXpathString(xpath)       
        return self._countInsideParenthesis(text)
    
    @log_time
    # Return true if export successfully
    # Pre-condition: Your browser downloading folder is at /Users/yourUserName/Downloads/
    # what2Export is one of these:  Systems, Processes, People, Help
    def exportFile(self, what2Export, filePath=""):
        
        # remove file if it already exist in directory
        if os.path.isfile(filePath):
            os.remove(filePath)

                
        print ""
        print "Start exporting: " + what2Export
        
        imp_exp_xpath = '//div[@id="page-header"]/..//div[2]//a[@data-toggle="dropdown"]'
        
        system_exp_link = '//div[@id="page-header"]/..//ul[@class="dropdown-menu"]/li//a[@href="/admin/export/system"]'
        process_exp_link = '//div[@id="page-header"]/..//ul[@class="dropdown-menu"]/li//a[@href="/admin/export/process"]'
        people_exp_link = '//div[@id="page-header"]/..//ul[@class="dropdown-menu"]/li//a[@href="/admin/export/people"]'
        help_exp_link = '//div[@id="page-header"]/..//ul[@class="dropdown-menu"]/li//a[@href="/admin/export/help"]'
        
        success_popup = '//div[@class="alert alert-success"]/span'
        close_popup = '//div[@class="alert alert-success"]/a'
        
        self.util.waitForElementToBeVisible(imp_exp_xpath, 10)
        self.util.clickOn(imp_exp_xpath)
        
        what2Export = str(what2Export).lower()
        
        if what2Export=="systems":       
            self.util.waitForElementToBeVisible(system_exp_link, 10)
            self.util.clickOn(system_exp_link)
        elif what2Export=="processes":       
            self.util.waitForElementToBeVisible(process_exp_link, 10)
            self.util.clickOn(process_exp_link)    
        elif what2Export=="people":       
            self.util.waitForElementToBeVisible(people_exp_link, 10)
            self.util.clickOn(people_exp_link)             
        elif what2Export=="help":       
            self.util.waitForElementToBeVisible(help_exp_link, 10)
            self.util.clickOn(help_exp_link)             
                       
        self.util.waitForElementToBeVisible(success_popup, 10)
        text = self.util.getTextFromXpathString(success_popup)
        
        self.util.clickOn(close_popup)
        
        if text=="Export successful.":
            return True
        else:
            return False   
  
    def getWrongTypeMessage(self):
        msg_xpath = '//div[@id="sampleData"]/p[1]'
        text = self.util.getTextFromXpathString(msg_xpath)
        time.sleep(1)
        return text
  
  
  
  
    @log_time
    # Return true if import successfully, otherwise return False
    # Pre-condition: You are already in Admin Board.  Same for the other export functions
    # what2Import is one of these:  System, Process, People, Help
    def importFile(self, what2Import, file2Import, positiveTest=True):
        print""
        print "Start importing: " + file2Import
        
        imp_exp_xpath = '//div[@id="page-header"]/..//div[2]//a[@data-toggle="dropdown"]'       
        system_imp_link = '//div[@id="page-header"]/..//ul[@class="dropdown-menu"]/li//a[@href="/systems/import"]'
        process_imp_link = '//div[@id="page-header"]/..//ul[@class="dropdown-menu"]/li//a[@href="/processes/import"]'
        people_imp_link = '//div[@id="page-header"]/..//ul[@class="dropdown-menu"]/li//a[@href="/admin/import/people"]'
        help_imp_link = '//div[@id="page-header"]/..//ul[@class="dropdown-menu"]/li//a[@href="/admin/import/help"]'        
        choose_file_bt= '//input[@type="file"]'
        upload_bt =  '//input[@type="submit" and @value="Upload and Review"]'
        x_button = '//div[@id="sampleData"]/div/button[@class="close"]'
        error_msg = '//div[@id="sampleData"]/div[@class="alert alert-error"]'

        proceed_with_caution_bt = '//input[@type="submit" and @value="Proceed with Caution"]'

        self.util.waitForElementToBeVisible(imp_exp_xpath, 10)
        self.util.clickOn(imp_exp_xpath)
        
        if what2Import=="Systems":       
            self.util.waitForElementToBeVisible(system_imp_link, 10)
            self.util.clickOn(system_imp_link)
        elif what2Import=="Processes":       
            self.util.waitForElementToBeVisible(process_imp_link, 10)
            self.util.clickOn(process_imp_link) 
        elif what2Import=="People":       
            self.util.waitForElementToBeVisible(people_imp_link, 10)
            self.util.clickOn(people_imp_link)           
        elif what2Import=="Help":  
            self.util.waitForElementToBeVisible(help_imp_link, 10)
            self.util.clickOn(help_imp_link)
                      
        time.sleep(1)
        self.util.uploadItem(file2Import, choose_file_bt)
        self.util.clickOn(upload_bt)
        time.sleep(1)
        
        if positiveTest == True:
            self.util.clickOnAndWaitForNotPresent(proceed_with_caution_bt, choose_file_bt, 10)
            return True
        else:
            self.assertEquals("Error!", self.util.getTextFromXpathString(error_msg))
            return False
         
    def appendToFile(self, text, filePath):
        with open(filePath, "a") as myfile:
            myfile.write(text)
            myfile.close()
         
            
    # Private function.  Return only content (count in this case) from inside parenthesis
    def _countInsideParenthesis(self, text):
        start = text.index("(") + 1
        end = text.index(")")
        text = text[start:end]
        return int(text)
    
    def getElem(self):
        return self.elem
    
    def getUniqueString(self, title=""):
        auto_title = title + "-auto-test" + str(datetime.datetime.now().time())
        return auto_title
    
    def getRandomNumber(self, max=sys.maxint, min=0):
        return randint(min,max)
    
    def refresh(self):
        self.util.refreshPage()
        time.sleep(10)

    def partialMatch(self, text2Match, longText):
        text2Match = str(text2Match).lower()
        longText = str(longText).lower()
        
        if text2Match in longText:
            return True
        else:
            return False
        
    # Return a lowercase name of logged in user
    def whoAmI(self):
        user_name_displayed = '//ul[@class="menu"]//a[@class="dropdown-toggle"]/span/strong'
        return str(self.util.getTextFromXpathString(user_name_displayed)).lower()
    
    # Provided that your page is already expanded
    def getObjectNavWidgetInfo(self, which):
        xpath_username = '//div[@id="middle_column"]//section[@class="info"]//div[1]//h3'
        xpath_email = '//div[@id="middle_column"]//section[@class="info"]//div[2]//p'
        xpath_company = '//div[@id="middle_column"]//section[@class="info"]//div[3]//p'
        
        if which == "username":
            return self.util.getTextFromXpathString(xpath_username)
        elif which == "email":
            return self.util.getTextFromXpathString(xpath_email) 
        elif which == "company":
            return self.util.getTextFromXpathString(xpath_company)
        
         
        
        
        
        
    
