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


class Setup(WebDriverTestCase):

    
    def testProgramAuditSetup(self):
        self.testname="TestProgramAuditSetup"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        grcobject = GRCObject()
        do = Helpers()
        do.setUtils(util)
        do.login()
        objectiveID = {}
        
        # 1: Create New Program 
        #program_name = "The Program for Auto Test of Audit"  
        #temporary to use one program with unique name
        current_time = do.getTimeId()

        program_name = "Program for Auto Test of Audit"  +current_time
        
        last_created_object_link = do.createObject("Program", program_name, "checked",True, config.username)
        #object_name = str(util.getTextFromXpathString(last_created_object_link)).strip() 
        
        # 2.  Navigate to that Program page
        #do.navigateToObjectWithSearch(program_name,"Program")
        do.navigateToObject("Program",last_created_object_link)
        util.max_screen()
         
        # 3. Select Regulations tab in Object pg Nav to bring up the Mapped Regulations widget
        # 4. Click +Regulation button to bring up modal selector for mapping Regulation to the Program
        do.navigateToMappingWindowForObject("Regulation")
        
        # 5. In modal, click green +Regulation button to bring up create a new Regulation modal
        util.clickOn(element.mapping_modal_add_button)
        
        # 6.  Fill in title for the new Regulation, "Regulation for Auto Test of Audit"
        # 7.  click Save (this dismisses the 2nd modal and puts the newly created Regulation at the top of the list in the 1st modal (the mapping modal)
        regulation_name = "Regulation for Auto Test of Audit"+current_time
        do.createObject("Regulation", regulation_name,"unchecked",False)
        
        # 8.  Select "Regulation for Auto test of Audit" at top of list then click Map button (dismisses modal and returns to Program pg now with the Regulation mapped)
        mapped_object_id = do.mapFirstObject("Regulation",False,regulation_name)
        
        # 9.  Click on Regulation for Auto Test of Audit in Mapped Regulations widget to expand the drop down and reveal Sections list
        #expand regulation area
        mapped_object_link = element.mapped_object.replace("OBJECT", "regulation").replace("ID", mapped_object_id)
        util.waitForElementToBePresent(mapped_object_link)
        self.assertTrue(util.isElementPresent(mapped_object_link),"doesn't see the newly created mapped object")
        util.clickOn(mapped_object_link)
        
        # 10.  Hover over +Sections link to reveal 3 options, then click on Create Section to launch the Create new Section modal
        # 11.  New Section modal:Title: "Section 1 of Regulation for Auto Test of Audit"
        # 12. Click Save - returns you to the Program pg > Regulation widget > Section now shows in revealed Sections display area
        do.createSectionFor("regulation",mapped_object_id,"Section 1 of Regulation for Auto Test of Audit"+current_time)
        section_id= do.getTheIdOfTheLastCreated("section")
        # 13. Click on "Section 1 of Regulation for Auto Test of Audit" title in the Sections display area - this reveals the Text of Section we entered and the "OBJECTIVES, CONTROLS, AND BUSINESS OBJECTS (0)" display area.
        #expand section area
        util.waitForElementToBePresent(element.sections_area_first_section)
        self.assertTrue(util.isElementPresent(element.sections_area_first_section),"doesn't see the newly created Section in the section area")
        util.clickOn(element.sections_area_first_section)
        self.assertTrue(util.isElementPresent(element.theShortDescriptionElement),"doesn't see the short description element")
        #make objectiveID link visible
        util.waitForElementToBePresent(element.section_area_add_object_link)
        self.assertTrue(util.isElementPresent(element.section_area_add_object_link),"doesn't see +Objective link")
        
        # 16. Repeat steps  14-15 3 times, increment Objective name, leave the next bullet point in description
        util.max_screen()
        for n in range(3):
            print "objective number " + str(n+1)
            # 14.  Hover over +Object to reveal 2 options

            util.scrollIntoView(element.section_area_add_object_link)
            util.hoverOverAndWaitFor(element.section_area_add_object_link, element.section_area_add_objective_link)
            self.assertTrue(util.isElementPresent(element.section_area_add_objective_link),"doesn't see the section_area_add_objective_link")
            
            # 15.  Click on +Objectives to open "Map New Objective to Section 1 of Regulation for Auto Test of Audit" modal, input data and click Save
            #util.clickOn(element.section_area_add_object_link)
            util.clickOn( element.section_area_add_objective_link)
        
            
            
            #create new objective
            do.createObjectives(grcobject.objective_title[n], grcobject.objective_description[n])
            last_created_object_element = element.objective_elemet_in_the_inner_tree_with_index.replace("INDEX",str(n+1 ))
            print "the last created objective element is "+last_created_object_element
            util.waitForElementToBePresent(last_created_object_element)
            self.assertTrue(util.isElementPresent(last_created_object_element), "cannot see the newly created objective")
            # store objectiveID ids
            objective_id= do.getTheIdOfTheLastCreatedObjective(last_created_object_element)
            objectiveID[n]=objective_id
            print objectiveID[n]
           
            

    
        # 17.after creating 3 Objectives, Hover over +Object 1 more time but this time click on +Object to launch the multi object mapper modal 
        
        #util.clickOnAndWaitFor(element.section_area_add_object_link, element.section_area_add_objective_link)
        util.clickOn(element.section_area_add_object_link)
        
        # 18.  Select Controls from top filter selector in modal
        util.selectFromDropdownByValue(element.mapping_modal_top_filter_selector_dropdown, "Control")
        
        # 19.  Click green +Control button to create a new control
        
        util.clickOn(element.mapping_modal_add_button)
        
        # 20.  Give it the title "Control for Auto Test of Audit" - Click Save
        control_name = "Control for Auto Test of Audit" +current_time
        do.createObject("Control", control_name,"unchecked",False)
        mapped_object_id= do.mapFirstObject("Control", False,control_name)
        print mapped_object_id
        
        #
        # Write audit setup data to file - program_name and the 3 objective ids, each on separate line
        #
        
        f=open("audit_setup_data","w")
        f.write(program_name+"\n")
        f.write(objectiveID[0]+"\n")
        f.write(objectiveID[1]+"\n")
        f.write(objectiveID[2]+"\n")
        f.close()
        
       
        
if __name__ == "__main__":
    unittest.main()