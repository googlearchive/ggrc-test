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
import unicodedata
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
    def submitGoogleCredentials(self, username="", password=""):
        
        if username == "" or password == "":
            self.util.inputTextIntoField(config.username, elem.gmail_userid_textfield)
            self.assertTrue(self.util.isElementPresent(elem.gmail_password_textfield), "can't see the password text field")
            self.util.inputTextIntoField(config.password, elem.gmail_password_textfield)
            self.util.clickOn(elem.gmail_submit_credentials_button)
        else:
            self.util.clickOnId("account-chooser-link")
            time.sleep(4)
            self.util.clickOnId("account-chooser-add-account")
            time.sleep(4)
            self.util.inputTextIntoField(username, elem.gmail_userid_textfield)
            self.assertTrue(self.util.isElementPresent(elem.gmail_password_textfield), "can't see the password text field")
            self.util.inputTextIntoField(password, elem.gmail_password_textfield)
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
    def login(self, username="", password=""):
        time.sleep(5)
        self.util.waitForElementToBePresent(elem.login_button)
        if "localhost" in config.url:
            self.util.clickOnAndWaitFor(elem.login_button, elem.dashboard_title)
            self.authorizeGAPI()  # in case it's present
        else:
            self.util.clickOnAndWaitFor(elem.login_button, elem.gmail_password_textfield)           
            self.submitGoogleCredentials(username, password)
            
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
        # self.assertTrue(self.util.waitForElementToBePresent(elem.dashboard_title),"ERROR inside login(): can't see dashboard_title")
        # finally, need to check for GAPI modal
        self.authorizeGAPI()
        # self.util.waitForElementToBePresent(elem.dashboard_title)
        # self.printVersion() #fail from Jenkins run on reciprocity lab because no library to parse

    def printVersion(self):
        xpath = '//section[@class="footer"]//p'
        version = self.util.getTextFromXpathString(xpath)
        print version
        

    def ensureLHNSectionExpanded(self, section, expandMode=True):
        """expand LHN section if not already expanded; not logging because currently no "wait" step
        """
        object_left_nav_section_object_link = elem.left_nav_expand_object_section_link.replace("OBJECT", section)
        self.assertTrue(self.util.waitForElementToBePresent(object_left_nav_section_object_link), "ERROR in navigateToObject(): can't see LHN link for " + section)
        
        self.showLHMenu(True)
        
        if expandMode == True:
            #if not self.isLHNSectionExpanded(section): # Feb09
                self.expandObjectGroup(section, expandMode)
                self.util.clickOn(object_left_nav_section_object_link)              
        else:
            #if self.isLHNSectionExpanded(section): COMMENT OUT# Feb09           
                self.expandObjectGroup(section, expandMode)
                #self.util.clickOn(object_left_nav_section_object_link)  # collapse it # Feb09
        time.sleep(4)
        
        

    # wait until something comes into picture, e.g., expand the LHN for an object and with until the count appears which signifies that all entries are loaded
    def waitUntilLHNCountDisplay(self, object, timeout=60):
        timer = int(timeout)
        
        if "local" in config.url:
            timer = 15;  # shorten the time            
        
        while timer > 0:
            try:  # theObject is a singular form
                count = self.countOfAnyObjectLHS(object)
                return count
            except:                
                if timer > 0:
                    timer = timer - 1
                    print "Wait count down: " + str(timer)
                else:
                    return  # time up, get out of here

    def waitUntilAEqualsB(self, A, B, timeout=60):
        timer = int(timeout)
        
        if "local" in config.url:
            timer = 30;  # shorten the time            
        
        while timer > 0:
            try:  # theObject is a singular form
                if A == B:
                    return True
                else:
                    timer = timer - 1
            except:                
                if timer > 0:
                    timer = timer - 1
                    print "Wait count down: " + str(timer)
                else:
                    return False  # time up, get out of here
        return False


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

    def generateNameForTheObject(self, grc_object):
        random_number = self.getTimeId()
        name = grc_object + "-auto-test" + random_number
        return name

    @log_time
    def createObject(self, grc_object, object_name="", private_checkbox="unchecked", open_new_object_window_from_lhn=True, owner=""):
        print "Start creating object: " + grc_object
        self.closeOtherWindows()
        if object_name == "":
            grc_object_name = self.generateNameForTheObject(grc_object)
        else:
            grc_object_name = object_name   
        
        # in the standard create object flow, a new window gets open via Create link in the LHN, in audit tests the new object gets created via + link, and that's why
        # openCreateNewObjectWindowFromLhn have to be skipped
        if open_new_object_window_from_lhn:           
            self.openCreateNewObjectWindowFromLhn(grc_object) 
        
        self.populateNewObjectData(grc_object_name, owner)      
        
        if private_checkbox == "checked":
            self.util.clickOn(elem.modal_window_private_checkbox)
        self.saveNewObjectAndWait()
        # in the standard create object flow, verify the new object is created happens vi LHN, for audits tests this verification should happen in the mapping modal window
        if open_new_object_window_from_lhn:
            # uncheck box if it is checked
            # self.uncheckMyWorkBox()
            last_created_object_link = self.verifyObjectIsCreatedinLHN(grc_object, grc_object_name)
            time.sleep(5)
            return last_created_object_link
        else:
            print "verifying create object in mapping window"
            time.sleep(5)
            # commented the verification for now
            last_created_object_link = self.verifyObjectIsCreatedInSections(grc_object_name)
        print "Object created successfully."

    @log_time
    # You must pass in an object name
    def createObjectSaveAddAnother(self, grc_object, object_name, private_checkbox="unchecked", open_new_object_window_from_lhn=True, owner="", save_and_close=True):
        print "Start creating object: " + grc_object
        self.closeOtherWindows()
        if object_name == "":
            grc_object_name = self.generateNameForTheObject(grc_object)
        else:
            grc_object_name = object_name
        self.checkMyWorkBox()  # so show only me objects, I don't care other people's
        # in the standard create object flow, a new window gets open via Create link in the LHN, in audit tests the new object gets created via + link, and that's why
        # openCreateNewObjectWindowFromLhn have to be skipped
        if open_new_object_window_from_lhn:
            self.openCreateNewObjectWindowFromLhn(grc_object) 
        
        self.populateNewObjectData(grc_object_name, owner)
        
        # if section object, need to specify other reg/pol/std field;  just pick the first link
        if grc_object == "Section":
            reg_pol_std = '//input[@data-lookup="Policy,Regulation,Standard"]'
            first_link = '//ul[contains(@class, "ui-autocomplete")]/li[1]'
            self.util.clickOn(reg_pol_std)   
            self.util.inputTextIntoField("auto", reg_pol_std)
            time.sleep(6)         
            self.util.hoverOver(first_link)
            self.util.clickOn(first_link)
        
        if private_checkbox == "checked":
            self.util.clickOn(elem.modal_window_private_checkbox)
        
        if save_and_close==True:
            self.saveNewObjectAndWait(True)
            last_created_object_link = self.verifyObjectIsCreatedinLHN(grc_object, grc_object_name)
            time.sleep(5)
            return last_created_object_link
        else:
            self.saveNewObjectAndWait(False)


    @log_time
    def createObjectWithHiddenFields(self, grc_object, object_name="", open_new_object_window_from_lhn=True, owner=""):
        print "Start creating object with hidden fields: " + grc_object
        self.closeOtherWindows()
        if object_name == "":
            grc_object_name = self.generateNameForTheObject(grc_object)
        else:
            grc_object_name = object_name
        # in the standard create object flow, a new window gets open via Create link in the LHN, in audit tests the new object gets created via + link, and that's why
        # openCreateNewObjectWindowFromLhn have to be skipped
        if open_new_object_window_from_lhn:
            self.openCreateNewObjectWindowFromLhn(grc_object) 
        
        self.populateNewObjectDataWithHiddenFields(grc_object_name, owner)
        
        self.saveNewObjectAndWait()
        # in the standard create object flow, verify the new object is created happens vi LHN, for audits tests this verification should happen in the mapping modal window
        if open_new_object_window_from_lhn:
            # uncheck box if it is checked
            self.uncheckMyWorkBox()
            last_created_object_link = self.verifyObjectIsCreatedinLHN(grc_object, grc_object_name)
            time.sleep(5)
            return last_created_object_link
        else:
            print "verifying create object in mapping window"
            time.sleep(5)
            # commented the verification for now
            last_created_object_link = self.verifyObjectIsCreatedInSections(grc_object_name)
        print "Object created successfully."
    

    @log_time
    # for quick test purpose it only verifies a few fields
    def verifyFieldsOnEditWindow(self):
        time.sleep(2)
        print "Start verify hidden fields being saved in Edit window."
        # value is embedded in the xpath
        obj_url = '//input[@value="https://www.object.com"]'
        ref_url = '//input[@value="https://www.reference.com"]'
        # verify against previously entered text       
        self.assertTrue(self.util.isElementPresent(obj_url), "Fail verify object url.")
        self.assertTrue(self.util.isElementPresent(ref_url), "Fail verify reference url.")

    @log_time
    # @author: Ukyo. Create program with input parameter as object
    # usage:  do.createDetailedObject(standard_object, "Standard")
    def createDetailedObject(self, myObject, object_type="", private_checkbox="unchecked", open_new_object_window_from_lhn=True, owner=""):
        self.closeOtherWindows()
        if myObject.program_elements.get("title") == "":
            grc_object_name = self.generateNameForTheObject(object_type)
        else:
            if object_type == 'Program':
                grc_object_name = myObject.program_elements['title']
            elif object_type == 'Standard':
                grc_object_name = myObject.standard_elements['title']

            
        # in the standard create object flow, a new window gets open via Create link in the LHN, in audit tests the new object gets created via + link, and that's why
        # openCreateNewObjectWindowFromLhn have to be skipped
        if open_new_object_window_from_lhn:
            self.openCreateNewObjectWindowFromLhn(object_type) 
        self.populateNewDetailedObjectData(myObject)
        if private_checkbox == "checked":
            self.util.clickOn(elem.modal_window_private_checkbox)
        self.saveNewObjectAndWait()
        # in the standard create object flow, verify the new object is created happens vi LHN, for audits tests this verification should happen in the mapping modal window
        if open_new_object_window_from_lhn:
            # uncheck box if it is checked
            self.uncheckMyWorkBox()
            last_created_object_link = self.verifyObjectIsCreatedinLHN(object_type, grc_object_name)
            return last_created_object_link
        else:
            print "verifying create object in mapping window"
            # commented the verifycation for now
            last_created_object_link = self.verifyObjectIsCreatedInSections(grc_object_name)
        print "Object created successfully."
        

    # @log_time
    # @author: Ukyo. Create program with input parameter as object
    # usage:  do.createDetailedObject(standard_object, "Standard")
    # you can add 10 objects, say Standard1 .... Standard10 by setting loopManyTimes=10
    def createObjectIncrementingNaming(self, myObject, object_type="", loopManyTimes=0, firstEntryName="", private_checkbox="unchecked", open_new_object_window_from_lhn=True, owner=""):
        self.closeOtherWindows()
                        
        # in the standard create object flow, a new window gets open via Create link in the LHN, in audit tests the new object gets created via + link, and that's why
        # openCreateNewObjectWindowFromLhn have to be skipped
        if open_new_object_window_from_lhn:
            self.openCreateNewObjectWindowFromLhn(object_type) 
        self.populateNewDetailedObjectDataIncrementing(myObject, object_type, loopManyTimes, firstEntryName)
        time.sleep(2)  # allows time to save

        

        

    @log_time
    # True = Save & Close
    # False = Save & Add Another
    def saveNewObjectAndWait(self, saveAndClose=True):
        """Thin wrapper around a saveObjectData function to indicate this is saving a new object rather than an edited one
        """
        self.saveObjectData(saveAndClose)

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
        # self.util.inputTextIntoField(object_name, elem.response_title)
        self.util.typeIntoFrame(object_name, frame_element)
        self.saveNewObjectAndWait()

    @log_time
    def expandObjectGroup(self, section, expand=True):
        if section in ("Regulation", "Policy", "Standard", "Contract", "Clause", "Section"):       
            if expand==True:
                if (self.util.isElementCSSPresent(elem.obj_directives_grp_collapsed_css))==True:
                    self.util.clickOnCSS(elem.obj_directives_grp_collapsed_css)
            else:
                if (self.util.isElementCSSPresent(elem.obj_directives_grp_expanded_css))==True:
                    self.util.clickOnCSS(elem.obj_directives_grp_expanded_css)
        
        # control & objectives        
        if section in ("Control", "Objective"):       
            if expand==True:
                if (self.util.isElementCSSPresent(elem.obj_ctrl_objectives_grp_collapsed_css))==True:
                    self.util.clickOnCSS(elem.obj_ctrl_objectives_grp_collapsed_css)
            else:
                if (self.util.isElementCSSPresent(elem.obj_ctrl_objectives_grp_expanded_css))==True:
                    self.util.clickOnCSS(elem.obj_ctrl_objectives_grp_expanded_css)        
        
        # people & org group & vendor
        if section in ("Person", "OrgGroup", "Vendor"):       
            if expand==True:
                if (self.util.isElementCSSPresent(elem.obj_people_grp_collapsed_css))==True:
                    self.util.clickOnCSS(elem.obj_people_grp_collapsed_css)
            else:
                if (self.util.isElementCSSPresent(elem.obj_people_grp_expanded_css))==True:
                    self.util.clickOnCSS(elem.obj_people_grp_expanded_css)

        # assets & business
        if section in ("System", "Process", "DataAsset", "Product", "Facility", "Market"):       
            if expand==True:
                if (self.util.isElementCSSPresent(elem.obj_asset_business_grp_collapsed_css))==True:
                    self.util.clickOnCSS(elem.obj_asset_business_grp_collapsed_css)
            else:
                if (self.util.isElementCSSPresent(elem.obj_asset_business_grp_expanded_css))==True:
                    self.util.clickOnCSS(elem.obj_asset_business_grp_expanded_css)

    @log_time
    def openCreateNewObjectWindowFromLhn(self, grc_object):

        self.ensureLHNSectionExpanded(grc_object)
        
        object_left_nav_section_object_add_button = elem.left_nav_object_section_add_button.replace("OBJECT", grc_object)
        self.assertTrue(self.util.waitForElementToBePresent(object_left_nav_section_object_add_button), "ERROR inside openCreateNewObjectWindowFromLhn():can't see the LHN Create New link for " + grc_object)
        result = self.util.clickOn(object_left_nav_section_object_add_button)
        self.assertTrue(result, "ERROR in openCreateNewObjectWindowFromLhn(): could not click on LHN Create New link for " + grc_object)
        self.waitForCreateModalToAppear()
        time.sleep(2)

    # Return TRUE if the 'Add New' link exists for the specified object, e.g., "Program".  First character is capitalized and the rest is in lowercase.
    @log_time
    def doesCreateNewExist(self, grc_object):
        object_left_nav_section_object_link = elem.left_nav_expand_object_section_link.replace("OBJECT", grc_object)
        self.assertTrue(self.util.waitForElementToBePresent(object_left_nav_section_object_link), "ERROR inside openCreateNewObjectWindowFromLhn():can't see the LHN link for " + grc_object)
        result = self.util.clickOn(object_left_nav_section_object_link)
        self.assertTrue(result, "ERROR in openCreateNewObjectWindowFromLhn(): could not click on LHN link for " + grc_object)
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
        time.sleep(2)
        # Make sure window is there
        self.util.waitForElementToBeVisible(elem.modal_window)
        self.assertTrue(self.util.isElementPresent(elem.modal_window), "can't see modal dialog window for create new object")        
        # Populate title
        self.util.waitForElementToBeVisible(elem.object_title)
        self.assertTrue(self.util.isElementPresent(elem.object_title), "can't access the input textfield")
        
        self.util.inputTextIntoField(object_title, elem.object_title)

    @log_time
    # also have one item not hidden (on purpose)
    def populateNewObjectDataWithHiddenFields(self, object_title, owner=""):    
        self.populateNewObjectData(object_title, owner)
        
        # populate some arbitrary fields and hide them
        self.util.waitForElementToBePresent(elem.private_program_chkbx)
        self.util.clickOn(elem.private_program_chkbx)
        self.util.waitForElementToBePresent(elem.reference_url)
        self.util.inputTextIntoField("https://www.object.com", elem.object_url)  # will display the whole time
        self.util.inputTextIntoField("https://www.reference.com", elem.reference_url)
        time.sleep(1)

        self.util.clickOn(elem.hide_new_private_program)
        self.assertTrue(self.util.isElementPresent(elem.new_private_program_hidden))
        self.util.clickOn(elem.hide_reference_url)
        self.assertTrue(self.util.isElementPresent(elem.new_program_reference_url_hidden))        
        time.sleep(3)

    def assertLevel(self, element, hidden=True):
        if hidden==True:
            self.assertTrue(element)
        else:
            self.assertFalse(element)

    @log_time
    # assertHidden is whether you verify fields are hidden or shown
    def _testAllFieldsOnModal(self, object, isHidden=True):
        # TODO add codes in
        # need to check it's not person, workflow, audit
        
        if object=="workflow":
            self.assertLevel(self.util.isElementPresent(elem.hidden_owner_modal), isHidden)
            self.assertLevel(self.util.isElementPresent(elem.hidden_description_modal), isHidden)
            self.assertLevel(self.util.isElementCSSPresent(elem.hidden_frequency_modal_css), isHidden)
            self.assertLevel(self.util.isElementCSSPresent(elem.hidden_email_preferences_modal_css), isHidden)
            self.assertLevel(self.util.isElementCSSPresent(elem.hidden_first_task_groups_title_modal_css), isHidden)
            self.assertLevel(self.util.isElementCSSPresent(elem.hidden_custom_email_message_modal_css), isHidden)            
        elif object=="audit":
            self.assertLevel(self.util.isElementCSSPresent(elem.hidden_status_modal_css), isHidden)
            self.assertLevel(self.util.isElementCSSPresent(elem.hidden_auto_generate_modal_css), isHidden)
            self.assertLevel(self.util.isElementCSSPresent(elem.hidden_planned_start_date_modal_css), isHidden)
            self.assertLevel(self.util.isElementCSSPresent(elem.hidden_planned_end_date_modal_css), isHidden)
            self.assertLevel(self.util.isElementCSSPresent(elem.hidden_planned_report_period_from_modal_css), isHidden)
            self.assertLevel(self.util.isElementCSSPresent(elem.hidden_planned_report_period_to_modal_css), isHidden)
            self.assertLevel(self.util.isElementCSSPresent(elem.hidden_auditors_modal_css), isHidden)
            self.assertLevel(self.util.isElementCSSPresent(elem.hidden_audit_firm_modal_css), isHidden)
            self.assertLevel(self.util.isElementPresent(elem.hidden_description_modal), isHidden)
        elif object=="person":
            self.assertLevel(self.util.isElementCSSPresent(elem.hidden_company_modal_css), isHidden)
            self.assertLevel(self.util.isElementCSSPresent(elem.hidden_enabled_user_modal_css), isHidden)
        else: # for all other objects             
            # satisfy the most basic except workflow and audit: "clause", "section", 
            self.assertLevel(self.util.isElementPresent(elem.hidden_owner_modal), isHidden)
            self.assertLevel(self.util.isElementPresent(elem.hidden_contact_modal), isHidden)
            self.assertLevel(self.util.isElementPresent(elem.object_new_prgm_desc_hidden), isHidden)
            self.assertLevel(self.util.isElementPresent(elem.new_note_hidden), isHidden) 
            self.assertLevel(self.util.isElementPresent(elem.hidden_reference_url_modal), isHidden)
            self.assertLevel(self.util.isElementPresent(elem.hidden_code_modal), isHidden)
                                        
            if object != "clause" and \
               object != "section":    
                # test more fields specifically related                                                
                self.assertLevel(self.util.isElementPresent(elem.hidden_url_modal), isHidden)
                self.assertLevel(self.util.isElementPresent(elem.hidden_state_modal), isHidden) 
                self.assertLevel(self.util.isElementPresent(elem.hidden_description_modal), isHidden)
                
                if object != "objective": 
                    self.assertLevel(self.util.isElementPresent(elem.hidden_effective_date_modal), isHidden) 
                    self.assertLevel(self.util.isElementPresent(elem.hidden_stop_date_modal), isHidden) 
                    
                    # "regulation", "contract", "org_group", "vendor", "data_asset","project","facility","market", "standard"   
                    # These have all those fields in the above
                                        
                    # test more fields specifically related
                    if object == "program":
                        self.assertLevel(self.util.isElementPresent(elem.hidden_private_program_modal), isHidden)
                    elif object == "policy":
                        self.assertLevel(self.util.isElementPresent(elem.hidden_kind_type_modal), isHidden)                  
                    elif object == "control":
                        self.assertLevel(self.util.isElementCSSPresent(elem.hidden_kind_nature_modal_css), isHidden)
                        self.assertLevel(self.util.isElementCSSPresent(elem.hidden_fraud_related_modal_css), isHidden)
                        self.assertLevel(self.util.isElementCSSPresent(elem.hidden_significance_modal_css), isHidden)
                        self.assertLevel(self.util.isElementCSSPresent(elem.hidden_type_means_modal_css), isHidden)
                        self.assertLevel(self.util.isElementCSSPresent(elem.hidden_frequency_modal_css), isHidden)
                        self.assertLevel(self.util.isElementCSSPresent(elem.hidden_assertion_modal_css), isHidden)
                        self.assertLevel(self.util.isElementCSSPresent(elem.hidden_categories_modal_css), isHidden)
                        self.assertLevel(self.util.isElementCSSPresent(elem.hidden_principal_assessor_modal_css), isHidden)
                        self.assertLevel(self.util.isElementCSSPresent(elem.hidden_fraud_related_modal_css), isHidden)
                        self.assertLevel(self.util.isElementCSSPresent(elem.hidden_secondary_assessor_modal_css), isHidden)                       
                    elif object == "system" or \
                         object == "process":  
                        self.assertLevel(self.util.isElementPresent(elem.hidden_network_zone_modal), isHidden)     
                    elif object == "product":
                        self.assertLevel(self.util.isElementPresent(elem.hidden_kind_type_modal), isHidden) 
        
    def _testIndividualFieldsOnModal(self, list):
        if "owner" in list:
            self.assertFalse(self.util.isElementPresent(elem.hidden_owner_modal))
            self.util.clickOn(elem.hide_owner_modal)
            self.assertTrue(self.util.isElementPresent(elem.hidden_owner_modal))   
        if "contact" in list:
            self.assertFalse(self.util.isElementPresent(elem.hidden_contact_modal))
            self.util.clickOn(elem.hide_contact_modal)
            self.assertTrue(self.util.isElementPresent(elem.hidden_contact_modal))  
        if "url" in list:
            self.assertFalse(self.util.isElementPresent(elem.hidden_url_modal))
            self.util.clickOn(elem.hide_url_modal)
            self.assertTrue(self.util.isElementPresent(elem.hidden_url_modal))  
        if "reference_url" in list:
                    
            if object == "program":
                ref_url = elem.hide_program_reference_url_modal                      
            else:
                ref_url = elem.hide_reference_url_modal
            # if is needed because program is abnormally has reference id pre-assigned                           
            self.assertFalse(self.util.isElementPresent(elem.hidden_reference_url_modal))
            self.util.clickOn(ref_url)
            self.assertTrue(self.util.isElementPresent(elem.hidden_reference_url_modal))                  
        if "code" in list:
            self.assertFalse(self.util.isElementPresent(elem.hidden_code_modal))
            self.util.clickOn(elem.hide_code_modal)
            self.assertTrue(self.util.isElementPresent(elem.hidden_code_modal))                   
        if "effective_date" in list:
            self.assertFalse(self.util.isElementPresent(elem.hidden_effective_date_modal))
            self.util.clickOn(elem.hide_effective_date_modal)                  
            self.assertTrue(self.util.isElementPresent(elem.hidden_effective_date_modal))
        if "stop_date" in list:
            self.assertFalse(self.util.isElementPresent(elem.hidden_stop_date_modal))
            self.util.clickOn(elem.hide_stop_date_modal)
            self.assertTrue(self.util.isElementPresent(elem.hidden_stop_date_modal))
        if "state" in list:
            self.assertFalse(self.util.isElementPresent(elem.hidden_state_modal))
            self.util.clickOn(elem.hide_state_modal)
            self.assertTrue(self.util.isElementPresent(elem.hidden_state_modal))
        # seems like description an note are candidates for using xpath
        if "description" in list:
            self.assertFalse(self.util.isElementPresent(elem.object_new_prgm_desc_hidden))
            self.util.clickOn(elem.hide_description_modal)
            self.assertTrue(self.util.isElementPresent(elem.object_new_prgm_desc_hidden))
        if "note" in list:
            self.assertFalse(self.util.isElementPresent(elem.new_note_hidden))
            self.util.clickOn(elem.hide_note_modal)
            self.assertTrue(self.util.isElementPresent(elem.new_note_hidden))
        if "private_program" in list:
            self.assertFalse(self.util.isElementPresent(elem.hidden_private_program_modal))
            self.util.clickOn(elem.hide_private_program_modal)
            self.assertTrue(self.util.isElementPresent(elem.hidden_private_program_modal))
        if "kind_type" in list:
            self.assertFalse(self.util.isElementPresent(elem.hidden_kind_type_modal))
            self.util.clickOn(elem.hide_kind_type_modal)
            self.assertTrue(self.util.isElementPresent(elem.hidden_kind_type_modal))
        if "network_zone" in list:
            self.assertFalse(self.util.isElementPresent(elem.hidden_network_zone_modal))
            self.util.clickOn(elem.hidden_network_zone_modal)
            self.assertTrue(self.util.isElementPresent(elem.hidden_network_zone_modal))
        if "kind_nature" in list:
            self.assertFalse(self.util.isElementCSSPresent(elem.hidden_kind_nature_modal_css))
            self.util.clickOnCSS(elem.hidden_kind_nature_modal_css)
            self.assertTrue(self.util.isElementCSSPresent(elem.hidden_kind_nature_modal_css))            
        if "fraud_related" in list:
            self.assertFalse(self.util.isElementCSSPresent(elem.hidden_fraud_related_modal_css))
            self.util.clickOnCSS(elem.hidden_fraud_related_modal_css)
            self.assertTrue(self.util.isElementCSSPresent(elem.hidden_fraud_related_modal_css))             
        if "significance" in list:
            self.assertFalse(self.util.isElementCSSPresent(elem.hidden_significance_modal_css))
            self.util.clickOnCSS(elem.hidden_significance_modal_css)
            self.assertTrue(self.util.isElementCSSPresent(elem.hidden_significance_modal_css))             
        if "type_means" in list:
            self.assertFalse(self.util.isElementCSSPresent(elem.hidden_type_means_modal_css))
            self.util.clickOnCSS(elem.hidden_type_means_modal_css)
            self.assertTrue(self.util.isElementCSSPresent(elem.hidden_type_means_modal_css))            
        if "frequency" in list:
            self.assertFalse(self.util.isElementCSSPresent(elem.hidden_frequency_modal_css))
            self.util.clickOnCSS(elem.hidden_frequency_modal_css)
            self.assertTrue(self.util.isElementCSSPresent(elem.hidden_frequency_modal_css))             
        if "assertion" in list:
            self.assertFalse(self.util.isElementCSSPresent(elem.hidden_assertion_modal_css))
            self.util.clickOnCSS(elem.hidden_assertion_modal_css)
            self.assertTrue(self.util.isElementCSSPresent(elem.hidden_assertion_modal_css))        
        if "categories" in list:
            self.assertFalse(self.util.isElementCSSPresent(elem.hidden_categories_modal_css))
            self.util.clickOnCSS(elem.hidden_categories_modal_css)
            self.assertTrue(self.util.isElementCSSPresent(elem.hidden_categories_modal_css))            
        if "principal_assessor" in list:
            self.assertFalse(self.util.isElementCSSPresent(elem.hidden_principal_assessor_modal_css))
            self.util.clickOnCSS(elem.hidden_principal_assessor_modal_css)
            self.assertTrue(self.util.isElementCSSPresent(elem.hidden_principal_assessor_modal_css))             
        if "secondary_assessor" in list:
            self.assertFalse(self.util.isElementCSSPresent(elem.hidden_secondary_assessor_modal_css))
            self.util.clickOnCSS(elem.hidden_secondary_assessor_modal_css)
            self.assertTrue(self.util.isElementCSSPresent(elem.hidden_secondary_assessor_modal_css))        
        if "company" in list:
            self.assertFalse(self.util.isElementCSSPresent(elem.hidden_company_modal_css))
            self.util.clickOnCSS(elem.hidden_company_modal_css)
            self.assertTrue(self.util.isElementCSSPresent(elem.hidden_company_modal_css))        
        if "enabled_user" in list:
            self.assertFalse(self.util.isElementCSSPresent(elem.hidden_enabled_user_modal_css))
            self.util.clickOnCSS(elem.hidden_enabled_user_modal_css)
            self.assertTrue(self.util.isElementCSSPresent(elem.hidden_enabled_user_modal_css))            
        if "status" in list:
            self.assertFalse(self.util.isElementCSSPresent(elem.hidden_status_modal_css))
            self.util.clickOnCSS(elem.hidden_status_modal_css)
            self.assertTrue(self.util.isElementCSSPresent(elem.hidden_status_modal_css))             
        if "auto_generate" in list:
            self.assertFalse(self.util.isElementCSSPresent(elem.hidden_auto_generate_modal_css))
            self.util.clickOnCSS(elem.hidden_auto_generate_modal_css)
            self.assertTrue(self.util.isElementCSSPresent(elem.hidden_auto_generate_modal_css))        
        if "planned_start_date" in list:
            self.assertFalse(self.util.isElementCSSPresent(elem.hidden_planned_start_date_modal_css))
            self.util.clickOnCSS(elem.hidden_planned_start_date_modal_css)
            self.assertTrue(self.util.isElementCSSPresent(elem.hidden_planned_start_date_modal_css))        
        if "planned_end_date" in list:
            self.assertFalse(self.util.isElementCSSPresent(elem.hidden_planned_end_date_modal_css))
            self.util.clickOnCSS(elem.hidden_planned_end_date_modal_css)
            self.assertTrue(self.util.isElementCSSPresent(elem.hidden_planned_end_date_modal_css))        
        if "planned_report_period_from" in list:
            self.assertFalse(self.util.isElementCSSPresent(elem.hidden_planned_report_period_from_modal_css))
            self.util.clickOnCSS(elem.hidden_planned_report_period_from_modal_css)
            self.assertTrue(self.util.isElementCSSPresent(elem.hidden_planned_report_period_from_modal_css))            
        if "planned_report_period_to" in list:
            self.assertFalse(self.util.isElementCSSPresent(elem.hidden_planned_report_period_to_modal_css))
            self.util.clickOnCSS(elem.hidden_planned_report_period_to_modal_css)
            self.assertTrue(self.util.isElementCSSPresent(elem.hidden_planned_report_period_to_modal_css))             
        if "auditors" in list:
            self.assertFalse(self.util.isElementCSSPresent(elem.hidden_auditors_modal_css))
            self.util.clickOnCSS(elem.hidden_auditors_modal_css)
            self.assertTrue(self.util.isElementCSSPresent(elem.hidden_auditors_modal_css))        
        if "audit_firm" in list:
            self.assertFalse(self.util.isElementCSSPresent(elem.hidden_audit_firm_modal_css))
            self.util.clickOnCSS(elem.hidden_audit_firm_modal_css)
            self.assertTrue(self.util.isElementCSSPresent(elem.hidden_audit_firm_modal_css))            
        if "first_task_groups_title" in list:
            self.assertFalse(self.util.isElementCSSPresent(elem.hidden_first_task_groups_title_modal_css))
            self.util.clickOnCSS(elem.hidden_first_task_groups_title_modal_css)
            self.assertTrue(self.util.isElementCSSPresent(elem.hidden_first_task_groups_title_modal_css))             
        if "email_preferences" in list:
            self.assertFalse(self.util.isElementCSSPresent(elem.hidden_email_preferences_modal_css))
            self.util.clickOnCSS(elem.hidden_email_preferences_modal_css)
            self.assertTrue(self.util.isElementCSSPresent(elem.hidden_email_preferences_modal_css))  
        if "custom_email_message" in list:
            self.assertFalse(self.util.isElementCSSPresent(elem.hidden_custom_email_message_modal_css))
            self.util.clickOnCSS(elem.hidden_custom_email_message_modal_css)
            self.assertTrue(self.util.isElementCSSPresent(elem.hidden_custom_email_message_modal_css))            

    @log_time
    # It reads a list of fields to populate for the described object
    # TODO TODO
    # Applicable to  {Regulation, Standard, Contract,  
    def hideInNewModal(self, list, isHidden=True, object="", owner=""):

        print "Start testing hide/show function ..." 
        
        # if title exist that means modal is in view 
        self.util.waitForElementToBePresent(elem.title_modal)
                  
        if isHidden == True:
            # regardless of current state, just want to hide all
            if "all" in list:
                # hide_all is visible
                if self.util.isElementIdPresent(elem.hide_all_id) == True:
                    self.util.clickOnId(elem.hide_all_id)
                    show_all_text = str(self.util.getTextFromIdString(elem.show_all_id))
                    self.assertEqual("Show all optional fields", str.strip(show_all_text), "Show all text mismatch.")
                    
                    # verify that all non-mandatory fields are hidden
                    self._testAllFieldsOnModal(object, True)

                # show_all is currently visible, click on it to see "hide all", then click on hide_all    
                elif self.util.isElementIdPresent(elem.show_all_id) == True:
                    self.util.clickOnId(elem.show_all_id)  # even if one item is hidden, showAll displays
                    self.util.waitForElementIdToBePresent(elem.hide_all_id)
                    self.util.clickOnId(elem.hide_all_id)
                    
                    # verify that all non-mandatory fields are hidden
                    self._testAllFieldsOnModal(object, True)                   
                
                # verify show_all text after hide_all is clicked
                show_all_text = str(self.util.getTextFromIdString(elem.show_all_id))
                self.assertEqual("Show all optional fields", str.strip(show_all_text), "Show all text mismatch.")               
                # take snapshot
            # hide individual item(s)
            else:               
                self._testIndividualFieldsOnModal(list)
        else:
            # cannot unhide individual item so if show button exist click on it
            if self.util.isElementIdPresent(elem.show_all_id) == True:
                self.util.clickOnId(elem.show_all_id)
                self.assertEquals("Hide all optional fields", self.util.getTextFromIdString(elem.hide_all_id), "Hide all optional fields text is not shown.")
                 
                # verify hide_all text after show_all is clicked
                hide_all_text = str(self.util.getTextFromIdString(elem.hide_all_id))
                self.assertEqual("Hide all optional fields", str.strip(hide_all_text), "Hide all text mismatch.")
                self._testAllFieldsOnModal(object, isHidden)
                

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
       
        frame_element = elem.object_iFrame.replace("FRAME_NAME", "description")
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
            frame_element = elem.object_iFrame.replace("FRAME_NAME", "description")
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
            time.sleep(5);  # allow marginal delay

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
    # To use Save & Add Another, pass 'False' as input
    def saveObjectData(self, saveAndClose=True):
        
        if saveAndClose==True:
            save_button = elem.modal_window_save_button
        else:
            save_button = elem.modal_window_save_add_another_button
                        
        self.util.waitForElementToBePresent(save_button)
        self.assertTrue(self.util.isElementPresent(save_button), "do not see the Save button")
        self.util.clickOnSave(save_button)
        time.sleep(10)

    @log_time
    def verifyObjectIsCreatedinLHN(self, section, object_title): 
        """this helper method is generic for any type and verifies that object is created and can be clicked in LHN"""
        # Refresh the page
        self.util.refreshPage()
        
        # Wait for the object section link to appear in the left nav (e.g. Programs, Products, Policies, etc.)
        self.ensureLHNSectionExpanded(section, True)  # Feb09 change to True
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
        self.assertTrue(self.util.isElementPresent(object_left_nav_section_object_link_with_one_result), "the search did not return one result as it's supposed to")
        self.ensureLHNSectionExpanded(section)
        object_title_link = elem.left_nav_last_created_object_link.replace("SECTION", section).replace("OBJECT_TITLE", search_term)
        self.util.waitForElementToBePresent(object_title_link)
        self.assertTrue(self.util.isElementPresent(object_title_link), "ERROR inside navigateToObject(): do not see object  " + object_title_link + " in lhn")

    @log_time
    def verifyObjectIsCreatedInSections(self, object_title):
        self.util.waitForElementToBePresent(elem.mapping_modal_selector_list_first_object_link)
        self.assertTrue(self.util.isElementPresent(elem.mapping_modal_selector_list_first_object_link), "can't see the first link in the mapping modal window")
        last_create_object_link_on_the_first_spot = elem.mapping_modal_selector_list_first_object_link_with_specific_title.replace("TITLE", object_title)
        self.util.waitForElementToBePresent(last_create_object_link_on_the_first_spot)
        self.assertTrue(self.util.isElementPresent(last_create_object_link_on_the_first_spot), "the newly create object" + object_title + " is not on the first spot or doesn't eexist")
        last_created_object_link = self.util.getTextFromXpathString(last_create_object_link_on_the_first_spot)
        print "the newly created object is " + last_created_object_link
        self.assertEquals(last_created_object_link, object_title, "the newly created object is not in Mapping Modal Window")
        return last_created_object_link

    @log_time
    def createSectionFor(self, object, object_id, section_title):
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
        # entering the descriptiom
        frame_element = elem.object_iFrame.replace("FRAME_NAME", "description")
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
        # entering the descriptiom
        frame_element = elem.object_iFrame.replace("FRAME_NAME", "description")
        self.util.typeIntoFrame(description, frame_element) 
        self.saveNewObjectAndWait()

    @log_time
    def navigateToObject(self, section, object_title_link):
        # Wait for the object section link to appear in the left nav (e.g. Programs, Products, Policies, etc.)
        object_left_nav_section_object_link = elem.left_nav_expand_object_section_link.replace("OBJECT", section)
        self.assertTrue(self.util.waitForElementToBePresent(object_left_nav_section_object_link), "ERROR in navigateToObject(): can't see LHN link for " + section)

        # Click on the object section link in the left nav
        # Wait for the newly-edited object link to appear, then click on it
        self.assertTrue(self.util.waitForElementToBePresent(object_title_link), "ERROR inside navigateToObject(): do not see object  " + object_title_link + " in lhn")       
        result = self.util.clickOn(object_title_link)
        self.assertTrue(result, "ERROR in navigateToObject(): could not click on object in LHN " + object_title_link)
        
    @log_time
    def navigateToObjectWithExpadingLhnSection(self, section, object_title_link):
        # Wait for the object section link to appear in the left nav (e.g. Program, Product, Policy, etc.)
        self.uncheckMyWorkBox()
        object_left_nav_section_object_link = elem.left_nav_expand_object_section_link.replace("OBJECT", section)
        self.assertTrue(self.util.waitForElementToBePresent(object_left_nav_section_object_link), "ERROR in navigateToObject(): can't see LHN link for " + section)

        # Click on the object section link in the left nav
        self.util.clickOn(object_left_nav_section_object_link)

        # Wait for the newly-edited object link to appear, then click on it
        self.util.scrollIntoView(object_title_link)
        self.assertTrue(self.util.waitForElementToBePresent(object_title_link), "ERROR inside navigateToObject(): do not see object  " + object_title_link + " in lhn")       
        result = self.util.clickOn(object_title_link)
        self.assertTrue(result, "ERROR in navigateToObject(): could not click on object in LHN " + object_title_link)

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
        time.sleep(2)  # extra delay for margin of error
        self.searchFor(search_term)
        time.sleep(5)  # hard wait for solving issue of ticket 15614155
        self.util.waitForElementToBePresent(object_left_nav_section_object_link_with_one_result)
        self.assertTrue(self.util.isElementPresent(object_left_nav_section_object_link_with_one_result), "the search did not return one result as it's supposed to")
        self.ensureLHNSectionExpanded(section)
        time.sleep(8)
        object_title_link = elem.left_nav_last_created_object_link.replace("SECTION", section).replace("OBJECT_TITLE", search_term)
        self.util.waitForElementToBePresent(object_title_link)
        self.assertTrue(self.util.isElementPresent(object_title_link), "ERROR inside navigateToObject(): do not see object " + object_title_link + " in lhn")

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
        time.sleep(6)  # extra delay for margin of error
        self.searchFor(search_term)
        time.sleep(5)



    @log_time
    def navigateToObjectAndOpenObjectEditWindow(self, section, object_title_link, refresh_page=True):

        self.closeOtherWindows()

        # Wait for the object section link to appear in the left nav (e.g. Programs, Products, Policies, etc.)
        object_left_nav_section_object_link = elem.left_nav_expand_object_section_link.replace("OBJECT", section)
        self.assertTrue(self.util.waitForElementToBePresent(object_left_nav_section_object_link), "ERROR inside navigateToObjectAndOpenObjectEditWindow(): can't see object_left_nav_section_object_link")

        self.util.scrollIntoView(object_title_link)
        self.assertTrue(self.util.waitForElementToBePresent(object_title_link), "ERROR inside navigateToObjectAndOpenObjectEditWindow(): do not see the just edited object link ")       
        result = self.util.clickOn(object_title_link)
        self.assertTrue(result, "ERROR in navigateToObjectAndOpenObjectEditWindow(): could not click on just edited object link: " + object_title_link)

        # Wait for the object detail page info section on the right side to appear, then hover over it to enable the Edit button
        self.assertTrue(self.util.waitForElementToBePresent(elem.object_detail_page_info_section), "ERROR inside navigateToObjectAndOpenObjectEditWindow(): do not see object info section")
        self.util.hoverOver(elem.object_detail_page_info_section)

        # Wait for the Edit button in the object detail page info section, then click on it
        self.clickInfoPageEditLink()
        
        # Wait for the modal window to appear
        self.assertTrue(self.util.waitForElementToBePresent(elem.modal_window), "ERROR inside navigateToObjectAndOpenObjectEditWindow(): modal window does not become visible")
        
        # Wait for the field object title to appear
        self.assertTrue(self.util.waitForElementToBePresent(elem.object_title), "ERROR inside navigateToObjectAndOpenObjectEditWindow(): do not see field [title] in the edit window")

    def clickInfoPageEditLink(self):
        self.assertTrue(self.util.clickOnCSS(elem.page_edit_gear_icon_css), "Gear icon for edit does not exist.")    
        self.assertTrue(self.util.clickOnCSS(elem.page_edit_link_css), "Page edit link does not exist.")  
        time.sleep(5)

    def isInfoPageEditLinkPresent(self):
        self.assertTrue(self.util.clickOnCSS(elem.page_edit_gear_icon_css), "Gear icon for edit does not exist.") 
        return self.util.isElementPresent(elem.page_edit_link_css)

    @log_time
    def openObjectEditWindow(self):
        self.closeOtherWindows()
        self.clickInfoPageEditLink()
        self.assertTrue(self.util.waitForElementToBePresent(elem.modal_window), "ERROR inside openObjectEditWindow(): can't see modal window")
        self.assertTrue(self.util.waitForElementToBePresent(elem.object_title), "ERROR inside openObjectEditWindow(): do not see object_title in the edit window")
        time.sleep(1)

    @log_time
    # lower-case please
    # Hide individual field or all
    # showOrHide tells whether you want to show or hide
    # list contains items to show or hide, "all" is a short hand for all
    def hideInProgramNewModal(self, hide=True, list=""):
        print "Start calling hide/show function ...hide=" + str(hide) 
        
        # if title exist that means modal is in view 
        self.util.waitForElementToBePresent(elem.object_title)
        time.sleep(3) 
          
        if hide == True:
            # regardless of current state, just want to hide all
            if "all" in list:
                # hide_all is visible
                if self.util.isElementPresent(elem.hide_all) == True:
                    self.util.clickOn(elem.hide_all)
                    time.sleep(10)
                    # verify that all non-mandatory fields are hidden
                    self.assertTrue(self.util.isElementPresent(elem.object_new_prgm_desc_hidden))
                    self.assertTrue(self.util.isElementPresent(elem.new_private_program_hidden))
                    self.assertTrue(self.util.isElementPresent(elem.new_note_hidden))
                    self.assertTrue(self.util.isElementPresent(elem.new_program_owner_hidden)) 
                    self.assertTrue(self.util.isElementPresent(elem.new_program_contact_hidden))
                    self.assertTrue(self.util.isElementPresent(elem.new_program_url_hidden)) 
                    self.assertTrue(self.util.isElementPresent(elem.new_program_reference_url_hidden)) 
                    self.assertTrue(self.util.isElementPresent(elem.new_program_code_hidden)) 
                    self.assertTrue(self.util.isElementPresent(elem.new_program_effective_date_hidden)) 
                    self.assertTrue(self.util.isElementPresent(elem.new_program_stop_date_hidden)) 
                    self.assertTrue(self.util.isElementPresent(elem.new_program_state_dropdown_hidden))                      
                # show_all is currently visible, click on it to see "hide all", then click on hide_all    
                elif self.util.isElementPresent(elem.show_all) == True:
                    self.util.clickOn(elem.show_all)  # even if one item is hidden, showAll displays
                    time.sleep(3)
                    self.util.waitForElementToBePresent(elem.hide_all)
                    self.util.clickOn(elem.hide_all)
                    time.sleep(5)
                    self.assertTrue(self.util.isElementPresent(elem.object_new_prgm_desc_hidden))
                    self.assertTrue(self.util.isElementPresent(elem.new_private_program_hidden))
                    self.assertTrue(self.util.isElementPresent(elem.new_note_hidden))
                    self.assertTrue(self.util.isElementPresent(elem.new_program_owner_hidden)) 
                    self.assertTrue(self.util.isElementPresent(elem.new_program_contact_hidden))
                    self.assertTrue(self.util.isElementPresent(elem.new_program_url_hidden)) 
                    self.assertTrue(self.util.isElementPresent(elem.new_program_reference_url_hidden)) 
                    self.assertTrue(self.util.isElementPresent(elem.new_program_code_hidden)) 
                    self.assertTrue(self.util.isElementPresent(elem.new_program_effective_date_hidden)) 
                    self.assertTrue(self.util.isElementPresent(elem.new_program_stop_date_hidden)) 
                    self.assertTrue(self.util.isElementPresent(elem.new_program_state_dropdown_hidden))
                
                # verify show_all text after hide_all is clicked
                show_all_text = str(self.util.getTextFromIdString(elem.show_all_id))
                self.assertEqual("Show all optional fields", str.strip(show_all_text), "Show all text mismatch.")               
                # take snapshot
                self.getScreenshot("screen_program_hide_all")
            # hide individual item(s)
            else:
                if "description" in list:
                    self.assertFalse(self.util.isElementPresent(elem.object_new_prgm_desc_hidden))
                    self.util.clickOn(elem.hide_object_descriptionx)
                    time.sleep(7)
                    self.assertTrue(self.util.isElementPresent(elem.object_new_prgm_desc_hidden))
                if "private" in list:
                    self.assertFalse(self.util.isElementPresent(elem.new_private_program_hidden))
                    self.util.clickOn(elem.hide_new_private_program)
                    time.sleep(3)
                    self.assertTrue(self.util.isElementPresent(elem.new_private_program_hidden))
                if "note" in list:
                    self.assertFalse(self.util.isElementPresent(elem.new_note_hidden))
                    self.util.clickOn(elem.hide_new_note)
                    time.sleep(3)
                    self.assertTrue(self.util.isElementPresent(elem.new_note_hidden))
                if "owner" in list:
                    self.assertFalse(self.util.isElementPresent(elem.new_program_owner_hidden))
                    self.util.clickOn(elem.hide_new_program_owner)
                    time.sleep(3)
                    self.assertTrue(self.util.isElementPresent(elem.new_program_owner_hidden))   
                if "contact" in list:
                    self.assertFalse(self.util.isElementPresent(elem.new_program_contact_hidden))
                    self.util.clickOn(elem.hide_contact)
                    time.sleep(3)
                    self.assertTrue(self.util.isElementPresent(elem.new_program_contact_hidden))  
                if "url" in list:
                    self.assertFalse(self.util.isElementPresent(elem.new_program_url_hidden))
                    self.util.clickOn(elem.hide_object_url)
                    time.sleep(3)
                    self.assertTrue(self.util.isElementPresent(elem.new_program_url_hidden))  
                if "reference_url" in list:
                    self.assertFalse(self.util.isElementPresent(elem.new_program_reference_url_hidden))
                    self.util.clickOn(elem.hide_reference_url)
                    time.sleep(3)
                    self.assertTrue(self.util.isElementPresent(elem.new_program_reference_url_hidden))  
                if "code" in list:
                    self.assertFalse(self.util.isElementPresent(elem.new_program_code_hidden))
                    self.util.clickOn(elem.hide_new_code)
                    time.sleep(3)
                    self.assertTrue(self.util.isElementPresent(elem.new_program_code_hidden))                   
                if "effective_date" in list:
                    self.assertFalse(self.util.isElementPresent(elem.new_program_effective_date_hidden))
                    self.util.clickOn(elem.hide_new_effective_date)
                    time.sleep(3)                    
                    self.assertTrue(self.util.isElementPresent(elem.new_program_effective_date_hidden))
                if "stop_date" in list:
                    self.assertFalse(self.util.isElementPresent(elem.new_program_stop_date_hidden))
                    self.util.clickOn(elem.hide_new_stop_date)
                    time.sleep(3)
                    self.assertTrue(self.util.isElementPresent(elem.new_program_stop_date_hidden))
                if "state" in list:
                    self.assertFalse(self.util.isElementPresent(elem.new_program_state_dropdown_hidden))
                    self.util.clickOn(elem.hide_new_state_dropdown)
                    time.sleep(3)
                    self.assertTrue(self.util.isElementPresent(elem.new_program_state_dropdown_hidden))
        else:
            # cannot unhide individual item so if show button exist click on it
            if self.util.isElementPresent(elem.show_all) == True:
                self.util.clickOn(elem.show_all)
                 
                # verify hide_all text after show_all is clicked
                hide_all_text = str(self.util.getTextFromIdString(elem.hide_all_id))
                self.assertEqual("Hide all optional fields", str.strip(hide_all_text), "Hide all text mismatch.")
         
    @log_time
    # lower-case please
    # Hide individual field or all
    # showOrHide tells whether you want to show or hide
    # list contains items to show or hide, "all" is a short hand for all
    def hideInRegulationNewModal(self, hide=True, list=""):
        print "Start calling hide/show function ...hide=" + str(hide) 
        
