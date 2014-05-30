'''
Created on May 13, 2014

@author: ukyo.duong
'''


import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.GRCObject import GRCObject
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *
from time import strftime


class TestArtyCreate(WebDriverTestCase):

    

    def testArtyCreate(self):
        

               
        self.testname="TestArtyCreate"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()
        
        program_object = GRCObject 
        program_object.program_elements['title']="Program for Load Test" + do.getTimeId()
        program_object.program_elements['description']="This program is created by ARTY as part of the Load Performance Test"
               
        standard_object = GRCObject 
        standard_object.standard_elements['title']="Standard" + do.getTimeId() # Standard for Load Test
        standard_object.standard_elements['description']="This standard is created by ARTY as part of the Load Performance Test"       
         
        section_object = GRCObject 
        section_object.section_elements['title']="Section" + do.getTimeId() # Section for Load Test
        section_object.section_elements['description']="This section is created by ARTY as part of the Load Performance Test"  
        
        objective_object = GRCObject 
        objective_object.objective_elements['title']="Objective" + do.getTimeId() # Objective for Load Test
        objective_object.objective_elements['description']="This objective is created by ARTY as part of the Load Performance Test"  
        
        control_object = GRCObject 
        control_object.control_elements['title']="Control" + do.getTimeId() # Control for Load Test
        control_object.control_elements['description']="This control is created by ARTY as part of the Load Performance Test"  
        
        firstItemStandard = do.getFirstItemFromASection("Standard")
        
        # uncomment later
        do.createObjectIncrementingNaming(program_object, "Program", 1)     
        do.createObjectIncrementingNaming(standard_object, "Standard",1)  #case sensitive parameter & singularity
        
        
        
        # select "Standard1" created in the above is used in filling Section form
        do.createObjectIncrementingNaming(section_object, "Section", 25, firstItemStandard)  #case sensitive parameter & singularity
        do.createObjectIncrementingNaming(objective_object, "Objective", 125)
        do.createObjectIncrementingNaming(objective_object, "Control", 625)
       
        #do.navigateToWidget("Standard") # use singularity form
        #do.navigateToObjectWithSearch("pg1", "Program")
        #do.mapAObjectLHN("Standard")
        
        
        
        
        #do.mapAObjectWidget("Program", True,, 0)
        #do.navigateToObjectAndOpenObjectEditWindow("Program",last_created_object_link)
        #do.deleteObject()



if __name__ == "__main__":
    unittest.main()
