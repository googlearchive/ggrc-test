'''
Created on Jul 15, 2014

@author: uduong
'''

import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *

class TestAddRoleInAdminDashboard(WebDriverTestCase):
    
    def testAddRoleInAdminDashboard(self):
        self.testname="TestAddRoleInAdminDashboard"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()
        
        theRole = "readingOnly"

        do.selectMenuInTopRight("Admin Dashboard")
        do.selectMenuItemInnerNavDashBoard("Roles") # on the roles selection
        count_before = do.roleCount()
        do.createRoleInAdminDB(theRole, "this role can read only")
        count_after = do.roleCount()
        self.assertEquals(count_after, count_before+1, "Role count has not incremented.")
        self.assertTrue(do.searchRoleInAdminDB(theRole), "readingOnly role not found")
        print ""
        print theRole + " has been created successfully."
        
        # TODO:  add delete role after create it
         
if __name__ == "__main__":
    unittest.main()
