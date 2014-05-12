'''
Created on May 20, 2014

@author: ukyo.duong
'''
import subprocess
import os.system
import os.popen
import popen2
import commands
import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.GRCObject import GRCObject
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.testcase import *


class TestArtyCreate(WebDriverTestCase):


                   

    def testArtyCreate(self):
        
        program_object = GRCObject 
        program_object.program_elements['title']="Program"
        program_object.program_elements['description']="This program is created by ARTY as part of the Load Performance Test"
               
        regulation_object = GRCObject 
        regulation_object.regulation_elements['title']="Regulation"  # regulation for Load Test
        regulation_object.regulation_elements['description']="This regulation is created by ARTY as part of the Load Performance Test"       
         
        system_object = GRCObject 
        system_object.system_elements['title']="System"  # system for Load Test
        system_object.system_elements['description']="This system is created by ARTY as part of the Load Performance Test"  
    
        
        
        
        
        
        subprocess.check_call("ls", "-la");
        
        
        
        self.testname="SmokeTest_Automation"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = Helpers(self)
        do.setUtils(util)
        do.login()
        
        
        do.createObjectIncrementingNaming(program_object, "Program")  # title=Program1; same for all
#         do.createObjectIncrementingNaming(program_object, "Regulation") 
#         do.createObjectIncrementingNaming(program_object, "System")    
#         do.createObjectIncrementingNaming(program_object, "People")  
#         do.createObjectIncrementingNaming(program_object, "Audit")  

        do.navigateToObjectAndOpenObjectEditWindow("Program","Program1")



    # verify that all tabs on left hand navigation exist
    def verifyAllObjectsOnLHN(self):
        object_left_nav_section_object_link = self.element.left_nav_expand_object_section_link.replace("OBJECT", "Program")














if __name__ == "__main__":
    unittest.main()
