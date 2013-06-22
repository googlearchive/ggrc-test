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
    
    def Login(self,util):
        self.util.waitForElementToBePresent(self.element.login_button)
        self.util.clickOnAndWaitFor(self.element.login_button, self.element.gmail_password_textfield)
        self.util.inputTextIntoField(config.username, self.element.gmail_userid_textfield)
        self.util.inputTextIntoField(config.password, self.element.gmail_password_textfield)
        self.util.clickOnAndWaitFor(self.element.gmail_submit_credentials_button, self.element.dashboard_title)