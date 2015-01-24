'''
Created on Jan 21, 2015

Description:   System-wide reader role cannot see private program unless he is added to that private program and assigned permission.

@author: uduong
'''

import time
import unittest
import unittest

from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestNoAccessRole(WebDriverTestCase):
    
    
    def testNoAccessRole(self):
        self.testname="TestNoAccessRole"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()

        email = config.reader1
        reader = config.reader2
        password = config.same_password
        title = "Auto_Private_" + do.getTimeId() + str(do.getRandomNumber())

        do.createObject("Program", title, "checked")
        do.verifyObjectIsCreatedinLHN("Program", title)
        do.assertEqual(1, do.countOfAnyObjectLHS("Program"), "Expect count to be 1 but don't see it.")

        # now log out and then log in with the new account and try to create a program
        do.selectMenuInTopRight("Logout")
          
        # Refresh the page
        do.refresh()
          
        # Log in with new user
        do.login(reader, password)
        print "Log in as : " + do.whoAmI()
        do.uncheckMyWorkBox()
        
        try:
            do.verifyObjectIsCreatedinLHN("Program", title)
        except:
            do.assertEqual(0, do.countOfAnyObjectLHS("Program"), "Expect count to be 0 but don't see it.")
            print "Good...private program should not be visible to reader role unless permitted."

        
if __name__ == "__main__":
    unittest.main()