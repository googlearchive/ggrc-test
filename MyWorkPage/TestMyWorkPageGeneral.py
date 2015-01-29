'''
Created on Jan 26, 2015

Description:  This script test some general access such as tabs or navigation and help link after login in.

@author: uduong

'''
import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers


class TestMyWorkPageGeneral(WebDriverTestCase):
       
    def testMyWorkPageGeneral(self):
        self.testname="TestMyWorkPageGeneral"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()

        # open menu
        do.showLHMenu(True)
         
        # All and my object radio buttons exist?
        do.assertTrue(do.isMyObjectsOnlyPresent(), "My objects only radio button does not exist")
        do.assertTrue(do.isMyObjectsOnlyChecked(), "My objects only is not checked by default")
        
        # program, workflows, audits with count in the parenthesis
        my_program_count = do.countOfAnyObjectLHS("Program")
        isinstance(my_program_count, int)
        my_workflow_count = do.countOfAnyObjectLHS("Workflow")
        isinstance(my_workflow_count, int)        
        my_audit_count = do.countOfAnyObjectLHS("Audit")
        isinstance(my_audit_count, int)
        
        do.assertTrue(do.isAllObjectsPresent(), "All objects radio button does not exist")        
        do.assertFalse(do.isAllObjectsChecked(), "All objects is checked by default which is wrong")
        do.uncheckMyWorkBox() # select all radio
          
        # program, workflows, audits with count in the parenthesis should update and should be different than in the above
        all_program_count = do.countOfAnyObjectLHS("Program")
        isinstance(all_program_count, int)
        all_workflow_count = do.countOfAnyObjectLHS("Workflow")
        isinstance(all_workflow_count, int)        
        all_audit_count = do.countOfAnyObjectLHS("Audit")
        isinstance(all_audit_count, int)
        
        # counts are not updating; it's likely that there is a difference
        if my_program_count == all_program_count and \
           my_workflow_count == all_workflow_count and \
           my_audit_count == all_audit_count:
            do.assertTrue(False, "Counts are the same and are not likely updating.") #force output of error message
        
        # verify that objects created by different users show up
        do.verifyAllUsersObjectsShown("Program")
        
         
        # verify to each items in the LHS exist and labels are correct
        item_input = ['Program', 'Workflow', 'Audit', 'Regulation', 'Policy', 'Standard', 'Contract', 'Clause', 'Section', \
                     'Objective', 'Control', 'Person', 
                     'OrgGroup', 'Vendor', 'System', 'Process', 'DataAsset', 'Product', \
                     'Project', 'Facility', 'Market']
         
        expected   = ['Programs', 'Workflows', 'Audits', 'Regulations', 'Policies', 'Standards', 'Contracts', 'Clauses', 'Sections', \
                     'Objectives', 'Controls', 'People', 
                     'Org Groups', 'Vendors', 'Systems', 'Processes', 'Data Assets', 'Products', \
                     'Projects', 'Facilities', 'Markets']
         
        dictionary = dict(zip(item_input, expected))
        for object in item_input:
            raw = do.getItemLabelInLHS(object)
             
            if object == 'OrgGroup' or \
               object == 'DataAsset':
                Nth = 2
            else:
                Nth = 1
             
            filtered = do.getTextUpToNthSpace(raw, Nth)
            expected_text = dictionary.get(object)
            do.assertTrue(do.compareText(filtered, expected_text), "Mismatch text for object: " + filtered)
        
        # add help content and verify
        do.addHelpTitleContent("Help Me", "I will help you.")
        do.clickHelpTopRightCorner()
        do.assertEqual(do.getHelpTitle(), "Help Me", "Fail to get Help title.")
        #do.assertEqual(do.getHelpContent(), "I will help you.", "Fail to get Help content.")
        do.clickHelpDone()
        
        # click help icon, then click outside of modal
        do.clickHelpIcon()
        do.clickMyTasksIcon()

        # BUG: IF CONTENT IS EMPTY IT DOES NOT SAVE TO DATABASE EVENT IT SAYS SAVED

        




if __name__ == "__main__":
    unittest.main()







