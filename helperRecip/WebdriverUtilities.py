'''
Created on Jun 19, 2013

@author: diana.tzinov
'''

from lib2to3.pgen2 import driver
import sys
from unittest import TestCase
import unittest, time, re, os

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.command import Command
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from testcase import WebDriverTestCase


class WebdriverUtilities(unittest.TestCase):
    

    timeout_time=70 #App Engine guarantees result comes back within a minute

    #timeout_time=50

        
    def setDriver(self, driver):
        self.driver = driver

    def openBrowser(self, url):
        self.driver.get(url)
    
    def hoverOver(self, element):
        elem = self.driver.find_element_by_xpath(element)
        hov = ActionChains(self.driver).move_to_element(elem)
        hov.perform()

    def hoverOverAndWaitFor(self, hoverOverElement, waitForElement):
        self.assertTrue(self.waitForElementToBePresent(hoverOverElement),"ERROR inside hoverOverAndWaitFor(): can't see hoverOverElement "+hoverOverElement)
        hover = self.driver.find_element_by_xpath(hoverOverElement)
        hov = ActionChains(self.driver).move_to_element(hover)
        hov.perform()
        self.assertTrue(self.waitForElementToBeVisible(waitForElement),"ERROR inside hoverOverAndWaitFor(): can't see waitForElement "+waitForElement)
        #self.assertTrue(self.waitForElementToBePresent(waitForElement),"ERROR inside hoverOverAndWaitFor(): can't see waitForElement "+waitForElement)
        
            
    def getTextFromXpathString(self, element):
        try:
            return self.driver.find_element_by_xpath(element).text
        except:
            self.fail("ERROR: Element "+element + " not found in getTextFromXpathString")
    

           
    def getAnyAttribute(self, element, attribute):
        try:
            return self.driver.find_element_by_xpath(element).get_attribute(attribute)
        except:
            self.fail("ERROR: Element "+element + " not found in getAnyAttribute()")

        
    def switch_to_active_element(self):
        active = self.driver.switch_to_active_element()
        active.click()
        return 
    
    def scroll(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    def find_element_by_xpath(self,element):
        return self.driver.find_element_by_xpath(element)
        
    def clickOn(self, element):
        try:    
            retries=0
            while True:
                try:
                    #self.scrollIntoView(element)
                    self.hoverOver(element)
                    self.assertTrue(self.waitForElementToBePresent(element),"ERROR inside clickOn(): can't see element "+element)
                    WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.XPATH, element)))
                    WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH, element)))
                    elem = self.driver.find_element_by_xpath(element)
                    self.driver.execute_script("return arguments[0].click();", elem)
                    return True
                except StaleElementReferenceException:
                    if retries < 10:
                        retries+=1
                        print "Encountered StaleElementReferenceException, will try again, retries="+str(retries)
                        continue
                    else:
                        print "Maximum number of retries reached when dealing with StaleElementReferenceException"
                        raise StaleElementReferenceException
        except:
            print "clickOn(): Element "+element + " not found, stale or not clickable"
            self.print_exception_info()
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
            self.fail("ERROR: Element "+element + " not found in clickOnSave()")
            
            

    
       
    def clickOnAndWaitFor(self, element, something, timeout=timeout_time):
        try:
            # elem = self.driver.find_element_by_xpath(element)
            # self.driver.execute_script("return arguments[0].click();", elem)
            self.hoverOver(element)
            self.driver.find_element_by_xpath(element).click()  
            return True
        except:
            #self.driver.get_screenshot_as_file("clickOnFailinClikAndAndFor.png")
            self.fail("ERROR: Element to click on "+element + " not found in clickOnAndWaitFor()")    
        try:
            # WebDriverWait(self.driver, timeout).until(lambda driver : self.driver.find_element_by_xpath(someting))
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, something)))
            return True
        except: 
            #self.driver.get_screenshot_as_file("waitForFailinClikAndAndFor.png")
            self.fail("ERROR: Element to wait for "+something  + " not found in clickOnAndWaitFor()")
            
  
    def waitForElementToBePresent(self, element, timeout=timeout_time):
        try:
            WebDriverWait(self.driver, timeout).until(lambda driver : self.driver.find_element_by_xpath(element))
            return True
        except:
            #self.driver.get_screenshot_as_file("waitForElementPresentFail.png")
            print "ERROR: Element "+element + " not found in waitForElementToBePresent()"
            self.print_exception_info()
            return False

    def waitForElementValueToBePresent(self, element, timeout=timeout_time):
        try:
            WebDriverWait(self.driver, timeout).until(lambda driver : self.driver.find_element_by_xpath(element).text <> "")
            return True
        except:
            print "ERROR: Element "+element + " not found in waitForElementValueToBePresent()"
            self.print_exception_info()
            return False

    def waitForElementToBeClickable(self, element, timeout=timeout_time):
        try:
            self.assertTrue(self.waitForElementToBePresent(element),"ERROR inside waitForElementToBeClickable(): can't see element "+element)
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((By.XPATH, element)))
            return True
        except:
            self.print_exception_info()
            self.fail("ERROR: Element "+element + " not found or stale in waitForElementToBeClickable()")
            
    def waitForIframe(self, element, timeout=timeout_time):
        try:
            #self.assertTrue(self.waitForElementToBePresent(element),"ERROR inside waitForElementToBeClickable(): can't see element "+element)
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, element)))
            WebDriverWait(self.driver, timeout).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, element)))
            return True
        except:
            self.print_exception_info()
            self.fail("ERROR: Element "+element + " not found or stale in waitForElementToBeClickable()")
        
    def waitForElementToBeVisible(self, element, timeout=timeout_time):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, element)))
            return True
        except:
            self.fail("ERROR: Element "+element + " not found in waitForElementToBeVisible()")
         
    def waitForElementNotToBePresent(self, element, timeout=timeout_time):
        try:
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located((By.XPATH, element)))
            return True
        except:
            #self.driver.get_screenshot_as_file("stillVisibleElementFail.png")
            print "ERROR: Element "+element + " still visible in waitForElementNotToBePresent(), Save/Map Object takes too long"
            self.print_exception_info()
            return False
        
    def clickOnAndWaitForNotPresent(self, element, someting, timeout=timeout_time):
        try:
            self.driver.find_element_by_xpath(element).click()
            return True  
        except:
            self.fail("ERROR: Element "+element + " not found in clickOnAndWaitForNotPresent()")
        try:
            WebDriverWait(self.driver, timeout).until(lambda driver : not self.isElementPresent(someting))
            return True
        except:
            self.fail("ERROR: Element "+someting + " still visible in clickOnAndWaitForNotPresent()")

    def pressEnterKey(self, element):
        try:    
            retries=0
            while True:
                try:
                    self.driver.find_element_by_xpath(element).send_keys(Keys.RETURN)
                    return True
                except StaleElementReferenceException:
                    if retries < 10:
                        retries+=1
                        print "Encountered StaleElementReferenceException, will try again, retries="+str(retries)
                        continue
                    else:
                        print "Maximum number of retries reached when dealing with StaleElementReferenceException"
                        raise StaleElementReferenceException
        except:
            self.print_exception_info()
            self.fail("ERROR: Element "+element + " not found, stale or not clickable in method pressEnterKey()")
            return False
        
            
    def inputTextIntoField(self, what, where):
        try:    
            retries=0
            while True:
                try:
                    self.hoverOver(where)
                    self.assertTrue(self.waitForElementToBePresent(where),"ERROR inside inputTextIntoField(): can't see element where: "+where)
                    WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.XPATH, where)))
                    WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH, where)))
                    self.driver.find_element_by_xpath(where).clear()
                    self.driver.find_element_by_xpath(where).send_keys(what)
                    
                    return True
                except StaleElementReferenceException:
                    if retries < 10:
                        retries+=1
                        print "Encountered StaleElementReferenceException, will try again, retries="+str(retries)
                        continue
                    else:
                        print "Maximum number of retries reached when dealing with StaleElementReferenceException"
                        raise StaleElementReferenceException
        except:
            self.print_exception_info()
            self.fail("ERROR: Element "+where + " not found, stale or not clickable in method inputTextIntoField()")
            return False

    def isElementVisible(self, element):
        try:
            elem = self.driver.find_elements_by_xpath(element)
            return elem[0].is_displayed()
        except:
            return False

    def isElementPresent(self, element):
        try:
            self.driver.find_element_by_xpath(element)
            return True
        except:
            return False
            #self.fail("ERROR: Element "+element + " not found in isElementPresent()")

    def handleMultiSelect(self,s,e1,e2):
        el=self.driver.find_element_by_xpath(s)
        for option in el.find_elements_by_tag_name('option'):
            if option.text == 'testrecip':
                option.click() # select() in earlier versions of webdriver
            if option.text == 'silas@reciprocitylabs.com':
                option.click() # select() in earlier versions of webdriver
    
        
        #select=Select(self.driver.find_element_by_xpath(elem))
        #select.select_by_visible_text('testrecip')
        #select.select_by_visible_text('silas@reciprocitylabs.com')
        
        '''
        select=Select(self.driver.find_element_by_xpath(s))
        
        self.waitForElementToBePresent(e1)
        ee1=self.driver.find_element_by_xpath(e1)
        self.waitForElementToBePresent(e2)
        ee2=self.driver.find_element_by_xpath(e2)
        #time.sleep(4)
        #ac = ActionChains(self.driver)
        #ac.key_down(Keys.SHIFT).perform()
        
        self.shift_key_down()
        #ee1.click()
        select.select_by_visible_text('testrecip')
        #self.clickOn(e1)
        
        #ee2.click()
        select.select_by_visible_text('silas@reciprocitylabs.com')
        #self.clickOn(e2)
        
        self.shift_key_up()
        #ac.key_up(Keys.SHIFT).perform()
        '''
        
        
        
        #time.sleep(20)
       
    
    
    
    def selectFromDropdownUntilSelected(self, where, what):
        self.waitForElementToBePresent(where)
        Select(self.driver.find_element_by_xpath(where)).select_by_visible_text(what)
        
    def selectFromDropdownByValue(self, where, what):
        self.waitForElementToBePresent(where)
        Select(self.driver.find_element_by_xpath(where)).select_by_value(what)
    
    
    def getNumberOfOccurences(self, element):
        return len(self.driver.find_elements_by_xpath(element))

    def focus(self):
        try:
            self.driver.switch_to_default_content()
        except ValueError as e:
            pass


            
    def findText(self, text):
        try:
            self.assertTrue(self.driver.getPageSource().contains(text) <> None, "no element found")
            return text
        except:
            self.fail("ERROR: Element "+text + " not found in findText()")

    def press_key(self):
        self.driver.key_down(Keys.SPACE)
    
    def deleteAllCookies(self):    
        self.driver.deleteAllCookies()
        
        
    def typeIntoFrame(self, text, frame_element):
        self.driver.switch_to_frame(self.driver.find_element(By.XPATH, frame_element))
        bodyofhtml = self.driver.switch_to_active_element()
        bodyofhtml.clear()
        bodyofhtml.send_keys(text)
        self.driver.switch_to_default_content()
        
        
    def getTextFromFrame(self, frame_element):
        self.driver.switch_to_frame(self.driver.find_element(By.XPATH, frame_element))
        bodyofhtml = self.driver.switch_to_active_element()
        value = bodyofhtml.text
        self.driver.switch_to_default_content()
        return value

    def waitForPageToLoad(self, time):
            self.driver.set_page_load_timeout(time)

    def refreshPage(self):
        self.driver.refresh()
        
    def get_a_screen_shot(self, filename):
        self.driver.get_screenshot_as_file(filename)

    def runTest(self):
        pass
    
    def print_exception_info(self):
        print "Exception Type:", sys.exc_info()[0]
        print "Exception Value:", sys.exc_info()[1]
        print "Exception Traceback:", sys.exc_info()[2]
        
    def scrollIntoView(self, element):
        try:
            elem = self.driver.find_element_by_xpath(element)
            self.driver.execute_script( "arguments[0].scrollIntoView(true);", elem);
        except:
                print "  element is still Found or timed out "
                return False
            
    def inputTextIntoFieldAndPressEnter(self,what,where):
        self.driver.find_element_by_xpath(where).clear()
        self.driver.find_element_by_xpath(where).send_keys(what)
        self.driver.find_element_by_xpath(where).send_keys(Keys.RETURN)
        
    def uploadItem(self, what, where):
        print what
        self.waitForElementToBePresent(where)
        self.driver.find_element_by_xpath(where).send_keys(what)
        time.sleep(2)
        #self.waitForElementToBeVisible(element.upload_file_button)
        #util.find_element_by_xpath(element.upload_file_button).click() 
        #time.sleep(5)
        
    def switch_frame(self):
        #self.driver.switch_to_frame(frame_name)
        #self.driver.switch_to_frame(1)
        self.driver.switch_to_frame(self.driver.find_elements_by_tag_name("iframe")[1])
    
    def switch_google_doc_frame(self):
        #frame_element =self.driver.find_element_by_xpath('//iFrame[@class="picker-frame picker-dialog-frame"]') 
        #self.driver.switch_to_frame(frame_element)
        self.driver.switch_to_frame(self.driver.find_elements_by_tag_name("iframe")[3])
      
    
    def switchWindow(self):
        handles = self.driver.window_handles
        print handles
        self.driver.switch_to_window(handles[1])
        
    def switchBackWindow(self):
        handles = self.driver.window_handles
        self.driver.switch_to_window(handles[0])
        
                
    def max_screen(self):
        self.driver.maximize_window()
    
    def print_source(self):
        print self.driver.page_source
        
    def switchToNewUrl(self,url):
        self.driver.get(url)
        
    def backBrowser(self):
        self.driver.back()

    def double_click(self,element):
        double_click = ActionChains(self.driver).double_click(element)
        double_click.perform()
        
    def click_on_link_by_link_text(self, link_text):
        elem = self.driver.find_element_by_link_text(link_text) 
        self.driver.execute_script("return arguments[0].click();", elem)

    def scroll_to_the_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
    def move_mouse_over(self, element):
        elem = self.driver.find_element_by_xpath(element)
        mouse = ActionChains(self.driver)
        mouse.move_to_element(elem).perform()
        
    def shift_key_down(self):
        keysdown = ActionChains(self.driver)
        keysdown.key_down(Keys.SHIFT)
       
    def shift_key_up(self):
        keysdown = ActionChains(self.driver)
        keysdown.key_up(Keys.SHIFT)

    def tab_key_down(self):
        keysdown = ActionChains(self.driver)
        keysdown.key_down(Keys.TAB)
    
    def jsExecutor(self, the_dom):
        self.driver.execute_script(the_dom)
       
    def countChildren(self, element):
        count = self.driver.find_elements_by_xpath(element)
        return count


        