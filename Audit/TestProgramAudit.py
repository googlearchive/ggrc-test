'''
Created on Oct 30, 2013

@author: diana.tzinov
'''
'''
Created on Sep 10, 2013

@author: diana.tzinov
'''




import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers
from helperRecip.GRCObject import GRCObject


class TestProgramAudit(WebDriverTestCase):

    
    def testProgramAudit(self):
        self.testname="TestProgramAudit"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        grcobject = GRCObject()
        do = Helpers()
        do.setUtils(util)
        do.login()
        
        # 1: Create New Program 
        program_name = "Program for Auto Test of Audit"  +do.getTimeId()
        last_created_object_link = do.createObject("Program", program_name, "checked",True, config.username)
        #object_name = str(util.getTextFromXpathString(last_created_object_link)).strip() 
        
        # 2.  Navigate to that Program page
        do.navigateToObject("Program",last_created_object_link)
         
        # 3. Select Regulations tab in Object pg Nav to bring up the Mapped Regulations widget
        # 4. Click +Regulation button to bring up modal selector for mapping Regulation to the Program
        do.navigateToMappingWindowForObject("Regulation")
        
        # 5. In modal, click green +Regulation button to bring up create a new Regulation modal
        util.clickOn(element.mapping_modal_add_button)
        
        # 6.  Fill in title for the new Regulation, "Regulation for Auto Test of Audit"
        # 7.  click Save (this dismisses the 2nd modal and puts the newly created Regulation at the top of the list in the 1st modal (the mapping modal)
        do.createObject("Regulation", "Regulation for Auto Test of Audit","unchecked",False)
        
        # 8.  Select "Regulation for Auto test of Audit" at top of list then click Map button (dismisses modal and returns to Program pg now with the Regulation mapped)
        mapped_object_id = do.mapFirstObject("Regulation")
        
        # 9.  Click on Regulation for Auto Test of Audit in Mapped Regulations widget to expand the drop down and reveal Sections list
        #expand regulation area
        mapped_object_link = element.mapped_object.replace("OBJECT", "regulation").replace("ID", mapped_object_id)
        util.clickOn(mapped_object_link)
        
        # 10.  Hover over +Sections link to reveal 3 options, then click on Create Section to launch the Create new Section modal
        # 11.  New Section modal:Title: "Section 1 of Regulation for Auto Test of Audit"
        # 12. Click Save - returns you to the Program pg > Regulation widget > Section now shows in revealed Sections display area
        do.createSectionFor("regulation",mapped_object_id,"Section 1 of Regulation for Auto Test of Audit")
        
        # 13. Click on "Section 1 of Regulation for Auto Test of Audit" title in the Sections display area - this reveals the Text of Section we entered and the "OBJECTIVES, CONTROLS, AND BUSINESS OBJECTS (0)" display area.
        #expand section area
        util.waitForElementToBePresent(element.sections_area_first_section)
        self.assertTrue(util.isElementPresent(element.sections_area_first_section),"doesn't see the newly created Section in the section area")
        util.clickOn(element.sections_area_first_section)
        #make objectives link visible
        util.waitForElementToBePresent(element.section_area_add_object_link)
        self.assertTrue(util.isElementPresent(element.section_area_add_object_link),"doesn't see +Objective link")
        
        # 16. Repeat steps  14-15 3 times, increment Objective name, leave the next bullet point in description
        
        for s in ["Objective 1 for Auto Test of Audit","Objective 2 for Auto Test of Audit","Objective 3 for Auto Test of Audit"]:
            # 14.  Hover over +Object to reveal 2 options
            util.hoverOverAndWaitFor(element.section_area_add_object_link, element.section_area_add_objective_link)
            
            # 15.  Click on +Objectives to open "Map New Objective to Section 1 of Regulation for Auto Test of Audit" modal, input data and click Save
            util.clickOn( element.section_area_add_objective_link)
        
            
            
            #create new objective
            do.createObject("Objective", s, "uncheckbox", False)
            
        
        # 17.after creating 3 Objectives, Hover over +Object 1 more time but this time click on +Object to launch the multi object mapper modal 
        
        #util.clickOnAndWaitFor(element.section_area_add_object_link, element.section_area_add_objective_link)
        util.clickOn(element.section_area_add_object_link)
        
        # 18.  Select Controls from top filter selector in modal
        util.selectFromDropdownByValue(element.mapping_modal_top_filter_selector_dropdown, "Control")
        
        # 19.  Click green +Control button to create a new control
        
        util.clickOn(element.mapping_modal_add_button)
        
        # 20.  Give it the title "Control for Auto Test of Audit" - Click Save
        
        do.createObject("Control", "Control for Auto Test of Audit","unchecked",False)
        
       
        
if __name__ == "__main__":
    unittest.main()