#         # if title exist that means modal is in view 
#         self.util.waitForElementToBePresent(elem.object_title)
#         time.sleep(3) 
#           
#         if hide==True:
#             # regardless of current state, just want to hide all
#             if "all" in list:
#                 # hide_all is visible
#                 if self.util.isElementPresent(elem.hide_all)==True:
#                     self.util.clickOn(elem.hide_all)
#                     time.sleep(10)
#                     #verify that all non-mandatory fields are hidden
#                     self.assertTrue(self.util.isElementPresent(elem.object_new_description_hidden))
#                     self.assertTrue(self.util.isElementPresent(elem.new_note_hidden))
#                     self.assertTrue(self.util.isElementPresent(elem.new_owner_hidden)) 
#                     self.assertTrue(self.util.isElementPresent(elem.new_contact_hidden))
#                     self.assertTrue(self.util.isElementPresent(elem.new_url_hidden)) 
#                     self.assertTrue(self.util.isElementPresent(elem.new_reference_url_hidden)) 
#                     self.assertTrue(self.util.isElementPresent(elem.new_code_hidden)) 
#                     self.assertTrue(self.util.isElementPresent(elem.new_effective_date_hidden)) 
#                     self.assertTrue(self.util.isElementPresent(elem.new_stop_date_hidden)) 
#                     self.assertTrue(self.util.isElementPresent(elem.new_state_dropdown_hidden))                      
#                 # show_all is currently visible, click on it to see "hide all", then click on hide_all    
#                 elif self.util.isElementPresent(elem.show_all)==True:
#                     self.util.clickOn(elem.show_all) #even if one item is hidden, showAll displays
#                     time.sleep(3)
#                     self.util.waitForElementToBePresent(elem.hide_all)
#                     self.util.clickOn(elem.hide_all)
#                     time.sleep(5)
#                     self.assertTrue(self.util.isElementPresent(elem.object_new_description_hidden))
#                     self.assertTrue(self.util.isElementPresent(elem.new_note_hidden))
#                     self.assertTrue(self.util.isElementPresent(elem.new_owner_hidden)) 
#                     self.assertTrue(self.util.isElementPresent(elem.new_contact_hidden))
#                     self.assertTrue(self.util.isElementPresent(elem.new_url_hidden)) 
#                     self.assertTrue(self.util.isElementPresent(elem.new_reference_url_hidden)) 
#                     self.assertTrue(self.util.isElementPresent(elem.new_code_hidden)) 
#                     self.assertTrue(self.util.isElementPresent(elem.new_effective_date_hidden)) 
#                     self.assertTrue(self.util.isElementPresent(elem.new_stop_date_hidden)) 
#                     self.assertTrue(self.util.isElementPresent(elem.new_state_dropdown_hidden))
#                 
#                 # verify show_all text after hide_all is clicked
#                 show_all_text = str(self.util.getTextFromIdString(elem.show_all_id))
#                 self.assertEqual("Show all optional fields", str.strip(show_all_text), "Show all text mismatch.")               
#                 # take snapshot
#                 self.getScreenshot("screen_regulation_hide_all")
#             # hide individual item(s)
#             else:
#                 if "description" in list:
#                     self.assertFalse(self.util.isElementPresent(elem.object_new_description_hidden))
#                     self.util.clickOn(elem.hide_object_descriptionx)
#                     time.sleep(7)
#                     self.assertTrue(self.util.isElementPresent(elem.object_new_description_hidden))
#                 if "note" in list:
#                     self.assertFalse(self.util.isElementPresent(elem.new_note_hidden))
#                     self.util.clickOn(elem.hide_new_note)
#                     time.sleep(3)
#                     self.assertTrue(self.util.isElementPresent(elem.new_note_hidden))
#                 if "owner" in list:
#                     self.assertFalse(self.util.isElementPresent(elem.new_owner_hidden))
#                     self.util.clickOn(elem.hide_new_owner)
#                     time.sleep(3)
#                     self.assertTrue(self.util.isElementPresent(elem.new_owner_hidden))   
#                 if "contact" in list:
#                     self.assertFalse(self.util.isElementPresent(elem.new_contact_hidden))
#                     self.util.clickOn(elem.hide_contact)
#                     time.sleep(3)
#                     self.assertTrue(self.util.isElementPresent(elem.new_contact_hidden))  
#                 if "url" in list:
#                     self.assertFalse(self.util.isElementPresent(elem.new_url_hidden))
#                     self.util.clickOn(elem.hide_object_url)
#                     time.sleep(3)
#                     self.assertTrue(self.util.isElementPresent(elem.new_url_hidden))  
#                 if "reference_url" in list:
#                     self.assertFalse(self.util.isElementPresent(elem.new_reference_url_hidden))
#                     self.util.clickOn(elem.hide_reference_url)
#                     time.sleep(3)
#                     self.assertTrue(self.util.isElementPresent(elem.new_reference_url_hidden))  
#                 if "code" in list:
#                     self.assertFalse(self.util.isElementPresent(elem.new_code_hidden))
#                     self.util.clickOn(elem.hide_new_code)
#                     time.sleep(3)
#                     self.assertTrue(self.util.isElementPresent(elem.new_code_hidden))                   
#                 if "effective_date" in list:
#                     self.assertFalse(self.util.isElementPresent(elem.new_effective_date_hidden))
#                     self.util.clickOn(elem.hide_new_effective_date)
#                     time.sleep(3)                    
#                     self.assertTrue(self.util.isElementPresent(elem.new_effective_date_hidden))
#                 if "stop_date" in list:
#                     self.assertFalse(self.util.isElementPresent(elem.new_stop_date_hidden))
#                     self.util.clickOn(elem.hide_new_stop_date)
#                     time.sleep(3)
#                     self.assertTrue(self.util.isElementPresent(elem.new_stop_date_hidden))
#                 if "state" in list:
#                     self.assertFalse(self.util.isElementPresent(elem.new_state_dropdown_hidden))
#                     self.util.clickOn(elem.hide_new_state_dropdown)
#                     time.sleep(3)
#                     self.assertTrue(self.util.isElementPresent(elem.new_state_dropdown_hidden))
#         else:
#             # cannot unhide individual item so if show button exist click on it
#             if self.util.isElementPresent(elem.show_all)==True:
#                 self.util.clickOn(elem.show_all)
#                 time.sleep(10)
#                  
#                 # verify hide_all text after show_all is clicked
#                 hide_all_text = str(self.util.getTextFromIdString(elem.hide_all_id))
#                 self.assertEqual("Hide all optional fields", str.strip(hide_all_text), "Hide all text mismatch.")         
         
                
    @log_time
    def populateObjectInEditWindow(self, name, grcobject_elements, grcobject_values, ownerEmail="testrecip@gmail.com"):

        print "Start populate data in Edit window for object: " + name

        self.util.waitForElementToBeVisible(elem.object_title)
        self.closeOtherWindows()
        time.sleep(3)
        for key, xpath in grcobject_elements.iteritems():
            if key in ["network_zone", "kind", "fraud_related", "key_control", "means", "type"]:
                dropdown_element = elem.object_dropdown.replace("NAME", key)
                self.util.waitForElementToBePresent(dropdown_element) 
                self.assertTrue(self.util.isElementPresent(dropdown_element), "do not see the dropdown for " + key)
                
                dropdown_option = dropdown_element + "/option[" + str(grcobject_values[key]) + "]"
                self.util.waitForElementToBePresent(dropdown_option) 
                option = self.util.getTextFromXpathString(dropdown_option)
                print "the option for the dropdown " + key + " that should be selected is " + option
                self.selectFromDropdownOption(dropdown_element, grcobject_values[key])
                
                # COMMENT THIS IS STUPID LINE OUT. IT CAUSES FAILURE WHEN THIS CODE IS RUN THE SECOND TIME
                # grcobject_values[key]=option
            if key in ["description", "notes"]:                 
                frame_element = elem.object_iFrame.replace("FRAME_NAME", key)
                self.util.waitForElementToBeVisible(frame_element)
                grcobject_values[key] = key + "_" + name + "_edited"
                self.util.typeIntoFrame(grcobject_values[key], frame_element)
            if key == "code":
                self.util.waitForElementToBePresent(xpath) 
                self.util.waitForElementToBeVisible(xpath) 
                grcobject_values[key] = self.util.getAnyAttribute(elem.object_code, "value") + "_edited"
                self.util.inputTextIntoField(grcobject_values[key] , xpath)
            if key in ["title", "scope", "organization"]:
                self.util.waitForElementToBePresent(xpath)
                self.util.waitForElementToBeVisible(xpath) 
                grcobject_values[key] = name + "_edited" 
                self.util.inputTextIntoField(grcobject_values[key] , xpath)
            if key == "owner":
                self.util.waitForElementCSSToBePresent(elem.add_owner_css)
                self.util.clickOnCSS(elem.owner_delete_1st_icon_css) #remove the first owner
                self.util.clickOnCSS(elem.add_owner_css) 
                grcobject_values[key] = ownerEmail
                owner_email = ownerEmail
                self.util.inputTextIntoField(owner_email, elem.object_owner)
                matching_email_selector = elem.autocomplete_list_element_with_text.replace("TEXT", owner_email)               
                self.util.waitForElementToBeVisible(matching_email_selector)
                self.util.hoverOver(elem.object_owner)
                self.util.clickOn(matching_email_selector)
            if key == "url":
                self.util.waitForElementToBePresent(xpath)
                self.util.waitForElementToBeVisible(xpath) 
                grcobject_values[key] = "http://www.google.com"
                self.util.inputTextIntoField(grcobject_values[key] , xpath)
        self.assertTrue(self.util.isElementPresent(elem.modal_window_save_button), "do not see the Save button")
        self.util.waitForElementToBeVisible(elem.modal_window_save_button)
        self.saveEditedObjectAndWait()
        self.util.refreshPage()

    @log_time
    def selectFromDropdownOption(self, select_element, option_number):
        self.assertTrue(self.util.isElementPresent(select_element), "do not see the dropdown")
        self.util.waitForElementToBeVisible(select_element)
        option_to_be_selected = self.util.getTextFromXpathString(select_element + "/option[" + str(option_number) + "]")
        self.util.selectFromDropdownUntilSelected(select_element, option_to_be_selected)

    @log_time
    def verifyObjectValues(self, grcobject_elements, grcobject_values, module=""):
        self.closeOtherWindows()
        time.sleep(2) 
        for key, xpath in grcobject_elements.iteritems(): 
            
            if key in ["description", "notes"]:                 
                frame_element = elem.object_iFrame.replace("FRAME_NAME", key)
                self.util.waitForElementToBePresent(frame_element)
                self.util.waitForElementToBeVisible(frame_element)
                new_value = self.util.getTextFromFrame(frame_element)
                time.sleep(25)                
                self.assertTrue(new_value == grcobject_values[key], "Verification ERROR: the value of " + key + " should be " + grcobject_values[key] + " but it is " + new_value)
            if key in ["network_zone", "kind", "fraud_related", "key_control", "means", "type"]:
                dropdown_element = elem.object_dropdown.replace("NAME", key)
                dropdown_element_selected_option = elem.object_dropdown_selected_option.replace("NAME", key)
                self.util.waitForElementToBePresent(dropdown_element)                
                self.assertTrue(self.util.isElementPresent(dropdown_element), "ERROR inside verifyObjectValues(): can't see dropdown element " + key)
                self.util.waitForElementToBePresent(dropdown_element_selected_option)
                self.assertTrue(self.util.isElementPresent(dropdown_element_selected_option), "ERROR inside verifyObjectValues(): can't see dropdown selected option for " + key)
                new_value = self.util.getTextFromXpathString(dropdown_element_selected_option)
                # print "verifyObjectValues: grcobject_values[key] : " + str(grcobject_values[key])
                # print "verifyObjectValues:             new_value : " + str(new_value)
                
                # work-around: 'if' is needed because the previous tester unnecessarily complicate the codes
                # self.assertTrue(new_value == grcobject_values[key], "Verification ERROR: for grcobject_values[key]")
            
            if key in ["title", "owner", "code", "url", "organization", "scope"]:
                    
                    # work-around; CORE-1245
                    if key=="owner":
                        xpath = '//div[@data-id="owner_hidden"]//span[contains(@class,"person-tooltip-trigger")]'
                                      
                    self.util.waitForElementToBePresent(xpath)
                    self.util.waitForElementToBeVisible(xpath)
                    self.assertTrue(self.util.isElementPresent(xpath), "ERROR inside verifyObjectValues(): can't see element " + key)
                    
                    if key=="owner":    
                        new_value = self.util.getTextFromXpathString(xpath) # work for owner
                    else:
                        new_value = self.util.getAnyAttribute(xpath, "value")
                        
                    if not new_value:
                        self.assertTrue(False, "Verification ERROR: could not retrieve the value of " + xpath)
                    # print "new_value="+new_value
                    else:
                        self.assertTrue(new_value == grcobject_values[key], "Verification ERROR: the value of " + key + " should be " + grcobject_values[key] + " but it is " + new_value)

            print "Verification OK: the value of " + key + " is " + str(grcobject_values[key]) + ", as expected." 

    @log_time
    # Delete object with title matching pattern, or default "auto" is matched
    # if you don't specify in which object to be deleted, e.g., Contract, Standard, etc.
    def deleteObjectsFromHLSMatching(self, grcObject="", check=False):
        items_lk = '//ul[@class="sub-level cms_controllers_infinite_scroll in"]/li[INDEX]//div[@class="lhs-main-title"]/span'
       
        if check == False:
            # uncheck box if it is checked
            self.uncheckMyWorkBox()
                                   
        self.ensureLHNSectionExpanded(grcObject)  
        if "localhost" in config.url:
            time.sleep(15)
        else:
            time.sleep(60)    
                        
        count = self.countOfAnyObjectLHS(grcObject)

        for index in range(0, count):                     
            xpath = str(items_lk).replace("INDEX", "1")  # always first row
            self.util.waitForElementToBePresent(xpath)
            time.sleep(2)
            mystr = self.util.getTextFromXpathString(xpath)
            print "index: " + str(index) + " " + mystr
            
            # print "Troubleshooting => index: " + str(index) + ": " + mystr

            self.util.clickOn(xpath)
            # Wait for the Edit button in the object detail page info section, then click on it
            self.clickInfoPageEditLink()
            self.deleteObject()
            count = count - 1;
            
            if count != 0:
                time.sleep(60)  # guarantee that result is returned
                
    @log_time
    # This function click on the Delete button after Edit window is already popped up
    def deleteObject(self):
        print "Start deleting object."
        time.sleep(3)
        self.util.waitForElementToBePresent(elem.modal_window_delete_button)
        self.assertTrue(self.util.isElementPresent(elem.modal_window_delete_button), "ERROR: Could not delete object: Can not see the Delete button")
        result = self.util.clickOn(elem.modal_window_delete_button)
        self.assertTrue(result, "ERROR in deleteObject(): could not click on Delete button " + elem.modal_window_delete_button)
        self.waitForDeleteConfirmToAppear()
        result = self.util.clickOn(elem.modal_window_confirm_delete_button)
        self.assertTrue(result, "ERROR inside deleteObject(): could not click Confirm Delete button " + elem.modal_window_confirm_delete_button)
        self.waitForDeletionToComplete()
        print "Object deleted successfully."

    @log_time
    def waitForDeleteConfirmToAppear(self):
        status = self.util.waitForElementToBePresent(elem.modal_window_confirm_delete_button)
        self.assertTrue(status, "ERROR inside deleteObject(): Could not delete object: Could not find " + elem.modal_window_confirm_delete_button)

    @log_time
    def waitForDeletionToComplete(self):
        time.sleep(3)
        status = self.util.waitForElementNotToBePresent(elem.modal_window)
        self.assertTrue(status, "ERROR inside deleteObject(): Could not delete object: Modal window " + elem.modal_window + " is still present")

    @log_time
    def  getObjectIdFromHref(self, link):
        href = self.util.getAnyAttribute(link, "href")
        id = href.split("/")[-1]
        return id

    @log_time
    # Select a passed-in object category, e.g., "Standard", then select the first entry and map to it after the filtering by search
    # Default to select "my object only" radio button
    def mapAObjectLHN(self, object, title="", my_object_only=True):
        
        # adjustment is need
        if object == "Data":
            object = "DataAsset"
        elif object == "Group":
            object = "OrgGroup"
        
        # if nothing is entered in the search box then it's index 2 otherwise it's index 1
        if title == "":
            xp_1st_entry_LHS = str('//ul[@class="top-level"]//li[contains(@data-model-name,"OBJECT")]/div/ul[contains(@class, "sub-level")]/li[2]/a[contains(@class, "show-extended")]//span').replace("OBJECT", object)
            
        else:
            xp_1st_entry_LHS = str('//ul[@class="top-level"]//li[contains(@data-model-name,"OBJECT")]/div/ul[contains(@class, "sub-level")]/li[1]/a[contains(@class, "show-extended")]//span').replace("OBJECT", object)
            self.searchFor(title)
        
        print "Start mapping LHN " + object
        self.closeOtherWindows()
        
        self.ensureLHNSectionExpanded(object)
        self.clearSearchBoxOnLHS()
       
        if object == "Person":
          self.uncheckMyWorkBox()         
        else:
          self.checkMyWorkBox()        
        
        time.sleep(40)
        self.waitUntilLHNCountDisplay(object)
        # assumption here is that you always have at least 2 people in the database
        # first_link_of_the_section_link = xp_1st_entry_LHS

        
        self.assertTrue(self.util.waitForElementToBePresent(xp_1st_entry_LHS), "ERROR inside mapAObjectLHN(): cannot see the first " + object + " in LHN")
  
        if "local" in config.url and object == "Person":
            second_link_of_the_section_link = '//ul[@class="top-level"]//li[contains(@data-model-name,"Person")]/div/ul[contains(@class, "sub-level")]/li[2]'
            self.assertTrue(self.util.waitForElementToBePresent(second_link_of_the_section_link), "ERROR inside mapAObjectLHN(): cannot see the first " + object + " in LHN")
            self.util.waitForElementToBePresent(second_link_of_the_section_link)
            idOfTheObject = self.util.getTextFromXpathString(second_link_of_the_section_link)
            self.util.hoverOverAndWaitFor(second_link_of_the_section_link, elem.map_to_this_object_link)
        else:
            self.util.waitForElementToBePresent(xp_1st_entry_LHS)
            idOfTheObject = self.util.getTextFromXpathString(xp_1st_entry_LHS)  # work for regulation, 
            self.util.hoverOverAndWaitFor(xp_1st_entry_LHS, elem.map_to_this_object_link)

        self.assertTrue(self.util.waitForElementToBePresent(elem.map_to_this_object_link), "no Map to link")
        result = self.util.clickOn(elem.map_to_this_object_link)
        self.assertTrue(result, "ERROR in mapAObjectLHN(): could not click on Map to link for " + object)        
        
        if "program" in str(title).lower():
            self.verifyObjectIsMapped(object, idOfTheObject, True)
        else:
            self.verifyObjectIsMapped(object, idOfTheObject)
        
    @log_time
    # Select a passed-in object category, e.g., "Standard", then select the first entry and map to it after the filtering by search
    def unmapAObjectFromWidget(self, object, isProgram=False):
        print "Start un-mapping LHN " + object
        objectLowercase = str(object).lower()
        
        if objectLowercase == "data":
            objectLowercase = "data_asset"
        if objectLowercase == "group":
            objectLowercase = "org_group"    
        
        if object == "Person":
          self.uncheckMyWorkBox()
        else:
          self.checkMyWorkBox()
        
        # make sure you select the widget first before you can unmap
        # but if the widget is already open then do have to click on it
        xpath = '//a[@href="#OBJECT_widget"]/div'
        tab = str(xpath).replace("OBJECT", objectLowercase)
        self.util.clickOn(tab)
        time.sleep(10)  # takes time to load
        countBefore = self.countOfAnyObjectInWidget(objectLowercase)
        
        open_mapping_modal_window_link = elem.section_widget_join_object_link.replace("OBJECT", object)

        if objectLowercase == "person" and isProgram == True:
            # First row is owner and you can't unmap owner.  Program needs to have at least one owner
            self.expandNthItemInWidget(objectLowercase, 1)
        else:
            self.expandNthItemInWidget(objectLowercase)      
            
        # CORE-1284 + SIGN to map is in the bottom, in table row 
        self.showLHMenu(False) #collapse the LHN
            
        self.clickOnUnmapButton()
        time.sleep(10)  # takes long time when more objects are unmapped
        # give it enough time
        countAfter = countBefore - 1

        theCount = self.countOfAnyObjectInWidget(objectLowercase)        
        # need this function because 
        comparison = self.waitUntilAEqualsB(theCount, countAfter)
        
        if comparison == True:
            print "Object " + object + " is un-mapped successfully."
            return True
        else:
            return False

    @log_time
    def waitForWidgetListToLoad(self, list_xpath):
        self.util.waitForElementToBePresent(list_xpath)
        self.util.waitForElementToBePresent(list_xpath + elem.list_loaded_suffix)

    @log_time
    def navigateToWidget(self, object):
        # click on the inner nav and wait for the corresponding widget section to become active
        inner_nav_object_link = elem.inner_nav_object_link.replace("OBJECT", object.lower())
        self.assertTrue(self.util.waitForElementToBePresent(inner_nav_object_link), "ERROR mapAObjectWidget XXX(): can't see inner_nav_object_link for " + object)
        self.util.waitForElementToBeVisible(inner_nav_object_link)
        # inject event handler before clicking
        self.util.driver.execute_script('$("body").append("{}");'.format(self.loaded_script))
        result = self.util.clickOn(inner_nav_object_link)
        self.assertTrue(result, "ERROR in mapAObjectWidget(): could not click " + inner_nav_object_link + " for object " + object)
        widget_tree = elem.section_widget_tree.replace("OBJECT", object.lower())
        self.waitForWidgetListToLoad(widget_tree)

    def clickMapLink(self, object):
        map_link = elem.section_widget_join_object_link.replace("OBJECT", object)
        self.util.clickOn(map_link)
    
    # Example: Map Contract link from Contract Tab widget;  object is singular and Capitalized first letter   
    def isMapLinkPresent(self, object):
        map_link = elem.section_widget_join_object_link.replace("OBJECT", object)
        return self.util.isElementPresent(map_link)



    def navigateToMappingWindowForObject(self, object, expandables=(), is_program=False):
        """Set expandables to the list of object types whose footer expands when you hover over the "add" button.
        """
        self.authorizeGAPI(1)
        self.assertTrue(self.util.waitForElementToBePresent(elem.add_widget_plus_sign), "ERROR inside mapAObjectWidget(): can't see add widget + plus sign")

        # Person tab is pre-defined for program, just select person tab
        if object == "Person" and is_program == True:           
            person_tab = '//a[@href="#person_widget"]/div'
            self.util.clickOn(person_tab)
            open_mapping_modal_window_link = elem.section_widget_join_object_link.replace("OBJECT", object)
            time.sleep(1)            
        else:              
            self.util.clickOn(elem.add_widget_plus_sign)
            obj = str(object).lower()
            expanded_widget = '//div[contains(@class, "dropdown-menu")]/div/a[@href="#OBJECT_widget"]/div/i'
            expanded_widget = expanded_widget.replace('OBJECT', obj)
            self.util.clickOn(expanded_widget)
    
            # click on the object link in the widget to  search for other objects modal
            if object in expandables:
                open_mapping_modal_window_link = elem.section_widget_expanded_join_link1.replace("OBJECT", object.lower())
            else: 
                open_mapping_modal_window_link = elem.section_widget_join_object_link.replace("OBJECT", object)
    
        # if footer is expandable, hover first, then click on submenu
        if object in expandables:
        # hover before clicking in case expander must act
            self.util.hoverOver(open_mapping_modal_window_link)
            
            if object == "Section":
                expanded_button = elem.section_widget_expanded_sectionObject_link3.replace("OBJECT", object)
            else:
                expanded_button = elem.section_widget_expanded_join_link2.replace("OBJECT", object)
                self.util.waitForElementToBeVisible(expanded_button)
            open_map_modal_button = expanded_button
        else:
            if "Data_Asset" == object:
                object = "DataAsset"
                open_mapping_modal_window_link = elem.section_widget_join_object_link.replace("OBJECT", object)               
            if "Org_Group" == object:
                object = "OrgGroup"
                open_mapping_modal_window_link = elem.section_widget_join_object_link.replace("OBJECT", object)                         
            open_map_modal_button = open_mapping_modal_window_link
            
        # inject event modal list catcher
        self.util.driver.execute_script('$("body").append("{}");'.format(self.map_loaded_script))
        time.sleep(10)
        result = self.util.clickOn(open_map_modal_button)
        time.sleep(5)
        self.assertTrue(result, "ERROR in mapAObjectWidget(): could not click on " + open_map_modal_button + " for object " + object)
        # self.waitForFullMapModal(object) #commented out by Ukyo

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
    # map first object from the modal window
    def mapFirstObject(self, object, objectName="", is_program=False, email=config.username, howManyToMap=1, bypass=False):
        time.sleep(5)
        search_by_owner = "search-by-owner"
        match_term = "search"
        auto_complete_name = '//ul[contains(@class, "ui-autocomplete")]/li[contains(@class, "ui-menu-item")]/a[contains(., "TEXT")]'      
        search_bt = '//a[@id="modalSearchButton"]'
        search_bt_id = 'modalSearchButton'
        
        # Ukyo work around
        elem.mapping_modal_selector_list_first_object = '//ul[@class="tree-structure new-tree multitype-tree"]/li[1]'
        
        self.util.waitForElementToBePresent(elem.mapping_modal_selector_list_first_object)
        # self.assertTrue(self.util.waitForElementToBePresent(elem.mapping_modal_selector_list_first_object), "ERROR inside mapAObjectWidget(): cannot see first object in the selector")

        # Enter email in textbox and search
        if object != "Person":
            owner_email = email
            self.util.inputTextIntoField(objectName, match_term, "id")
                       
            if bypass==False:
                #CORE-289
                self.util.inputTextIntoField(owner_email, search_by_owner, "id")           
                matching_email_selector = auto_complete_name.replace("TEXT", owner_email)               
                self.util.waitForElementToBeVisible(matching_email_selector)
                self.util.hoverOver(search_by_owner, "id")  # object_owner = "//div[@class='modal-body']//div[@class='row-fluid']//label[contains(text(), 'Owner')]/following-sibling::input[1]"
                self.util.clickOn(matching_email_selector)
            
            self.util.clickOn('//a[@data-object-singular="Person"]/i[@class="grcicon-add-black"]/..')  # to out-focus of textbox  
            self.util.clickOn('//a[@data-dismiss="modal" and @class="btn btn-danger btn-mini pull-right"]')        
            self.util.clickOn(search_bt)
            self.util.clickOnId(search_bt_id)
            time.sleep(30)  # wait for results to come back

        # for program/person mapping, extract email for later
        if is_program and object == "Person":
            # emailOfPersonToBeMapped = self.util.getTextFromXpathString(elem.mapping_modal_selector_list_first_object_email)
            emailXpath = '//ul[@class="tree-structure new-tree multitype-tree"]/li[2]//span[@class="url-link"]'  # 2nd row email
            emailOfPersonToBeMapped = self.util.getTextFromXpathString(emailXpath)
            print "the first Person's email is " + emailOfPersonToBeMapped
        else:  # otherwise, get ID
            # idOfTheObjectToBeMapped = self.util.getAnyAttribute(elem.mapping_modal_selector_list_first_object, "data-id")
            idOfTheObjectToBeMapped = self.util.getTextFromXpathString('//ul[@class="tree-structure new-tree multitype-tree"]/li[1]//div[@class="tree-title-area"]')
            
            if object == "Person":
                # hacked version of splitting out name and email
                length = len(idOfTheObjectToBeMapped)
                space = idOfTheObjectToBeMapped.index(" ") + 1
                idOfTheObjectToBeMapped = idOfTheObjectToBeMapped[space:length]
            
            print "the first " + object + " id is " + idOfTheObjectToBeMapped
        
        if object == self.object_type:
            # if same object type, make sure id != this object's id
            # first_acceptable_map_link = elem.mapping_modal_selector_first_nonself_object_link.replace("OBJECTID", self.currentObjectId()) #commented out by U
            
            # select second row since first row is the object itself
            if objectName == idOfTheObjectToBeMapped:
                first_acceptable_map_link = '//ul[@class="tree-structure new-tree multitype-tree"]/li[2]//input[@type="checkbox"]'
            else:
                first_acceptable_map_link = '//ul[@class="tree-structure new-tree multitype-tree"]/li[1]//input[@type="checkbox"]'
                                
        else:  # otherwise, just grab first
            if is_program and object == "Person":
                first_acceptable_map_link = '//ul[@class="tree-structure new-tree multitype-tree"]/li[2]//input[@type="checkbox"]'
            else:
                while howManyToMap > 0:  # in case you want to map first more than 1 objects
                    first_acceptable_map_link = '//ul[@class="tree-structure new-tree multitype-tree"]/li[' + str(howManyToMap) + ']//input[@type="checkbox"]'                   
                    self.util.waitForElementToBePresent(first_acceptable_map_link)
                    self.util.clickOn(first_acceptable_map_link)
                    howManyToMap = howManyToMap - 1
        
        self.util.waitForElementToBePresent(elem.mapping_modal_window_map_button)
        self.assertTrue(self.util.isElementPresent(elem.mapping_modal_window_map_button), "no Map button")
        result = self.util.clickOn(elem.mapping_modal_window_map_button)
        self.assertTrue(result, "ERROR in mapAObjectWidget(): could not click on Map button for " + object)
        time.sleep(6)  # to be sure it vanish
        self.util.waitForElementNotToBePresent(elem.mapping_modal_window)
        
        # don't verify if it's more than 1 mapping
        if howManyToMap > 1:
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
        self.util.inputTextIntoField(person, elem.mapping_modal_input_textfiled)

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
    def mapAObjectWidget(self, object, objectName="", is_program=False, expandables=(), howManyToMap=1):
        self.closeOtherWindows()
        email = config.username
        
        self.navigateToMappingWindowForObject(object, expandables, is_program)
        
        # for Section, handles it differently because you have to create a section to map
        # fill in the form and hit Save
        if object == "Section":
            if "Policy" in objectName or "Regulation" in objectName or "Standard" in objectName:            
                
                titleSection = '//input[@id="section-title"]'
                saveButton = '//div[@class="confirm-buttons"]/a[@data-toggle="modal-submit"]'
    
                countBefore = self.countOfAnyObjectInWidget("section")
                countBefore = countBefore + 1
    
                title = "Section_" + str(self.getTimeId())
                self.util.inputTextIntoField(title, titleSection)
                self.util.clickOn(saveButton)
                time.sleep(20)
                countAfter = self.countOfAnyObjectInWidget("section")
                 
                self.assertEqual(countBefore, countAfter, "Count before+1 = after? fails.")
                print "mapped Section successfully."
            else:
                # Map_Section widget appears on others, e.g., product
                # troubleshoot, send in blank ""
                time.sleep(5)
                self.mapFirstObject(object, "", is_program=is_program)
        else:        
            # select the first object from the search results and map it
            # troubleshoot, send in blank ""
            time.sleep(5)
            self.mapFirstObject(object, "", is_program, email, howManyToMap)
        
    @log_time
    # Unmap the first row.
    # object : singular form, lower case, e.g., data_access, org_group, 
    def unmapAnObjectFromWidget(self, object, is_program=False, expandables=()):
        # singular form, lower-case,
        # special case: data_access, org_group
        first_row = '//li[@class="tree-item governance cms_controllers_tree_view_node" and @data-object-type="OBJECT"]'
        
        self.closeOtherWindows()
        self.util.navigateToWidget(object)
        # select the first row from widget
        

    @log_time
    def verifyObjectIsMapped(self, object, objIdentifier, is_program=False, mapped_email=None):
        if is_program and object == "Person":
            objectEmail = objIdentifier
        else:
            objectId = objIdentifier
            
        # adjustment
        if object == "DataAsset":
            object = "data_asset"
        elif object == "OrgGroup":
            object = "org_group"
            

        if object.lower() == "group":
            object = "org_group"
        
        if is_program and object == "Person":
            mapped_object = elem.mapped_person_program_email.replace("EMAIL", objectEmail)
            print "the mapped object is " + mapped_object
            # check whether the person appears in the list at all
            self.assertTrue(self.util.waitForElementToBePresent(mapped_object), "ERROR inside verifyObjectIsMapped(): Person does not appear in Program list")
        else:
            mapped_object1 = elem.mapped_object.replace("OBJECT", object.lower())
            
            if object=="Person":
                mapped_object1 = elem.mapped_object_person.replace("OBJECT", object.lower())
            
            self.util.waitForElementToBePresent(mapped_object1)
            mapped_object = self.util.getTextFromXpathString(mapped_object1)
            print "the mapped object is :" + mapped_object
            print "objIdentifier is     :" + objIdentifier
            time.sleep(2)
            
            if object != "Person":
                self.assertEqual(objIdentifier, mapped_object, "Object mapping failure verification due to name not matching.")
            else:
                text = str(mapped_object)
                length = len(text)
                
                try:  # check to see if there is a space in between
                    space_index = text.index(" ")  # example:   Example User                   
                except:  # testrecip@gmail.com
                    self.assertEqual(objIdentifier, mapped_object, "Object mapping failure verification due to name not matching.")
                    print "Object " + object + " is mapped successfully"
                    return mapped_object
                
                partial_text = text[space_index:length]                
                partial_text = str(partial_text).strip()                 
                text_full = str(objIdentifier).strip()
                 
                if partial_text in text_full:
                    self.assertTrue(True, "Fail verifying personal info like email or name.")
                else:
                    self.assertTrue(False, "Fail verifying personal info like email or name.")
                                   
        print "Object " + object + " is mapped successfully"
        return mapped_object

    @log_time
    # case-insensitive and singular
    def navigateToInnerNavSection(self, object, is_program=False):
