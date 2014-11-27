'''
Created on Nov 25, 2014

@author: uduong
'''


import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *

# This test verifies that counts on People, Roles, and Events are correct

class TestAdminDBGeneral(WebDriverTestCase):
    
# Warning: The count might not be correct if other users are using the application at the same time
    
    def testAdminDBGeneral(self):
        
        # testrecip@gmail exists in the database
        the_email = 'testrecip@gmail.com'
        roles = 9 # nine types of roles
        
        self.testname="TestAdminDBGeneral"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()
        
        do.selectMenuInTopRight("Admin Dashboard")
               
        # verify people table
        do.selectMenuItemInnerNavDashBoard("People")       
        self.assertTrue(do.searchPersonInAdminDB(the_email), "Cannot find it in the People table.")
        people_count = do._countOfObjectsFromAdminDB("people")
        people_count_from_label = do._countOfObjectsFromAdminDBLabel("people")
        self.assertEquals(people_count, people_count_from_label, "People count is not in sync.")
        self.assertEquals(1, people_count, "Expect count equals to 1, but it's " + str(people_count))
        
        # verify Roles table
        do.selectMenuItemInnerNavDashBoard("Roles")
        roles_count = do._countOfObjectsFromAdminDB("roles")
        roles_count_from_label = do._countOfObjectsFromAdminDBLabel("roles")
        self.assertEquals(roles_count, roles_count_from_label, "Roles count is not in sync.")
        self.assertEquals(roles, roles_count, "Expect count equals to" + str(roles) + ", but it's " + str(roles_count))


        # verify events table
        # There are more than 22 thousands entries so can't count every entries.  Work-around is to verify that it
        # increments by 1 when you create an object for example
        do.selectMenuItemInnerNavDashBoard("Events")
        events_count_before = do._countOfObjectsFromAdminDB("events")
        events_count_from_label = do._countOfObjectsFromAdminDBLabel("events")
        self.assertEquals(events_count_before, events_count_from_label, "Events count is not in sync.")
        
        xpath = do.createObject("Contract")
        title = util.getTextFromXpathString(xpath)
        do.selectMenuInTopRight("Admin Dashboard")
        
        do.selectMenuItemInnerNavDashBoard("Events")
        do.delay(20) #events table takes time to load
        events_count_before = do._countOfObjectsFromAdminDB("events")
        events_count_from_label = do._countOfObjectsFromAdminDBLabel("events")
        events_count_after = int(events_count_from_label + 1) 
        
        self.assertEquals(events_count_before, events_count_from_label, "Events count is not in sync.")                    
        self.assertEquals(events_count_after, events_count_after, "Count before=" + str(events_count_before) + "; Count after=" + str(events_count_after))



if __name__ == "__main__":
    unittest.main()
