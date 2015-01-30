'''
Created on Jan 26, 2015

PRE-REQUISITES:  There are at least 2 objects created by 2 different users for each object type.

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

        item_input = ['Program', 'Workflow', 'Audit', 'Regulation', 'Policy', 'Standard', 'Contract', 'Clause', 'Section', \
                     'Objective', 'Control', 'Person', 
                     'OrgGroup', 'Vendor', 'System', 'Process', 'DataAsset', 'Product', \
                     'Project', 'Facility', 'Market']


        # open menu
        do.showLHMenu(True)

        # All and my object radio buttons exist?
        do.assertTrue(do.isMyObjectsOnlyPresent(), "My objects only radio button does not exist")
        do.assertTrue(do.isMyObjectsOnlyChecked(), "My objects only is not checked by default")
        
        # get counts for each type of object
        my_list = []
        for object in item_input:
            count_my = do.countOfAnyObjectLHS(object)
            my_list.append(count_my)

        
        do.assertTrue(do.isAllObjectsPresent(), "All objects radio button does not exist")        
        do.assertFalse(do.isAllObjectsChecked(), "All objects is checked by default which is wrong")
        do.uncheckMyWorkBox() # select all radio
          
        # program, workflows, audits with count in the parenthesis should update and should be different than in the above
        # get counts for each type of object
        all_list = []
        for object in item_input:
            count_all = do.countOfAnyObjectLHS(object)
            all_list.append(count_all)
        
        # counts are not updating; it's likely that there is a difference

        count_updated = False
        total_items = len(item_input)
        for object_count in my_list:
            my_count = my_list.pop()
            all_count = all_list.pop()
            total_items = total_items - 1
            
            if not my_count == all_count:
                count_updated = True
                break # good, it updates
            else:
                if total_items == 0:
                    do.assertTrue(count_updated, "Count of objects do not update.  Error.")
                    
            
        
        # verify that objects created by different users show up; repeat for all different object type
        # PRE-REQUISITES:  There are at least 2 objects created by 2 different users for each object type
        print ("WARNING !!!")
        print ("PRE-REQUISITES:  There are at least 2 objects created by 2 different users for each object type")
        for object in item_input:
            do.verifyAllUsersObjectsShown(object)
        
         
        # verify to each items in the LHS exist and labels are correct
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