#         inner_nav_object_link = elem.inner_nav_object_link.replace("OBJECT", object.lower())
#         self.assertTrue(self.util.waitForElementToBePresent(inner_nav_object_link),"ERROR mapAObjectWidget XXX(): can't see inner_nav_object_link for "+object)
#         self.util.waitForElementToBeVisible(inner_nav_object_link)
# 
#         result=self.util.clickOn(inner_nav_object_link)
#         self.assertTrue(result,"ERROR in mapAObjectWidget(): could not click "+inner_nav_object_link + " for object "+object)
#         active_section = elem.section_active.replace("SECTION", object.lower())
#         self.assertTrue(self.util.waitForElementToBePresent(active_section), "ERROR inside mapAObjectWidget(): no active section for "+ object)

        self.assertTrue(self.util.waitForElementToBePresent(elem.add_widget_plus_sign), "ERROR inside mapAObjectWidget(): can't see add widget + plus sign")

        # Person tab is pre-defined for program, just select person tab
        if object == "Person" and is_program == True:           
            person_tab = '//a[@href="#person_widget"]/div'
            self.util.clickOn(person_tab)
            open_mapping_modal_window_link = elem.section_widget_join_object_link.replace("OBJECT", object)                      
        else:              
            self.util.clickOn(elem.add_widget_plus_sign)
            obj = str(object).lower()
            expanded_widget = '//div[@class="dropdown-menu"]/div/a[@href="#OBJECT_widget"]/div/i'
            expanded_widget = expanded_widget.replace('OBJECT', obj)
            self.util.clickOn(expanded_widget)
        time.sleep(3) 
        
    @log_time
    def createAudit(self, program_name):
        # verify modal window
        self.util.waitForElementToBeVisible(elem.modal_window)
        self.assertTrue(self.util.isElementPresent(elem.modal_window), "can't see modal dialog window for create new object")

        # verify audit title textbox
        self.util.waitForElementToBeVisible(elem.object_title)
        self.assertTrue(self.util.isElementPresent(elem.object_title), "can't access the input textfield")

        # set a unique title
        audit_auto_populated_title = program_name + " Audit" + self.getTimeId()
        self.util.inputTextIntoField(audit_auto_populated_title, elem.object_title)
        self.util.clickOn(elem.audit_modal_autogenerate_checkbox)

        # calculate the dates - Fill in start date (current date), Planned End Date (+2months), Planned Report date from(+1month from start), Planned report date to (Planned end date + 1 week)
        start_date = date.today()
        end_date = self.add_months(start_date, 2)
          
        report_start_date = self.add_months(datetime.date.today(), 1)
        report_end_date = report_start_date + datetime.timedelta(days=7)
  
        # populate the dates
        self.enterDateWithCalendar(elem.audit_modal_start_date_input, start_date, "start date")
        self.enterDateWithCalendar(elem.audit_modal_end_date_input, end_date, "end date")
        self.enterDateWithCalendar(elem.audit_modal_report_start_date_input, report_start_date, "reporting start date")
        self.enterDateWithCalendar(elem.audit_modal_report_end_date_input, report_end_date, "reporting end date")
         
        # click on Advanced link
        frame_element = elem.object_iFrame.replace("FRAME_NAME", "description")
         
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
        
        # verifying the auto-populated Audit Lead email
        self.util.waitForElementToBePresent(elem.audit_modal_audit_lead_input_field)
        self.assertTrue(self.util.isElementPresent(elem.audit_modal_audit_lead_input_field), "can't see the Audit Lead input field")
        audit_auto_populated_audit_lead = self.util.getAnyAttribute(elem.audit_modal_audit_lead_input_field, "value")
        self.assertTrue(self.current_user_email()  in audit_auto_populated_audit_lead, "not correct Audit Lead value")
        
        self.saveNewObjectAndWait()
        return audit_auto_populated_title

    @log_time
    def expandCollapseRequest(self, request_title_text):
        expand_link = str(elem.audit_pbc_request_expand_collapse_button2).replace("TITLE", request_title_text) 
        expanded_section = str(elem.audit_pbc_request_expanded).replace("TITLE", request_title_text) 
        self.util.waitForElementToBePresent(expand_link)
        self.assertTrue(self.util.isElementPresent(expand_link), "can't see the expand link") 
        self.util.hoverOver(expand_link)
        self.util.clickOn(expand_link)
        self.util.waitForElementToBePresent(expanded_section)
        if self.util.isElementPresent(expanded_section) == False:
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
        frame_element = elem.object_iFrame.replace("FRAME_NAME", "description")
        
        # type the description 
        self.util.waitForElementToBePresent(frame_element)
        self.assertTrue(self.util.isElementPresent(frame_element), "can't see the description frame")
        self.util.typeIntoFrame(description, frame_element)
        self.saveNewObjectAndWait()

    def convertDateIntoFormat(self, date):
        correct_format_date = str(date.month) + "/" + str(date.day) + "/" + str(date.year) 
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

    def add_months(self, sourcedate, months):
        month = sourcedate.month - 1 + months
        year = sourcedate.year + month / 12
        month = month % 12 + 1
        day = min(sourcedate.day, calendar.monthrange(year, month)[1])
        return datetime.date(year, month, day)

    @log_time
    def getTheIdOfTheLastCreated(self, newly_created_object_type):
        object_element = elem.data_object_element.replace("DATA_OBJECT", newly_created_object_type)
        self.util.waitForElementToBePresent(object_element)
        self.assertTrue(self.util.isElementPresent(object_element), "no " + newly_created_object_type + " have been created")
        overall_number_of_objects = str(self.util.getNumberOfOccurences(object_element))
        print "  " + str(overall_number_of_objects) + " " + newly_created_object_type + " have been created"
        last_created_object_element = elem.data_object_element_with_index.replace("DATA_OBJECT", newly_created_object_type).replace("INDEX", overall_number_of_objects)
        self.util.waitForElementToBePresent(last_created_object_element)
        self.assertTrue(self.util.isElementPresent(last_created_object_element), "cannot see the last created object")
        print last_created_object_element
        last_created_object_element_id = self.util.getAnyAttribute(last_created_object_element, "data-object-id")
        print last_created_object_element_id
        return last_created_object_element_id
    
    def getTheIdOfTheLastCreatedObjective(self, link):
       
        # overall_number_of_objectives = str(self.util.getNumberOfOccurences(elem.objective_elemet_in_the_inner_tree))
        # print str(overall_number_of_objectives) + " objectives have been created so far"
        # last_created_object_element = elem.objective_elemet_in_the_inner_tree_with_index.replace("INDEX",overall_number_of_objectives )
        print link
        last_created_object_element_id = self.util.getAnyAttribute(link, "data-object-id")
        print last_created_object_element_id
        return last_created_object_element_id

    @log_time
    # To show or to hide away menu in the left hand navigation
    def showLHMenu(self, showIt=True):
        
        show = '//button[contains(@class, "lhn-trigger pull-left active")]'
        no_show = '//button[contains(@class, "lhn-trigger pull-left")]'
        
        if showIt==True:
            if not (self.util.isElementPresent(show)):
                self.util.clickOn(no_show) #toggle it to show
        else:
            if (self.util.isElementPresent(show)):
                self.util.clickOn(show) #toggle it to not show

    @log_time
    def isLHMenuOpen(self):
        show = '//button[contains(@class, "lhn-trigger pull-left active")]'
        return self.util.isElementPresent(show)

    @log_time #returns its label or text
    def getGovernanceLabel(self):
        label = self.util.getTextFromCSSString(elem.governance_accordion_css)
        self.util.clickOnCSS(elem.governance_accordion_css)
        return label
    def getPeopleLabel(self):
        label = self.util.getTextFromCSSString(elem.people_accordion_css)
        self.util.clickOnCSS(elem.people_accordion_css)
        return label      
    def getBusiness(self):
        label = self.util.getTextFromCSSString(elem.business_accordion_css)
        self.util.clickOnCSS(elem.business_accordion_css)
        return label
    
    # click on accordion
    def clickGovernanceLabel(self):
        return self.util.clickOnCSS(elem.governance_accordion_css)

    def clickPeopleLabel(self):
        return self.util.clickOnCSS(elem.people_accordion_css)
     
    def clickBusiness(self):
        return self.util.clickOnCSS(elem.business_accordion_css)  
    
    # check if accordion is expanded
    def isPeopleExpanded(self):
        expanded = '[class="entities accordion-group"] [style="display: block;"]'       
        return self.util.isElementPresent(expanded)
    def isBusinessExpanded(self):
        expanded = '[class="business accordion-group"] [style="display: block;"]'       
        return self.util.isElementPresent(expanded)
    def isGovernanceExpanded(self):
        expanded = '[class="governance accordion-group"] [style="display: block;"]'       
        return self.util.isElementPresent(expanded)

    # enable=False means collapse it
    def expandPeople(self, enable=True):
        if enable==True:
            if self.isPeopleExpanded==False:
                self.util.clickOnCSS(elem.people_accordion_css)
        else:
            if self.isPeopleExpanded==True:
                self.util.clickOnCSS(elem.people_accordion_css)
    def expandGovernance(self, enable=True):
        if enable==True:
            if self.isGovernanceExpanded==False:
                self.util.clickOnCSS(elem.governance_accordion_css)
        else:
            if self.isGovernanceExpanded==True:
                self.util.clickOnCSS(elem.governance_accordion_css)
    def expandBusiness(self, enable=True):
        if enable==True:
            if self.isBusinessExpanded==False:
                self.util.clickOnCSS(elem.business_accordion_css)
        else:
            if self.isBusinessExpanded==True:
                self.util.clickOnCSS(elem.business_accordion_css)

    @log_time
    def checkMyWorkBox(self):
        """ensures "My Work" box is checked, regardless of current state"""
        self.util.waitForElementToBePresent("//div")
        self.util.waitForElementToBePresent(elem.my_work_checkbox)
        my_objects_tab = self.util.isElementPresent((elem.my_work_checkbox))
        if my_objects_tab:
            self.util.clickOn(elem.my_work_checkbox)

    def isMyObjectsOnlyChecked(self):
        return self.util.waitForElementToBePresent(elem.my_work_checkbox_selected)
    
    def isAllObjectsChecked(self):
        return self.util.waitForElementToBePresent(elem.everyone_work_checkbox_selected)

    @log_time
    # Select "All objects" is equivalent to uncheck my work box
    def uncheckMyWorkBox(self):
        """ensures "My Work" box is UNchecked, regardless of current state"""
        selected = self.util.isElementPresent(elem.everyone_work_checkbox_selected)

        if not selected:
            self.util.clickOn(elem.everyone_work_checkbox)
            time.sleep(5)
        

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
    def scheduleMeeting(self, title, date, start_time, end_time):
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
        
        dates = self.util.getTextFromXpathString('//li[@data-object-type="meeting"]//div[@class="tree-description short"]')
        dates = dates.strip()  
        # Example dates string:
        # 'Starts at: 01/25/2014 03:00:00 PM\nEnds at: 01/25/2014 04:00:00 PM'
        
        date1 = dates.split("\n")[0]  # 'Starts at: 01/25/2014 03:00:00 PM'
        date2 = dates.split("\n")[1]  # 'Ends at: 01/25/2014 04:00:00 PM'
        meeting_date = date1.split(" ")[2]  # '01/25/2014'

        meeting_start_time = date1.split(" ")[3] + " " + date1.split(" ")[4]  # '03:00:00 PM'
        meeting_end_time = date2.split(" ")[3] + " " + date2.split(" ")[4]  # '04:00:00 PM'

        self.assertTrue(meeting_date == data, "Meeting dates do NOT match; expected meeting date:" + data + ", actual meeting date:" + meeting_date)
        self.assertTrue(meeting_start_time == start_time, "Meeting start times do NOT match; expected meeting start time:" + start_time + ", actual meeting start time:" + meeting_start_time)
        self.assertTrue(meeting_end_time == end_time, "Meeting end times do NOT match; expected meeting end time:" + end_time + ", actual meeting end time:" + meeting_end_time)

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
    # Create a new person object from the LHN
    def createPeopleLHN(self, grcObject, save=True):
        self.util.waitForElementToBePresent(elem.new_person_name)
        self.util.inputTextIntoField(grcObject.people_elements.get("name"), elem.new_person_name)
        self.util.inputTextIntoField(grcObject.people_elements.get("email"), elem.new_person_email)
        self.util.inputTextIntoField(grcObject.people_elements.get("company"), elem.new_person_company)
        
        # default to save, unless you want to test the Cancel button
        if save == True: 
            self.util.clickOn(elem.modal_window_save_button)
        else:
            self.util.clickOn(elem.modal_window_cancel_button)

    @log_time
    # Create a new person object from the LHN
    def createPersonLHN(self, name, email, company, save=True, enabled=True):
        print ""
        print "Start creating person : " + name
        
        enable_user_false = '//input[@id="person_is_enabled" and @value="false"]'
        enable_user_true = '//input[@id="person_is_enabled" and @value="true"]'
        
        self.openCreateNewObjectWindowFromLhn("Person") 
        
        self.util.waitForElementToBePresent(elem.new_person_name)
        self.util.inputTextIntoField(name, elem.new_person_name)
        self.util.inputTextIntoField(email, elem.new_person_email)
        self.util.inputTextIntoField(company, elem.new_person_company)
        
        if enabled == True:
            if self.util.isElementPresent(enable_user_false):
                self.util.clickOn(enable_user_false)
                time.sleep(2)                
            self.assertTrue(self.util.isElementPresent(enable_user_true))
        else:
            if self.util.isElementPresent(enable_user_true):
                self.util.clickOn(enable_user_true)
                time.sleep(2)                
            self.assertTrue(self.util.isElementPresent(enable_user_false))
                    
        # default to save, unless you want to test the Cancel button
        if save == True: 
            self.util.clickOn(elem.modal_window_save_button)
        else:
            self.util.clickOn(elem.modal_window_cancel_button)

    @log_time
    # + Section button is already visible and displayed         
    def createSectionFromInnerNavLink(self, theName="mySectionX"):
        
        time.sleep(1)
        self.util.waitForElementToBePresent(elem.section_add_link_from_inner_nav, 20)
        
        for x in range(1, 10):
            try:
                self.util.hoverOver(elem.section_add_link_from_inner_nav)      
                self.util.clickOn(elem.section_create_link_from_inner_nav)
                time.sleep(1)
                
                # is modal window comes up, it's good.  Let's exist
                if (self.util.isElementPresent(elem.modal_window)):
                    break               
            except:
                print "Try to click on section-create link ..."
                pass
            
        
        self.populateNewObjectData(theName)
        # self.populateNewObjectData(ggrcObject.section_elements.get("title"), ggrcObject.section_elements.get("owner"))
        self.saveNewObjectAndWait()

    @log_time
    # From Inner Nav panel, with Section already created, just click on a section to do objective mapping
    def mapObjectToSectionFromInnerNav(self, theName):
        map_bt = '//div[@class="confirm-buttons"]//a'
        
        # expand the section item
        self.util.clickOn(elem.first_item_section_link_from_nav)
        self.util.waitForElementToBePresent(elem.map_object_to_section_from_nav)
 
        for x in range(1, 10):
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
        
        for x in range(1, 10):
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

    # This is for, Program -> Regulation -> Section -> Object 
    # Singular: objectCategory = {Person, DataAsset}     
    def mapObjectFormFilling(self, objectCategory, searchTerm):
        
        # type_select = '//select[@automation="at_by_type_586385323_sel"]'
        # option = '//select[@automation="at_by_type_586385323_sel"]//option[@value="OBJECT"]'
        type_select = '//select[@class="input-block-level option-type-selector"]'
        match_term_search = '//input[@id="search"]'
        
        add_selected_bt = '//div[@class="confirm-buttons"]/a'
        search_bt = '//a[@class="btn pull-right modalSearchButton"]'
        firstRow_chkbx = '//ul[@class="tree-structure new-tree multitype-tree"]/li[1]//input[@type="checkbox"]'
        time.sleep(3)
        self.util.selectFromDropdownByValue(type_select, objectCategory)
        self.util.inputTextIntoField(searchTerm, match_term_search)

        self.util.clickOn(search_bt)
        
        if "local" in config.url:
            time.sleep(15)
        else:
            time.sleep(25)  # ensure data comes back
        self.util.waitForElementToBePresent(firstRow_chkbx)
        self.util.clickOn(firstRow_chkbx)
        time.sleep(1)
        self.util.clickOn(add_selected_bt)
        time.sleep(5)

        
        

    # Specify a category label, and title to search
    def _searchInMapObjectModalWindow(self, label, title):
        xpath = '//select[@class="input-block-level option-type-selector"]/'
        search_count_label = '//div[@class="search-title"]/div/div/h4'
        row = '//div[@class="selector-list cms_controllers_infinite_scroll"]//li[INDEX]//div[@class="tree-title-area"]/span'

        # click on the dropdown for category
        myXpath = xpath + '/option[@label=\"' + label + '\"]'
        self.util.waitForElementToBePresent(myXpath)
        self.util.clickOn('//div[@id="ajax-modal-javascript:--"]//select[@class="input-block-level option-type-selector"]')   
        self.util.clickOn(myXpath)  
        self.util.clickOn(myXpath)
        
        self.util.inputTextIntoField(title, '//input[@id="search"]')
        time.sleep(6)  # it auto completes and return matches
        
        count = self._countInsideParenthesis(self.util.getTextFromXpathString(search_count_label))
        
        for indx in range(1, count + 1):
            row = row.replace("INDEX", str(indx))
            text = self.util.getTextFromXpathString(row)
            
            if text == title:
                self.util.clickOn(row)


    # Specify a category label, and title to search
    def _searchTitleInTable(self, label, title):
        xpath = '//select[@class="input-block-level option-type-selector"]/'
        search_count_label = '//div[@class="search-title"]/div/div/h4'
        row = '//div[@class="selector-list cms_controllers_infinite_scroll"]//li[INDEX]//div[@class="tree-title-area"]/span'

        # click on the dropdown for category
        myXpath = xpath + '/option[@label=\"' + label + '\"]'
        self.util.waitForElementToBePresent(myXpath)
        self.util.clickOn('//div[@id="ajax-modal-javascript:--"]//select[@class="input-block-level option-type-selector"]')   
        self.util.clickOn(myXpath)  
        self.util.clickOn(myXpath)
        
        self.util.inputTextIntoField(title, '//input[@id="search"]')
        time.sleep(6)  # it auto completes and return matches
        
        count = self._countInsideParenthesis(self.util.getTextFromXpathString(search_count_label))
        
        for indx in range(1, count + 1):
            row = row.replace("INDEX", str(indx))
            text = self.util.getTextFromXpathString(row)
            
            if text == title:
                self.util.clickOn(row)


    @log_time
    # Unmap from object (third) level:  from this scheme, Program->Regulation->Section->Object
    def unMapObjectFromWidgetIn3rdLevel(self, title):
            self._searchObjectIn3rdLevelAndClickOnIt(title)
        
    @log_time
    # Return xpath of row for this item if found else return False
    def _searchObjectIn3rdLevelAndClickOnIt(self, title, withLink=False):

        # to find out how many rows
        # xpath_c = '//ul[@class="tree-structure new-tree cms_controllers_tree_view"]/../h6'
        xpath_c = '//div[@class="inner-tree"]/h6'
        raw_text = str(self.util.getTextFromXpathString(xpath_c))
        start = raw_text.index("(")
        end = raw_text.index(")")
        start = start + 1       
        count = raw_text[start:end]
        count = int(count) + 1  # because loop starts from index 1, not 0; therefore adjustment is neccessary 
        
        for row in range(1, count):
            if withLink == False:
                xp = '//ul[@class="tree-structure new-tree cms_controllers_tree_view"]/li[' + str(row) + ']//div[@class="span12"]/div/div'  # no_link
            else:
                xp = '//div[@class="inner-tree"]/ul/li[' + str(row) + ']//span[@class="person-tooltip-trigger"]'  # link

            atitle = self.util.getTextFromXpathString(xp)
            if atitle == title:
                if withLink == False:
                    self.util.clickOn(xp)
                else:
                    self.util.clickOn(xp + "/../../..")  # click on the same row but not on the link         
                
                time.sleep(5)
                return
                
    @log_time
    # Expand first tier, and then click on Unmap button
    def unMapObjectFromWidget(self, object_level=True):
        
        if object_level == False:
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
        if secondTier == True:
            self.clickOnUnmapLink()  # from second tier
            time.sleep(2)
        else:   
            self.util.waitForElementToBePresent(elem.unmap_button_from_3rd_level_object) 
            self.util.clickOn(elem.unmap_button_from_3rd_level_object)
            time.sleep(2)
        
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
    def expandNthItemInWidget(self, object, nth=1):

        #old
        if nth == 1:
            #xpath = '//section[@id="' + object + '_widget"]//li[1]//div[@class="row-fluid"]'
            xpath = '//li[@data-object-type="' + object + '"]//div[@class="select"]/div/div[@class="row-fluid"]/div[1]/div'
        elif nth > 1:
            xpath = '//li[@data-object-type="' + object + '"]//div[@class="select"]/div/div[@class="row-fluid"]/div[2]/div'      
        
        self.util.waitForElementToBePresent(xpath, 20)
        self.util.clickOn(xpath)
 
    @log_time
    # Assume you already call expandNthItemInWidget() to expand the row
    def clickViewProgram(self, object, nth):
        xpath = '//section[@id="' + object + '_widget"]//li[' + str(nth) + ']//div[@class="tier-2-info-content"]//div[@class="action-bar"]/ul[2]/li/a'       
        self.util.waitForElementToBePresent(xpath, 20)
        self.util.clickOn(xpath) 
        time.sleep(7)
         
    @log_time
    # Object is singular and Capitalized first letter, and can be program, control, etc.
    # Find item based on the_email in tier 1, is the option  
    def expandItemWidget(self, object, title="", isProgram=False):
        
        objectLowercase = str(object).lower()
        
        if objectLowercase == "data":
            objectLowercase = "data_asset"
        if objectLowercase == "group":
            objectLowercase = "org_group"    
        
        # make sure you select the widget first before you can unmap
        # but if the widget is already open then do have to click on it
        self.selectInnerNavTab(objectLowercase)
        time.sleep(10)  # takes time to load
        open_mapping_modal_window_link = elem.section_widget_join_object_link.replace("OBJECT", object)
        time.sleep(2)  
               
        count = self.countOfAnyObjectInWidget(objectLowercase)
        
        if title=="":
            if objectLowercase == "person" and isProgram == True:
                # First row is owner and you can't unmap owner.  Program needs to have at least one owner
                self.expandNthItemInWidget(objectLowercase, 2)
            else:
                self.expandNthItemInWidget(objectLowercase)
        else:
            while (count > 0):
                
                if object=="Person":
                    xpath = '//ul[contains(@class, "tree-structure new-tree colored-list cms_controllers_tree_view")]/li[' + str(count) + ']//span[contains(@class, "email")]'
                else:
                    xpath = '//ul[contains(@class, "tree-structure new-tree colored-list cms_controllers_tree_view")]/' \
                            'li[@data-object-type="' + object + '"][' + str(count) + ']//div[@class="span12"]/div[@class="item-data"]/div'
                
                text = self.util.getTextFromXpathString(xpath)
                
                if text==title:
                    self.expandNthItemInWidget(objectLowercase, count)
                    return count
                    break
                else:
                    count = count - 1
                  
 
    @log_time
    # lower case, e.g., data_asset
    def selectInnerNavTab(self, object):
        xpath = '//a[@href="#OBJECT_widget"]/div'
        tab = str(xpath).replace("OBJECT", object)
        self.util.clickOn(tab)

 
    @log_time
    # Return title from the widget table based on the passed-in index
    def getTitleFromWidgetList(self, index, section=""):
        if section == "Section":
          xp = '//div[@id="middle_column"]//li[' + str(index) + ']//ul[@class="tree-action-list"]/../div//div[@class="tree-title-area"][1]//span[@class="person-tooltip-trigger"]'
        elif section == "Person":
          xp = '//div[@id="middle_column"]//li[' + str(index) + ']//ul[@class="tree-action-list"]/../div//div[@class="tree-title-area"][1]'
        
        self.util.waitForElementToBePresent(xp)
        txt = self.util.getTextFromXpathString(xp)
        return str(txt)
   
    @log_time
    # Expand 4th tier from mapping recursion
    def expandWidget4thTier(self, title, make_relevant=False):
        person_email_link = '//div[@id="middle_column"]//li[@class="tree-item cms_controllers_tree_view_node"]//div[@class="tree-title-area"]/span'
        row = '//div[@id="middle_column"]//li[@class="tree-item cms_controllers_tree_view_node"]//div[@class="openclose"]'
        relevant_chkbx = '//a[@class="info-action pull-right map-to-page-object relevant-action"]/i'
        
        if make_relevant == True:
            self.util.waitForElementToBePresent(relevant_chkbx)   
            self.util.clickOn(relevant_chkbx)
        
        self.util.waitForElementToBePresent(row)      
        self.util.clickOn(row)
        time.sleep(4)
   
    # You want to check or uncheck the box.  Set it True to check on the box, False to uncheck
    def makeAllRelevant(self, check_flag):
        unchecked = '//div[@id="middle_column"]//section[contains(@id, "clause_widget")]/section//div[@class="inner-tree"]//h6/a/i[@class="grcicon-check"]'
        checked = '//div[@id="middle_column"]//section[contains(@id, "clause_widget")]/section//div[@class="inner-tree"]//h6/a/i[@class="grcicon-checked"]'
    
        if check_flag == True:
            if self.util.isElementPresent(unchecked) == True:
                self.util.clickOn(unchecked)
        else:
             if self.util.isElementPresent(checked) == True:
                self.util.clickOn(checked)
        time.sleep(10)  # takes some time to show effect
   
    # Click on the unmap link        
    def clickOnUnmapLink(self):
        self.util.waitForElementToBePresent(elem.widget_edit_gear, 10)
        self.util.clickOn(elem.widget_edit_gear)
        time.sleep(2)
        self.util.waitForElementToBePresent(elem.unmap_lk, 10)
        self.util.clickOn(elem.unmap_lk)

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
            self.util.waitForElementToBePresent('//ul[@class="dropdown-menu"]/li/a[@href="/logout"]')
            self.util.clickOn('//ul[@class="dropdown-menu"]/li/a[@href="/logout"]')
        time.sleep(3)     

    def getRoleLabelInTopRight(self):
        toggle_dropdown = '//ul[@class="menu"]/li[@class="user dropdown dropdown-black black-link"]/a'
        self.util.clickOn(toggle_dropdown)       
        time.sleep(2)

        text = self.util.getTextFromXpathString('//ul[@class="dropdown-menu"]/li[1]/a')
        role_label = self._countInsideParenthesis(text, True)
        
        self.util.clickOn(toggle_dropdown)  # collapse the menu
        return role_label
        
    @log_time
    # select menu items on inner nav on Admin Dashboard
    def selectMenuItemInnerNavDashBoard(self, item):       
        xpath = '//div[@class="object-nav"]/ul[@class="nav internav  cms_controllers_inner_nav ui-sortable"]'
        self.util.waitForElementToBePresent(xpath)
        
        if item == "People":
            self.util.clickOn(xpath + '/li/a[@href="#people_list_widget"]')
            time.sleep(25) 
        elif item == "Roles":
            self.util.clickOn(xpath + '/li/a[@href="#roles_list_widget"]')
            time.sleep(20) 
        elif item == "Events":
            self.util.clickOn(xpath + '/li/a[@href="#events_list_widget"]')
            time.sleep(40)        
               
    @log_time
    # Return correct count of any object
    # theObject is a singular form, e.g., Person, Objective, Standard, etc. 
    def countOfAnyObjectLHS(self, theObject):
        xpath = '//a[contains(@data-object-singular,"OBJECT")]/small/span'
        xpath = xpath.replace("OBJECT", theObject)
        self.util.waitForElementToBePresent(xpath, 15)
        time.sleep(5)
        return int(self.util.getTextFromXpathString(xpath))
    
    @log_time
    # User Role Assignment inside Admin Dashboard
    def assignUserRole(self, role):
        time.sleep(15)
        xpath = '//div[@class="selector-list people-selector"]/ul/li[INDEX]//div[@class="tree-title-area"]'
        radio_bt = '//div[@class="selector-list people-selector"]/ul/li[INDEX]//input[@type="radio"]'
        roleAssignmentCount = '//div[@class="modal modal-selector hide ui-draggable in ggrc_controllers_user_roles_modal_selector"]//div[@class="option_column"]/div[@class="search-title"]/div/div/h4'
        done = '//div[@class="confirm-buttons"]/a'
        
        text = self.util.getTextFromXpathString(roleAssignmentCount)   
        count = self._countInsideParenthesis(text)
        role = str(role).lower()
        
        for indx in range(1, count + 1):
            text = self.util.getTextFromXpathString(str(xpath).replace("INDEX", str(indx))).lower()
        
            if role == text:
                self.util.clickOn(str(radio_bt).replace("INDEX", str(indx)))
                time.sleep(1)
                self.util.clickOn(done)
                time.sleep(2)
                return True
        
        return False  # fail to assign
            
     
    
    
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
        
        singularLower = str(singularLower).lower()  # make sure lowercase
        #xpath = '//section[@id="' + singularLower + '_widget"]//span[@class="object_count"]'
        xpath = str('//a[@href="#OBJECT_widget"]/div').replace('OBJECT', singularLower)
        self.util.waitForElementToBePresent(xpath)
        raw_text = self.util.getTextFromXpathString(str(xpath))
        raw_text = raw_text.encode('ascii', 'ignore')
        raw_text = str(raw_text).strip()
        count = self._countInsideParenthesis(raw_text)        
        return int(count)
 
    @log_time
    # Add person in Admin DashBoard and return True if successful, otherwise return False
    # To test Cancel, just set Save=False
    # To disable person, set it Enabled=False
    def addPersonInAdminDB(self, name="", email="", company="", Save=True, Enabled=True):
        
        add_person_bt = '//a[@class="btn-add" and @data-object-plural="people"]'
        pName_txtbx = '//input[@id="person_name"]'
        pEmail_txtbx = '//input[@id="person_email"]'
        pCompany_txtbx = '//input[@id="person_company"]'
        save_bt = '//div[@class="confirm-buttons"]//a[@data-toggle="modal-submit"]'
        cancel_bt = '//div[@class="deny-buttons"]//a'
        enabled_true = '//input[@type="checkbox" and @id="person_is_enabled" and @value="true"]'
        enabled_false = '//input[@type="checkbox" and @id="person_is_enabled" and @value="false"]'
        
        countBefore = self._countOfPeopleFromAdminDB()
        
        self.util.waitForElementToBePresent(add_person_bt, 10)
        self.util.clickOn(add_person_bt)
        self.util.waitForElementToBePresent(pName_txtbx, 10)  
        self.util.inputTextIntoField(name, pName_txtbx)
        self.util.inputTextIntoField(email, pEmail_txtbx)
        self.util.inputTextIntoField(company, pCompany_txtbx)
           
        if Enabled == True: 
            if self.util.isElementPresent(enabled_false) == True: 
                self.util.clickOn(enabled_false)
        else:
            if self.util.isElementPresent(enabled_true) == False: 
                self.util.clickOn(enabled_true)
           
           
        if Save == True:
            self.util.clickOn(save_bt)
        else:
            self.util.clickOn(cancel_bt)
        
        time.sleep(5)
        self.util.waitForElementToBeVisible(add_person_bt, 10)
        time.sleep(2)
        countAfter = self._countOfPeopleFromAdminDB()       
                                            
        if (countAfter == countBefore + 1):
            return True
        else:
            return False
    
    # This function is handle in special situation where you want to click on a specified web element
    def clickCancelButtonOnAddPersonModal(self):
        cancel_bt = '//div[@class="deny-buttons"]//a'
        self.util.clickOn(cancel_bt)
        
    
    def _countOfPeopleFromAdminDB(self):
        time.sleep(15)
        xpathCount = '//div[@class="object-nav"]//li/a[@href="#people_list_widget"]/div'
        self.util.waitForElementToBePresent(xpathCount)
        countText = self.util.getTextFromXpathString(xpathCount)
        count = self._countInsideParenthesis(countText)
        return count

    # count for people, roles, or events ?
    # look at count on tab
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
    
    # count for people, roles, or events ?
    # look at count NOT on tab, but on the label on top of the table
    def _countOfObjectsFromAdminDBLabel(self, item):
        
        xpathCount = '//section[@id="ITEM_list_widget"]//div[contains(@class, "span9")]//span[@class="object_count"]'
        
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
    def searchPersonInAdminDB(self, term, search_by="name"):
        
        if search_by == "name":
            # row = '//section[@id="people_list_widget"]//ul[@class="tree-structure new-tree"]/li[1]//div[@class="tree-title-area"]/span[@class="person-holder"]/a/span'
            row = '//li[1]//div[@class="tree-title-area"]//span[contains(@class, "person-tooltip-trigger")]' 
        else:  # by email
            row = '//section[@id="people_list_widget"]//ul[@class="tree-structure new-tree"]/li[1]//div[@class="tree-title-area"]/span[@class="email"]'
        
        # alternative way: search it myself
        xpathCount = '//div[@class="object-nav"]//li/a[@href="#people_list_widget"]/div'
        next_page = '//ul[@class="tree-structure new-tree"]/li[@class="tree-footer tree-item tree-item-add sticky sticky-footer"]/a[@data-next="true"]'
        countText = self.util.getTextFromXpathString(xpathCount)
        # count = self._countInsideParenthesis(countText) + 1
        
        filter_txtbx = '//input[@name="search"]'
        
        # filter is now working; use it to narrow down the entries
        self.util.inputTextIntoFieldAndPressEnter(term, filter_txtbx)
        time.sleep(5)
        count = self._countOfPeopleFromAdminDB() + 1       
        time.sleep(5)
        
        for indx in range(1, count):
            # 50 entries per page
            modulo = indx % 50
            
            if modulo == 0:
                modulo = 50  # so 100, 150, 200... => 50
                self.util.max_screen()  # to see NEXT_PAGE, must maximize         
                self.util.waitForElementToBePresent(next_page)               
                self.util.clickOn(next_page)
                time.sleep(30)
                      
            rowX = str(row).replace("INDEX", str(modulo))           
            rowX = str.strip(rowX)
            
            does_entry_exist = self.util.waitForElementToBePresent(rowX, 20)
            
            # no entry means that email is not in used, get out of here now
            if does_entry_exist == False:
                return False
            
            text = str(self.util.getTextFromXpathString(rowX))
            
            if term == text:
                print "Index: " + str(indx) + " " + text
                return True
               
        return False  # outside of loop,

    @log_time
    # verify that it can go to the next page for previous page, and return if successful and false otherwise
    # Pre-condition:  Must have at least 51 records in the Event Log Table to be able to test
    # If tab equals "people" it goes to PEOPLE tab otherwise it goes to EVENTS  
    def verifyPrevNextOperation(self, tab="events"):
        
        if tab == 'people':
            # xpath name
            # xpath = '//section[@id="people_list_widget"]//ul[@class="tree-structure new-tree"]/li[1]//div[@class="tree-title-area"]/span[@class="person-holder"]/a/span'
            xpath = '//li[1]//div[@class="tree-title-area"]//span[contains(@class, "person-tooltip-trigger")]'            
            name = str(self.util.getTextFromXpathString(xpath))
            
            if name == "":  # name cannot be blank, CORE-733
                return False
                        
            # email
            row1 = '//li[1]//div[@class="tree-title-area"]//span[contains(@class, "email")]'
            next_page = '//ul[contains(@class, "tree-structure new-tree")]/li[contains(@class, "tree-footer tree-item tree-item-add")]/a[@data-next="true"]'
            prev_page = '//ul[contains(@class, "tree-structure new-tree")]/li[contains(@class, "tree-footer tree-item tree-item-add")]/a[3]'
        else:
            row1 = '//ul[@class="tree-structure new-tree event-tree"]/li[1]//div[@class="tree-title-area"]/ul/li[1]/strong'
            next_page = '//ul[@class="tree-structure new-tree event-tree"]/li[contains(@class, "tree-footer tree-item tree-item-add")]/a[@data-next="true"]'
            prev_page = '//ul[@class="tree-structure new-tree event-tree"]/li[contains(@class, "tree-footer tree-item tree-item-add")]/a[2]'
        
        # text at row1 before clicking on the Next
        row1_text = str(self.util.getTextFromXpathString(row1))
            
        if self.util.isElementPresent(next_page) == True:
            self.util.clickOn(next_page)
            time.sleep(40)
            updated_text = str(self.util.getTextFromXpathString(row1))
            
            if row1_text == updated_text:
                return False
            print "NEXT page button is tested."
        else:
            print "NEXT page button is not available for testing."
          
        if self.util.isElementPresent(prev_page) == True:
            self.util.clickOn(prev_page)
            time.sleep(40)
            updated_text = str(self.util.getTextFromXpathString(row1))
            
            if row1_text != updated_text:
                return False
            print "PREVIOUS page button is tested."
        else:
            print "PREVIOUS page button is not available for testing."
        
        return True  # return TRUE if passes both tests            
 
    @log_time
    # Search for the specified role and return True if found, otherwise return False    
    def searchRoleInAdminDB(self, title):
               
    # alternative way: search it myself
        xpathCount = '//div[@class="object-nav"]//li/a[@href="#roles_list_widget"]/div'
        row = '//section[@id="roles_list_widget"]/section/ul/li[INDEX]//ul[@class="tree-action-list"]/../div[@class="item-data"]/div'
        
        countText = self.util.getTextFromXpathString(xpathCount)
        count = self._countOfObjectsFromAdminDB("roles") + 1
        
        for indx in range(1, count):
            rowX = str(row).replace("INDEX", str(indx))
            name = self.util.getTextFromXpathString(rowX)
              
            if title == name:
                print title + " role is found in the in the database."
                return True
               
        return False  # outside of loop,        
        
        
    @log_time
    # Expand person row if found and return its index
    # Note: This function should not be used when text is entered in the searchbox and auto filtered because xpath is different  
    def _expandPersonInAdminDB(self, term, search_by="name"):
        # xpath = '//section[@id="people_list_widget"]//ul[@class="tree-structure new-tree"]/li[INDEX]//div[@class="tree-title-area"]/span[@class="email"]'
        # first_row_name = '//section[@class="content ggrc_controllers_list_view"]//span[@class="person-holder"]/a/span'
        
        xpathCount = '//div[@class="object-nav"]//li/a[@href="#people_list_widget"]/div'    
        row = '//section[@id="people_list_widget"]//ul[contains(@class, "tree-structure new-tree")]/li[INDEX]//div[@class="tree-title-area"]/span[@class="email"]/..'
        
        if search_by == "name":
            # xpath = '//section[@id="people_list_widget"]//ul[@class="tree-structure new-tree"]/li[INDEX]//div[@class="tree-title-area"]/span[@class="person-holder"]/a/span'
            xpath = '//li[1]//div[@class="tree-title-area"]//span[contains(@class, "person-tooltip-trigger")]'
        else:  # by email
            xpath = '//section[@id="people_list_widget"]//ul[contains(@class, "tree-structure new-tree")]/li[INDEX]//div[@class="tree-title-area"]/span[@class="email"]'
        
        countText = self.util.getTextFromXpathString(xpathCount)
        # count = self._countInsideParenthesis(countText) + 1
        count = self._countOfPeopleFromAdminDB() + 1
        
        for index in range (1, count):
            myXPath = xpath.replace("INDEX", str(index))
            text = str(self.util.getTextFromXpathString(myXPath))
            if (term == text):
                self.util.clickOn(str(row).replace("INDEX", str(index)))  # click on it to expand
                time.sleep(2)
                return index
            
    @log_time
    # Expand person row if found and return its index
    # Note: This can be used after the item has been filtered such that there is only one row in the table 
    def _expandPersonFirstRowInAdminDB(self, personName, search_by="name"):
        
        if search_by == "name":
            first_row = '//section[@class="content ggrc_controllers_list_view"]//span[@class="person-holder"]/a/span'
        else:  # by email
            first_row = '//section[@class="content ggrc_controllers_list_view"]//span[@class="email"]'

        self.util.waitForElementToBePresent(first_row, 10)
        self.util.clickOn(first_row)
        return 1  # index
        
    def isEditAuthorizationPresent(self):
        edit_auth = '//a[@data-modal-selector-options="user_roles"]' 
        return self.util.isElementPresent(edit_auth)      
            
    def isSubmitForReviewPresent(self):
        link = '//div[@id="middle_column"]//a[@title="Edit "]/../../li[1]/a'
        return self.util.isElementPresent(link)
    
    def clickSubmitForReview(self):
        link = '//div[@id="middle_column"]//a[@title="Edit "]/../../li[1]/a'
        self.util.waitForElementToBePresent(link, 15)            
        self.util.clickOn(link)
        time.sleep(12)   
    
            
    @log_time
    # It will seach for the person name and click Edit Authorization link from it  
    # Pre-condition: you are already on the Admin Dashboard view, or you are already in expanded 2nd tier of person object in People widget
    def clickOnEditAuthorization(self, personName, inDBView=True, permission="No access"):
        time.sleep(3)
        if inDBView==True:       
            indx = self._expandPersonInAdminDB(personName)
            edit_auth = '//div[@id="middle_column"]//ul[@class="tree-structure new-tree tree-open"]/li[' + str(indx) + ']//ul[@class="change-links"]/li/a[@data-modal-selector-options="user_roles"]/span'
            self.util.waitForElementToBePresent(edit_auth, 15)            
            self.util.clickOn(edit_auth)
            time.sleep(15)
        else:
            edit_auth = '//a[@data-modal-selector-options="user_roles"]'
            save_xpath = '//div[@class="confirm-buttons"]/a'
            save_css = '[xdata-toggle=modal-submit]'
            self.util.clickOn(edit_auth)
            
            if permission=="No access":
                radio_bt = '//div[@class="selector-list people-selector"]/ul/li[1]//input'
            elif permission=="ProgramReader":
                radio_bt = '//div[@class="selector-list people-selector"]/ul/li[4]//input'
            elif permission=="ProgramEditor":
                radio_bt = '//div[@class="selector-list people-selector"]/ul/li[3]//input'
            elif permission=="ProgramOwner":
                radio_bt = '//div[@class="selector-list people-selector"]/ul/li[2]//input'
            self.util.clickOn(radio_bt)
            self.util.clickOn(save_xpath)
        
    @log_time 
    # create private program assign it to a person and set his reading permission level
    # and return program title
    # permission: {No access, "ProgramReader", "ProgramEditor", "ProgramOwner"}
    def createPrivateProgramPermission(self, email, prgm_name="", permission="No access"):

        if prgm_name=="":
            prgm_name = "Auto_Private_" + self.getTimeId() + str(self.getRandomNumber())
            
        last_created_object_link = self.createObject("Program", prgm_name, "checked")
 
        self.navigateToMappingWindowForObject("Person", (), True)                             
        self.mapFirstObject("Bypass_Person", email, True, "", 1, True)
        self.expandItemWidget("Person", email)
        
        self.clickOnEditAuthorization("don't care", False, permission)
        
        return prgm_name
            

        
    @log_time
    # It will seach for the person name and click Edit Person link from it 
    # Pre-condition: you are already on the Admin Dashboard view 
    def clickOnEditPerson(self, personName):
        indx = self._expandPersonInAdminDB(personName)       
        edit_person = '//div[@id="middle_column"]//ul[@class="tree-structure new-tree tree-open"]/li[' + str(indx) + ']//a[@data-object-singular="Person"]/span'
        self.util.waitForElementToBeVisible(edit_person, 15)
        self.util.clickOn(edit_person)
        time.sleep(2)
        
    @log_time
    # It clicks on Edit Person link, and change that person email to something else
    # Pre-condition: Already at people tab in Admin Dashboard
    def zeroizeThePersonEmail(self, email):        
        is_found = self.searchPersonInAdminDB(email, "by email")
        
        if is_found != True:
            return False;  # no need to do more since it does not exist
        
        self._expandPersonFirstRowInAdminDB(email, "by email")
        
        aEmail = "auto_email_" + str(self.getRandomNumber(65535)) + "@gmail.com"
        email_txtbx = '//input[@id="person_email"]'  
        company_txtbx = '//input[@id="person_company"]'     
        save_bt = '//div[@class="confirm-buttons"]//a[@data-toggle="modal-submit"]'              
        edit_person = '//div[@id="middle_column"]//ul[@class="tree-structure new-tree tree-open"]/li[1]//a[@data-object-singular="Person"]/span'
               
        self.util.waitForElementToBeVisible(edit_person, 15)
        self.util.clickOn(edit_person)
        time.sleep(8)  # delay so pop up shows
        self.util.inputTextIntoField(aEmail, email_txtbx)
        self.util.inputTextIntoField(aEmail, company_txtbx)  # to make SAVE button clickable
        self.util.clickOn(save_bt)
        time.sleep(5)  # relax        
        
        
    @log_time
    # Return TRUE if everything matches up correctly
    def verifyPersonInfoOnSecondTier(self, name="", email="", company="", role=""):
        name_xp = '//div[@id="middle_column"]//ul[@class="tree-structure new-tree tree-open"]/li[1]//div[@class="small-info"]/div[1]//h3'
        email_xp = '//div[@id="middle_column"]//ul[@class="tree-structure new-tree tree-open"]/li[1]//div[@class="small-info"]/div[2]//a'
        company_xp = '//div[@id="middle_column"]//ul[@class="tree-structure new-tree tree-open"]/li[1]//div[@class="small-info"]/div[3]//h3'
        role_xp = '//div[@id="middle_column"]//ul[@class="tree-structure new-tree tree-open"]/li[1]//div[@class="small-info"]/div[4]//span'
        
        name_txt = str(self.util.getTextFromXpathString(name_xp)).lower()
        email_txt = str(self.util.getTextFromXpathString(email_xp)).lower()
        company_txt = str(self.util.getTextFromXpathString(company_xp)).lower()
        role_txt = str(self.util.getTextFromXpathString(role_xp)).lower()
        
        if name != "":
            self.assertEqual(str(name).lower(), name_txt, "Expect " + name + " but see " + name_txt)
        if email != "":
            self.assertEqual(str(email).lower(), email_txt, "Expect " + email + " but see " + email_txt)            
        if company != "":
            self.assertEqual(str(company).lower(), company_txt, "Expect " + company + " but see " + company_txt)            
        if role != "":
            self.assertEqual(str(role).lower(), role_txt, "Expect " + role + " but see " + role_txt)
            
        return True        

    @log_time
    # Change username and email in the log_in text file
    def changeUsernameEmail(self, usernameOld, usernameNew, emailOld, emailNew, filePath):
        # WARNING: do not attempt to remove usernameOld and emailOld, indentation will be messed up
        # and can't log back in once noop.py is not compliant to Python indentation stardard
                
        # format looks like this in noop.py file
        oldUsername = "default_user_name = \'" + usernameOld + "\'"
        oldEmail = "default_user_email = \'" + emailOld + "\'"
        newUsername = "default_user_name = \'" + usernameNew + "\'\n"  # add new line
        newEmail = "default_user_email = \'" + emailNew + "\'\n"
        
        # Create temp file
        fh, abs_path = mkstemp()
        new_file = open(abs_path, 'w')
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
        # Remove original file
        remove(filePath)
        # Move new file
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
                return True  # found
                   
        file.close()
        return False  # not found   
        
    @log_time
    # Return true if data is logged to Event Log Table
    # By default, top row (index=0) is selected 
    def verifyInfoInEventLogTable(self, text2Match, row=1, index=1):
        print "Start verifying event log for text: \"" + text2Match + "\"" 
        
        # for row 2
        whom = '//ul[@class="tree-structure new-tree event-tree"]/li[' + str(row) + ']//div[@class="tree-title-area"]//span[contains(@class, "person-tooltip-trigger")]'
        when = '//ul[@class="tree-structure new-tree event-tree"]/li[' + str(row) + ']//div[@class="tree-title-area"]//span[contains(@class, "event-time")]'
        
        if index == 1:
            xpath = '//ul[@class="tree-structure new-tree event-tree"]/li[' + str(row) + ']//div[@class="tree-title-area"]/ul/li[1]/strong'
        else:    
            xpath = '//ul[@class="tree-structure new-tree event-tree"]/li[' + str(row) + ']//div[@class="tree-title-area"]/ul/li[' + str(index) + ']/strong'
        
        self.util.waitForElementToBePresent(xpath, 30)
        text = str(self.util.getTextFromXpathString(xpath))
        
        # this means user wants these fields to be checked
        if text2Match == 'whom':
            by = str(self.util.getTextFromXpathString(whom))
            if by not in config.username:
                return False
            else:
                return True            
        elif text2Match == 'when':
            on = str(self.util.getTextFromXpathString(when))
            if 'PST' not in on:
                return False
            else:
                return True
        elif text2Match in text:
            print ""
            print "'" + text2Match + "' is found in the Event Log table."
            return True
        else:
            return False
        
    
    @log_time
    # Create a rolein Admin DashBoard and return True if successful, otherwise return False
    # To test Cancel, just set Save=False
    def createRoleInAdminDB(self, role, desc="", Save=True):  # TODO expand more
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
       
        if Save == True:
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
        
        if what2Export == "systems":       
            self.util.waitForElementToBeVisible(system_exp_link, 10)
            self.util.clickOn(system_exp_link)
            if "localhost" in config.url:   
                time.sleep(30)
            else:
                time.sleep(180)  # wait 3 minutes  
        elif what2Export == "processes":       
            self.util.waitForElementToBeVisible(process_exp_link, 10)
            self.util.clickOn(process_exp_link)
            if "localhost" in config.url:   
                time.sleep(30)
            else:
                time.sleep(240)  # wait 4 minutes     
        elif what2Export == "people":       
            self.util.waitForElementToBeVisible(people_exp_link, 10)
            self.util.clickOn(people_exp_link)  
            if "localhost" in config.url:   
                time.sleep(15)
            else:
                time.sleep(60)  # wait 1 minutes            
        elif what2Export == "help":       
            self.util.waitForElementToBeVisible(help_exp_link, 10)
            self.util.clickOn(help_exp_link)             
            if "localhost" in config.url:   
                time.sleep(15)
            else:
                time.sleep(30)  # wait 30 seconds          
                
  
    def getWrongTypeMessage(self):
        msg_xpath = '//div[@id="sampleData"]/p[1]'
        text = self.util.getTextFromXpathString(msg_xpath)
        time.sleep(1)
        return text
  
    def getImportFailedMessage(self):
        msg_xpath = '//div[contains(@class, "error")]/strong'
        text = self.util.getTextFromXpathString(msg_xpath)
        return str(text)
  
  
    @log_time
    # Return true if import successfully, otherwise return False
    # Pre-condition: You are already in Admin Board.  Same for the other export functions
    # what2Import is one of these:  System, Process, People, Help
    def importFile(self, what2Import, file2Import, positiveTest=True, msg=""):
        print""
        print "Start importing: " + file2Import
        
        imp_exp_xpath = '//div[@id="page-header"]/..//div[2]//a[@data-toggle="dropdown"]'       
        system_imp_link = '//div[@id="page-header"]/..//ul[@class="dropdown-menu"]/li//a[@href="/systems/import"]'
        process_imp_link = '//div[@id="page-header"]/..//ul[@class="dropdown-menu"]/li//a[@href="/processes/import"]'
        people_imp_link = '//div[@id="page-header"]/..//ul[@class="dropdown-menu"]/li//a[@href="/admin/import/people"]'
        help_imp_link = '//div[@id="page-header"]/..//ul[@class="dropdown-menu"]/li//a[@href="/admin/import/help"]'        
        choose_file_bt = '//input[@type="file"]'
        upload_bt = '//input[@type="submit" and @value="Upload and Review"]'
        x_button = '//div[@id="sampleData"]/div/button[@class="close"]'
        error_msg = '//div[@id="sampleData"]/div[@class="alert alert-error"]'
        missing_msg = '//div[@id="sampleData"]/p'

        proceed_with_caution_bt = '//input[@type="submit" and @value="Proceed with Caution"]'

        self.util.waitForElementToBeVisible(imp_exp_xpath, 10)
        self.util.clickOn(imp_exp_xpath)
        
        if what2Import == "Systems":       
            self.util.waitForElementToBeVisible(system_imp_link, 10)
            self.util.clickOn(system_imp_link)
        elif what2Import == "Processes":       
            self.util.waitForElementToBeVisible(process_imp_link, 10)
            self.util.clickOn(process_imp_link) 
        elif what2Import == "People":       
            self.util.waitForElementToBeVisible(people_imp_link, 10)
            self.util.clickOn(people_imp_link)           
        elif what2Import == "Help":  
            self.util.waitForElementToBeVisible(help_imp_link, 10)
            self.util.clickOn(help_imp_link)
                      
        self.util.uploadItem(file2Import, choose_file_bt)
        self.util.clickOn(upload_bt)
        time.sleep(8)
        if positiveTest == True:
            self.util.waitForElementToBePresent(proceed_with_caution_bt)
            self.util.clickOn(proceed_with_caution_bt)
            time.sleep(7)
            return True
        else:
            # warning message
            if "Warning" in msg:
                missing_msg = str(self.util.getTextFromXpathString(missing_msg))
                if msg in missing_msg:
                    return False
            # error message
            else:
                error_msg = self.util.getTextFromXpathString(error_msg)
                error_msg = error_msg.encode('ascii', 'ignore')
                error_msg = str(error_msg).strip()
                if msg in error_msg:
                    return False
         
    def appendToFile(self, text, filePath):
        with open(filePath, "a") as myfile:
            myfile.write(text)
            myfile.close()
         
            
    # Private function.  Return only content (count in this case) from inside parenthesis
    # It can be used on any alphanumeric too
    def _countInsideParenthesis(self, text, no_int=False):
        start = text.index("(") + int(1)
        end = text.index(")")
        text = text[start:end]
        
        if no_int==True:
            return text
        else:
            return int(text)
    
    def getElem(self):
        return self.elem
    
    def getUniqueString(self, title=""):
        auto_title = title + "-auto-test" + str(datetime.datetime.now().time())
        return auto_title
    
    def getRandomNumber(self, max=sys.maxint, min=0):
        return randint(min, max)

    # Just file name,  no path
    def getScreenshot(self, filename):
        filepath = config.file_download_path + "/" + filename
        self.util.getScreenshot(filepath)
    
    def refresh(self):
        self.util.refreshPage()
        time.sleep(15)

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
        name = self.util.getTextFromXpathString(user_name_displayed)
        name = str(name).strip().lower()
        return name
    
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
        
    def clearSearchBoxOnLHS(self):
        # self.driver.find_element_by_xpath(elem.search_inputfield).clear()
        self.util.inputTextIntoFieldAndPressEnter("", elem.search_inputfield)
        time.sleep(1)
        
    def delay(self, seconds):
        time.sleep(seconds)
        
    def cancelButtonOnModalWindow(self):
        cancel_bt_css = '[data-dismiss=modal-reset]'
        self.util.clickOnCSS(cancel_bt_css)
    
    @log_time
    # Verify that these roles exist (programReader, programEditor, programOwner)
    def verifyDifferentRolesExist(self):       
        print "Start verifying roles existence..."
        
        admin = '//ul[@class="tree-structure new-tree"]/li[1]//div[@class="tree-title-area"]/span[@class="scope"]/../../../../../div/div'
        object_editor = '//ul[@class="tree-structure new-tree"]/li[2]//div[@class="tree-title-area"]/span[@class="scope"]/../../../../../div/div'
        program_creator = '//ul[@class="tree-structure new-tree"]/li[3]//div[@class="tree-title-area"]/span[@class="scope"]/../../../../../div/div'
        program_editor = '//ul[@class="tree-structure new-tree"]/li[4]//div[@class="tree-title-area"]/span[@class="scope"]/../../../../../div/div'
        program_owner = '//ul[@class="tree-structure new-tree"]/li[5]//div[@class="tree-title-area"]/span[@class="scope"]/../../../../../div/div'
        program_reader = '//ul[@class="tree-structure new-tree"]/li[6]//div[@class="tree-title-area"]/span[@class="scope"]/../../../../../div/div'
        reader = '//ul[@class="tree-structure new-tree"]/li[7]//div[@class="tree-title-area"]/span[@class="scope"]/../../../../../div/div'
        workflow_member = '//ul[@class="tree-structure new-tree"]/li[8]//div[@class="tree-title-area"]/span[@class="scope"]/../../../../../div/div'
        workflow_owner = '//ul[@class="tree-structure new-tree"]/li[9]//div[@class="tree-title-area"]/span[@class="scope"]/../../../../../div/div'

        text = str(self.util.getTextFromXpathString(admin)).lower()
        self.assertEqual("ggrc admin", text, "Expect admin but see " + text)
               
        text = str(self.util.getTextFromXpathString(object_editor)).lower()
        self.assertEqual("objecteditor", text, "Expect object editor but see " + text)

        text = str(self.util.getTextFromXpathString(program_creator)).lower()
        self.assertEqual("programcreator", text, "Expect program creator but see " + text)

        text = str(self.util.getTextFromXpathString(program_editor)).lower()
        self.assertEqual("programeditor", text, "Expect program editor but see " + text)

        text = str(self.util.getTextFromXpathString(program_owner)).lower()
        self.assertEqual("programowner", text, "Expect program owner but see " + text)

        text = str(self.util.getTextFromXpathString(program_reader)).lower()
        self.assertEqual("programreader", text, "Expect program reader but see " + text)
        
        text = str(self.util.getTextFromXpathString(reader)).lower()
        self.assertEqual("reader", text, "Expect reader but see " + text)       
        
        text = str(self.util.getTextFromXpathString(workflow_member)).lower()
        self.assertEqual("workflowmember", text, "Expect workflow member but see " + text)          
        
        text = str(self.util.getTextFromXpathString(workflow_owner)).lower()
        self.assertEqual("workflowowner", text, "Expect workflow owner but see " + text)   
        
        print "All roles exist." 
     
    # When All Objects radio button is checked, we want to know if objects created by other users are also shown as expected.  
    # So we want to see at least 2 different user names
    # PRE-CONDITIONS:  Be sure there are at least 2 program objects created by 2 different users 
    # object is like "Program" or "Person", etc.   
    def verifyAllUsersObjectsShown(self, object):
            self.ensureLHNSectionExpanded(object)
            count = self.countOfAnyObjectLHS(object)
            
            for INDEX in range(1, count):
                user_email_css = '#extended-info [class="extended-info-contact"] [class="person-tooltip-trigger"][data-original-title]'
                second_link_of_the_section_link = '//ul[@class="top-level"]//li[contains(@data-model-name,"' + object + '")]/div/ul[contains(@class, "sub-level")]/li[' + str(INDEX) + ']'
                self.assertTrue(self.util.waitForElementToBePresent(second_link_of_the_section_link), "ERROR inside mapAObjectLHN(): cannot see the first " + object + " in LHN")
                self.util.waitForElementToBePresent(second_link_of_the_section_link)
                #idOfTheObject = self.util.getTextFromXpathString(second_link_of_the_section_link)
                self.util.hoverOverAndWaitFor(second_link_of_the_section_link, elem.map_to_this_object_link)
                
                if INDEX == 1:
                    user_email_control = self.util.getTextFromCSSString(user_email_css)
                else:
                    user_email_rotate = self.util.getTextFromCSSString(user_email_css)
         
                # We already have 2 samples and the user_emails differ that means we see 2 users
                if user_email_control == user_email_rotate:
                    if INDEX < count:
                        # keep going
                        continue
                    else:
                        self.assertTrue(False, "Fail to see objects created by at least 2 different users.") #brute-force error message
                        
                elif not user_email_control == user_email_rotate and \
                    INDEX > 1:
                    print( "See objects created by at least 2 different users for object type: " + object)
                    break # see at 2 different users
                    
                    

         
         
           
    # ******************** simple click functions ************************        
    def clickHelpTopRightCorner(self):
        self.util.clickOn(elem.help)
    
    def clickHelpEdit(self):
        self.util.clickOnCSS(elem.edit_help_css, 10)

    def clickHelpIcon(self):
        self.util.clickOnCSS(elem.help_icon_css)
        
    def clickHelpDone(self):
        self.util.clickOn(elem.help_done)

    def clickHelpSave(self):
        self.util.clickOnCSS(elem.save_help_css)
        
    def addHelpTitleContent(self, title, content):
        self.clickHelpTopRightCorner()
        self.clickHelpEdit()
        self.util.inputTextIntoFieldAndPressEnter(title, elem.help_title)
        # TODO fix this later, now it just can't clear it
        #self.util.inputTextIntoFieldAndPressEnter(content, elem.help_content)
        self.clickHelpSave()
        self.clickHelpDone()
        
    def getHelpTitle(self):
        return self.util.getTextFromXpathString(elem.grc_help_title_text_css)
    
    def getHelpContent(self):
        return self.util.getTextFromXpathString(elem.help_content)
    
    def clickMyTasksIcon(self):
        self.util.clickOnCSS(elem.my_tasks_icon)
        
    def isMyObjectsOnlyPresent(self):
        return self.util.isElementPresent(elem.my_work_checkbox)
        
    def isAllObjectsPresent(self):
        return self.util.isElementPresent(elem.everyone_work_checkbox)        
    
    # item is like Person -- it return People (plural)
    def getItemLabelInLHS(self, item):
        item_link = elem.left_nav_expand_object_section_link.replace("OBJECT", item)
        return self.util.getTextFromXpathString(item_link)    
    
    # default is to get text up to first space;  if desire for second space, pass in 2
    def getTextUpToNthSpace(self, text, nth=1):
        
        if nth==1:
            index = str(text).index(' ')
            return text[0:index]
        elif nth==2:   # Example:   text = "Data Assets (2)"
            index = str(text).index(' ')
            first_part = text[0:index]  # Data
            
            temp_text = text[index+1:]  # Assets (2)
            index2 = str(temp_text).index(' ')
            second_part = temp_text[0:index2]
            
            sum_text =  first_part + " " + second_part
            
            return sum_text
            
    
    # lowercase both strings before comparison
    def compareText(self, str1, str2):
        str1 = str(str1).lower()
        str2 = str(str2).lower()
        try:
            self.assertEqual(str1, str2, "String 1 and 2 are not equal.")
            return True
        except:
            return False
        
        
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
            
