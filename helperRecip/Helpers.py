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
    
    def getTimeId(self):
        return strftime("_%Y_%m_%d_%H_%M_%S")
    
    def login(self):
        self.assertTrue(self.util.isElementPresent(self.element.login_button), "can't see the login button")
        self.util.clickOnAndWaitFor(self.element.login_button, self.element.gmail_password_textfield)
        self.assertTrue(self.util.isElementPresent(self.element.gmail_password_textfield), "can't see the password textfield")
        self.util.inputTextIntoField(config.username, self.element.gmail_userid_textfield)
        self.assertTrue(self.util.isElementPresent(self.element.gmail_userid_textfield), "can't see the userid textfield")
        self.util.inputTextIntoField(config.password, self.element.gmail_password_textfield)
        self.util.clickOnAndWaitFor(self.element.gmail_submit_credentials_button, self.element.dashboard_title)
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
        self.assertTrue(result,"ERROR in expandLeftNavMenuForObject(): could not click on LHN link for "+grc_object)
        object_left_nav_section_object_add_button = self.element.left_nav_object_section_add_button.replace("OBJECT", grc_object)
        self.assertTrue(self.util.waitForElementToBePresent(object_left_nav_section_object_add_button), "ERROR inside expandLeftNavMenuForObject(): can't see the LHN Create New link for "+ grc_object)
        
        
    def createObject(self, grc_object, object_name=""):
        self.assertTrue(self.util.isElementPresent(self.element.dashboard_title), "no dashboard page found")
        if object_name == "":
            grc_object_name = self.generateNameForTheObject(grc_object)
        else:
            grc_object_name = object_name
        self.openCreateNewObjectWindow(grc_object) 
        self.populateNewObjectData(grc_object_name)
        self.saveObjectData()
        last_created_object_link = self.verifyObjectIsCreated(grc_object, grc_object_name)
        print "Object created successfully."
        return last_created_object_link

    def openCreateNewObjectWindow(self, grc_object):
       
        object_left_nav_section_object_link = self.element.left_nav_expand_object_section_link.replace("OBJECT", grc_object)
        self.assertTrue(self.util.waitForElementToBePresent(object_left_nav_section_object_link), "ERROR inside openCreateNewObjectWindow():can't see the LHN link for "+ grc_object)
        result=self.util.clickOn(object_left_nav_section_object_link)
        self.assertTrue(result,"ERROR in openCreateNewObjectWindow(): could not click on LHN link for "+grc_object)
        object_left_nav_section_object_add_button = self.element.left_nav_object_section_add_button.replace("OBJECT", grc_object)
        self.assertTrue(self.util.waitForElementToBePresent(object_left_nav_section_object_add_button), "ERROR inside openCreateNewObjectWindow():can't see the LHN Create New link for "+ grc_object)
        result=self.util.clickOn(object_left_nav_section_object_add_button)
        self.assertTrue(result,"ERROR in openCreateNewObjectWindow(): could not click on LHN Create New link for "+grc_object)
        


        
    def populateNewObjectData(self, object_title):
        
        # Make sure window is there
        self.util.waitForElementToBeVisible(self.element.modal_window)
        self.assertTrue(self.util.isElementPresent(self.element.modal_window), "can't see modal dialog window for create new object")

        #self.assertTrue(self.util.isElementPresent(self.element.modal), "can't see the modal body")
        
        # Populate title
        self.util.waitForElementToBeVisible(self.element.object_title)
        self.assertTrue(self.util.isElementPresent(self.element.object_title), "can't access the input textfield")
        self.util.inputTextIntoField(object_title, self.element.object_title)
        self.util.inputTextIntoField("", self.element.object_owner) #need this click to activate Save button
        # Populate Description
        #self.util.typeIntoFrame("description-"+object_title)

        
        
    def saveObjectData(self):
        #self.util.inputTextIntoField("testrecip@gmail.com", self.element.modal_owner_textfield) #need this click to activate Save button
        self.assertTrue(self.util.isElementPresent(self.element.modal_window_save_button), "do not see the Save button")
        self.util.clickOnSave(self.element.modal_window_save_button)
        status=self.util.waitForElementNotToBePresent(self.element.modal_window,100)
        self.assertTrue(status,"Save operation taking too long, modal window still visible after 100 seconds")
        self.waitForLeftNavToLoad()

        

        
    def verifyObjectIsCreated(self, widget, object_title): 
        #this helper method is generic for any type 
        
        # Refresh the page
        
        self.util.refreshPage()
        
        # Wait for the object section link to appear in the left nav (e.g. Programs, Products, Policies, etc.)
        
        object_left_nav_section_object_link = self.element.left_nav_expand_object_section_link.replace("OBJECT", widget)
        self.assertTrue(self.util.waitForElementToBePresent(object_left_nav_section_object_link), "ERROR inside verifyObjectIsCreated(): do not see the LHN link for " + widget)

        # Click on the object section link in the left nav
        
        result=self.util.clickOn(object_left_nav_section_object_link)
        self.assertTrue(result,"ERROR in verifyObjectIsCreated(): could not click on LHN link for "+widget)
        
        # Wait for the newly-created object link to appear in the left nav (e.g. System-auto-test_2013_08_25_13_47_50)

        last_created_object_link = self.element.left_nav_last_created_object_link.replace("SECTION", widget).replace("OBJECT_TITLE", object_title)
        self.assertTrue(self.util.waitForElementToBePresent(last_created_object_link), "ERROR inside verifyObjectIsCreated(), do not see the newly created object in " + widget)
        return last_created_object_link
    
    def navigateToObject(self, section, object_title_link):
           # Refresh the page
        
        self.util.refreshPage()
        
        # Wait for the object section link to appear in the left nav (e.g. Programs, Products, Policies, etc.)
        
        object_left_nav_section_object_link = self.element.left_nav_expand_object_section_link.replace("OBJECT", section)
        self.assertTrue(self.util.waitForElementToBePresent(object_left_nav_section_object_link),"ERROR in navigateToObject(): can't see LHN link for "+section)
        
        # Click on the object section link in the left nav
        
        result=self.util.clickOn(object_left_nav_section_object_link)
        self.assertTrue(result,"ERROR in navigateToObject(): could not click on LHN link for "+section)        

        # Wait for the newly-edited object link to appear, then click on it        
        
        self.assertTrue(self.util.waitForElementToBePresent(object_title_link), "ERROR inside navigateToObject(): do not see object  " + object_title_link + " in lhn" )       
        result=self.util.clickOn(object_title_link)
        self.assertTrue(result,"ERROR in navigateToObject(): could not click on object in LHN "+object_title_link)
        
    
    def navigateToObjectAndOpenObjectEditWindow(self,section,object_title_link, refresh_page=True):

        # Refresh the page
        if refresh_page:
            self.util.refreshPage()
        
        # Wait for the object section link to appear in the left nav (e.g. Programs, Products, Policies, etc.)
        
        object_left_nav_section_object_link = self.element.left_nav_expand_object_section_link.replace("OBJECT", section)
        self.assertTrue(self.util.waitForElementToBePresent(object_left_nav_section_object_link),"ERROR inside navigateToObjectAndOpenObjectEditWindow(): can't see object_left_nav_section_object_link")
        
        # Click on the object section link in the left nav
        
        result=self.util.clickOn(object_left_nav_section_object_link)
        self.assertTrue(result,"ERROR in navigateToObjectAndOpenObjectEditWindow(): could not click on link for "+section)        

        # Wait for the newly-edited object link to appear, then click on it        
        
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
        self.util.hoverOver(self.element.object_detail_page_info_section)  
        self.assertTrue(self.util.waitForElementToBePresent(self.element.object_info_page_edit_link), "ERROR inside openObjectEditWindow(): do not see the Edit button")
        result=self.util.clickOn(self.element.object_info_page_edit_link)
        self.assertTrue(result,"ERROR in openObjectEditWindow(): could not click on Edit button "+self.element.object_info_page_edit_link)
        self.assertTrue(self.util.waitForElementToBePresent(self.element.modal_window),"ERROR inside openObjectEditWindow(): can't see modal window")
        self.assertTrue(self.util.waitForElementToBePresent(self.element.object_title), "ERROR inside openObjectEditWindow(): do not see object_title in the edit window")
       
    
    def showHiddenValues(self):
        result=self.util.clickOn(self.element.modal_window_show_hidden_fields_link)
        self.assertTrue(result,"ERROR in showHiddenValues(): could not click on "+self.element.modal_window_show_hidden_fields_link)
        self.util.waitForElementToBeVisible(self.element.modal_window_hidden_fields_area)
    
    def populateObjectInEditWindow(self, name, grcobject_elements,grcobject_values ):
        self.util.waitForElementToBeVisible(self.element.object_title)
        self.showHiddenValues() 
        for key,xpath in grcobject_elements.iteritems():  
            #print key, xpath ,  grcobject_values[key] 
            
            if key in ["network_zone","kind","fraud_related","key_control", "means","type"]:
                dropdown_element = self.element.object_dropdown.replace("NAME",key )
                self.util.waitForElementToBeVisible(dropdown_element) 
                option = self.util.getTextFromXpathString(dropdown_element + "/option[" + str(grcobject_values[key]) + "]")
                self.assertTrue(self.util.isElementPresent(dropdown_element), "no dropdown for " + key+ " isfound")
                self.selectFromDropdownOption(dropdown_element, grcobject_values[key])
                grcobject_values[key]=option
          
            if key=="code":
                self.util.waitForElementToBeVisible(xpath) 
                grcobject_values[key] = self.util.getAnyAttribute(self.element.object_code, "value") + "_edited"
                self.util.inputTextIntoField(grcobject_values[key] ,xpath)
                
            if key in ["title","scope","organization"]:
                self.util.waitForElementToBeVisible(xpath) 
                grcobject_values[key] = name + "_edited" 
                self.util.inputTextIntoField(grcobject_values[key] ,xpath)
            if key == "owner":
                self.util.waitForElementToBeVisible(xpath) 
                grcobject_values[key] = "testrecip@gmail.com" 
                self.util.inputTextIntoField(grcobject_values[key] ,xpath)       
            if key in ["description","notes"]:            
                frame_element = self.element.object_iFrame.replace("FRAME_NAME",key)
                self.util.waitForElementToBeVisible(frame_element)
                grcobject_values[key]=key+"_"+name+ "_edited"
                self.util.typeIntoFrame(grcobject_values[key], frame_element) 
            if key=="url":
                self.util.waitForElementToBeVisible(xpath) 
                grcobject_values[key] = "http://www.google.com"
                self.util.inputTextIntoField(grcobject_values[key] ,xpath)
                
        self.util.inputTextIntoField("testrecip@gmail.com" , self.element.object_owner)
        self.util.inputTextIntoField("http://www.google.com", self.element.object_url) # hack for make the Save button clickable
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
        for key,xpath in grcobject_elements.iteritems(): 
            #print "Inside verifyObjectValues, key=" + key + ", value="+grcobject_values[key]
            if key in ["description","notes"]:
                frame_element = self.element.object_iFrame.replace("FRAME_NAME",key)
                new_value = self.util.getTextFromFrame(frame_element)
                self.assertTrue(new_value == grcobject_values[key], "Verification ERROR: the value of " + key + " should be " + grcobject_values[key] + " but it is " + new_value )
            if key in ["network_zone","kind","fraud_related","key_control", "means","type"]:
                dropdown_element = self.element.object_dropdown.replace("NAME",key )
                dropdown_element_selected_option= self.element.object_dropdown_selected_option.replace("NAME",key )
                self.assertTrue(self.util.waitForElementToBePresent(dropdown_element),"ERROR inside verifyObjectValues(): can't see dropdown element")
                self.assertTrue(self.util.waitForElementToBePresent(dropdown_element_selected_option),"ERROR inside verifyObjectValues(): can't see dropdown element selected option")
                self.assertTrue(self.util.waitForElementValueToBePresent(dropdown_element_selected_option),"ERROR inside verifyObjectValues(): can't see value for dropdown element selected option")
                new_value = self.util.getTextFromXpathString(dropdown_element_selected_option)
                self.assertTrue(new_value == grcobject_values[key], "Verification ERROR: the value of " + key + " should be " + grcobject_values[key] + " but it is " + new_value )
            if key in ["title","owner","code","url", "organization", "scope"]:
                    new_value = self.util.getAnyAttribute(xpath, "value")
                    if not new_value:
                        self.assertTrue(False, "Verification ERROR: could not retrieve the value of " + xpath)
                    #print "new_value="+new_value
                    else:
                        self.assertTrue(new_value == grcobject_values[key], "Verification ERROR: the value of " + key + " should be " + grcobject_values[key] + " but it is " + new_value )
            print "Verification OK: the value of " + key + " is "+str(grcobject_values[key]) +", as expected." 
    
    def deleteObject(self):
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
        
        
  
        
    def mapAObjectWidget(self, object):
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
        
        #select the first object from the search results and map it
        self.assertTrue(self.util.waitForElementToBePresent(self.element.mapping_modal_selector_list_first_object), "ERROR inside mapAObjectWidget(): cannot see first object in the selector")
        idOfTheObjectToBeMapped = self.util.getAnyAttribute(self.element.mapping_modal_selector_list_first_object, "data-id")
        #print "the first "+ object + " id is " +  idOfTheObjectToBeMapped
        self.assertTrue(self.util.waitForElementToBePresent(self.element.mapping_modal_selector_list_first_object_link), "ERROR inside mapAObjectWidget(): cannot see first object LINK in the selector")
        self.util.clickOnAndWaitFor(self.element.mapping_modal_selector_list_first_object_link, self.element.mapping_modal_window_map_button)
        self.assertTrue(self.util.isElementPresent(self.element.mapping_modal_window_map_button), "no Map button")
        result=self.util.clickOn(self.element.mapping_modal_window_map_button)
        self.assertTrue(result,"ERROR in mapAObjectWidget(): could not click on Map button for "+object)
        
        self.util.waitForElementNotToBePresent(self.element.mapping_modal_window)
        self.verifyObjectIsMapped(object, idOfTheObjectToBeMapped)
        
       
       
    def verifyObjectIsMapped(self, object, objectId):
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
        mapped_object = self.element.mapped_object.replace("OBJECT", object.lower()).replace("ID", objectId)
        #print mapped_object
        self.assertTrue(self.util.waitForElementToBePresent(mapped_object), "ERROR inside verifyObjectIsMapped(): no mapped object")
        print "Object " + object + " is mapped successfully"
        
        
    #def waitForInnerNavToLoad(self):
        