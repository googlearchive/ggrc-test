'''
Created on Jun 19, 2013

@author: diana.tzinov
'''

from unittest import TestCase
from selenium import webdriver
from testcase import WebDriverTestCase
import unittest, time, re, os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.command import Command
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException




class WebdriverUtilities(object):


    def __inti__(self):
        pass
    
    def setDriver(self, driver):
        self.driver = driver

    def openBrowser(self, url):
        self.driver.get(url)
    
    def hoverOver(self, element):
        elem = self.driver.find_element_by_xpath(element)
        hov = ActionChains(self.driver).move_to_element(elem)
        hov.perform()

    def moveMouse(self, element):
        self.mouse = webdriver.ActionChains(self.driver)
        element = self.driver.find_element_by_css_selector("span.drop-arrow")
        self.mouse.move_to_element(element).perform()
        # self.mouse.move_to_element(element).click().perform()
            
    def getTextFromXpathString(self, element):
        try:
            return self.driver.find_element_by_xpath(element).text
        except:
            print element + "  element not found "
            return False
            
            
    def getAttribute(self, element):
        try:
            return self.driver.find_element_by_xpath(element).get_attribute("href")
        except:
            print element + "  element not found "
            return False
           
    def getAnyAttribute(self, element, attribute):
        try:
            return self.driver.find_element_by_xpath(element).get_attribute(attribute)
        except:
            print element + "  element not found "
            return False

    def switchWindow(self):
        handles = self.driver.window_handles
        self.driver.switch_to_window(handles[1])
        
    def switchBackWindow(self):
        handles = self.driver.window_handles
        self.driver.switch_to_window(handles[0])
        
    def switch_to_active_element(self):
        active = self.driver.switch_to_active_element()
        active.click()
        return 
    
    def scroll(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
   
    def clickOnSimple(self, element):
        try:    
            # elem = self.driver.find_element_by_xpath(element)
            # self.driver.execute_script("return arguments[0].click();", elem)
            self.hoverOver(element)
            self.driver.find_element_by_xpath(element).click()
            time.sleep(1)
            return True
        except:
            print element + "  element not found "
            return False
        
    def clickOn(self, element):
        try:    
            # elem = self.driver.find_element_by_xpath(element)
            # self.driver.execute_script("return arguments[0].click();", elem)
            self.hoverOver(element)
            elem = self.driver.find_element_by_xpath(element)
            self.driver.execute_script("return arguments[0].click();", elem)
            return True
        except:
            print element + "  element not found "
            return False
        
           
   
    def clickOnSave(self, element):
        try:    
            # elem = self.driver.find_element_by_xpath(element)
            # self.driver.execute_script("return arguments[0].click();", elem)
            self.hoverOver(element)
            elem = self.driver.find_element_by_xpath(element)
            self.driver.execute_script("return arguments[0].click();", elem)
            return True
        except:
            print element + "  element not found "
            return False 
        
    def clickOnByTextLink(self, linkText):
        try:    
            elem = self.driver.find_element_by_link_text(linkText)
            self.driver.execute_script("return arguments[0].click();", elem)
            # self.driver.find_element_by_link_text(linkText).click()
            return True
        except:
            print linkText + "  element not found "
            return False
        
    def clickOnById(self, element):
        try:    
            elem = self.driver.find_element_by_id(element)
            self.driver.execute_script("return arguments[0].click();", elem)
            return True
        except:
            print element + "  element not found "
            return False
        
    # def typeIntoFrame(self, text):
    #    self.driver.findElement(By.CSS_SELECTOR("body")).sendKeys(text);
    
    
    def clickOnByName(self, element):
        try:    
            elem = self.driver.find_element_by_name(element)
            self.driver.execute_script("return arguments[0].click();", elem)
            return True
        except:
            print element + "  element not found "
            return False
        
    
       
    def clickOnAndWaitFor(self, element, something, timeout=20):
        try:
            # elem = self.driver.find_element_by_xpath(element)
            # self.driver.execute_script("return arguments[0].click();", elem)
            self.hoverOver(element)
            self.driver.find_element_by_xpath(element).click()  
            return True
        except:
            print "Could not find " + element + " to click on in clickOnAndWaitFor."
            return False
        try:
            # WebDriverWait(self.driver, timeout).until(lambda driver : self.driver.find_element_by_xpath(someting))
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, something)))
            return True
        except:
            print "Could not find target element " + something + " to wait for in clickOnAndWaitFor."
            return False
        
  
    def waitForElementToBePresent(self, element, timeout=50):
        try:
            WebDriverWait(self.driver, timeout).until(lambda driver : self.driver.find_element_by_xpath(element))
            return True
        except:
            print element + "  element NOT found "
            return False

    def waitForElementValueToBePresent(self, element, timeout=50):
        try:
            WebDriverWait(self.driver, timeout).until(lambda driver : self.driver.find_element_by_xpath(element).text <> "")
            return True
        except:
            print element + "  element NOT found "
            return False



    def waitForElementToBeClickable(self, element, timeout=50):
        try:
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((By.XPATH, element)))
            return True
        except:
            print element + "  element NOT found in waitForElementToBeClickable"
            return False
        
    def waitForElementToBeVisible(self, element, timeout=50):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, element)))
            return True
        except:
            print element + "  element NOT found in waitForElementToBeVisible"
            return False
        
         
    def waitForElementNotToBePresent(self, element, timeout=50):
        try:
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located((By.XPATH, element)))
            return True
        except:
            print "element " + element + "  still visible in waitForElementNotToBePresent"
            return False
        
    def clickOnAndWaitForNotPresent(self, element, someting, timeout=50):
        try:
            self.driver.find_element_by_xpath(element).click()
            return True  
        except:
            return False
        try:
            WebDriverWait(self.driver, timeout).until(lambda driver : self.isElementNotPresent(someting))
            return True
        except:
            print someting + "  element is still Found or timed out "
            return False
    
    def uploadFile(self, what, where):
        self.driver.find_element_by_xpath(where)
        self.driver.find_element_by_xpath(where).send_keys(what)
        
            
    def inputTextIntoField(self, what, where):
        # element = self.driver.find_element_by_xpath(where)
        # element.clear()
        # element.send_keys(what)
        # element.send_keys(Keys.ENTER)
        self.driver.find_element_by_xpath(where).clear()
        self.driver.find_element_by_xpath(where).send_keys(what)
        
    def inputTextIntoFieldAndPressEnter(self, what, where):
        self.driver.find_element_by_xpath(where).clear()
        self.driver.find_element_by_xpath(where).send_keys(what + Keys.TAB)
        self.driver.send_keys()
        # self.driver.find_element_by_xpath(where).send_keys(Keys.TAB)
     

    def switchToNewUrl(self, url):
        self.driver.get(url)
        
    def isElementPresent(self, element):
        try:
            self.driver.find_element_by_xpath(element)
            return True
        except:
            return False

    def isElementNotPresent(self, element):       
        try:
            self.driver.find_element_by_xpath(element)
            return False
        except:
            return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert.text
        finally: self.accept_next_alert = True
    
    def selectFromDropdownNew(self, where, what):
        try:  
            select = self.driver.find_element_by_xpath(where)
            select.click()
            # time.sleep(1)      
            for option in select.find_elements_by_tag_name('option'):
                if option.text == what:
                    option.click()
                    time.sleep(1)
                    return True
        except:
            print where + " dropdown not found or the value " + what + " is not in the dropdown "
            return False
    
    def selectFromDropdownUntilSelected(self, where, what):
        Select(self.driver.find_element_by_xpath(where)).select_by_visible_text(what)
    
    
    def getNumberOfOccurences(self, element):
        return len(self.driver.find_elements_by_xpath(element))

    def focus(self):
        try:
            self.driver.switch_to_default_content()
        except ValueError as e:
            time.sleep(2)
    
    def swithToAlert(self):
        try:
            print "in Alert"
            self.driver.switch_to_active_element()
        except:
            self.fail("cannot switch to the active window")
            time.sleep(2)

    def findElement(self, how, element):
        try:
            # self.assertTrue(self.driver.find_element(by=how, value=element), "no element found")
            element = self.driver.find_element(by=how, value=element)
            return element
        except:
            self.fail("element " + element + " not found")
            
    def find_text(self, text):
        try:
            self.assertTrue(self.driver.getPageSource().contains(text) <> None, "no element found")
            return text
        except:
            self.fail("element " + text + " not found")

    def press_key(self):
        self.driver.key_down(Keys.SPACE)
    
    def delete_all_cookies(self):    
        self.driver.delete_all_cookies()
        
        
    def typeIntoFrame(self, text, frame_element):
        self.driver.switch_to_frame(self.driver.find_element(By.XPATH, frame_element))
        # self.driver.execute_script("document.body.innerHTML = '<body>'")
        bodyofhtml = self.driver.switch_to_active_element()
        bodyofhtml.send_keys(text)
        self.driver.switch_to_default_content()
        
        
    def getTextFromFrame(self, frame_element):
        self.driver.switch_to_frame(self.driver.find_element(By.XPATH, frame_element))
        # self.driver.execute_script("document.body.innerHTML = '<body>'")
        bodyofhtml = self.driver.switch_to_active_element()
        # value = self.driver.find_element_by_xpath("/x:html/x:body").text
        value = bodyofhtml.text
        # print value
        self.driver.switch_to_default_content()
        return value

    def wait_for_page_to_load(self, time):
            self.driver.set_page_load_timeout(time)

    def refreshPage(self):
        self.driver.refresh()


