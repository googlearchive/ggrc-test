'''
Created on Jul 19, 2013

@author: diana.tzinov
'''



import unittest
import time
from helperRecip.testcase import *
from helperRecip.Elements import Elements
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.Helpers import Helpers
from helperRecip.GRCObject import GRCObject


class TestProgramEdit(WebDriverTestCase):

    
    def testProgramEdit(self):
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        grcobject = GRCObject()
        do = Helpers()
        do.setUtils(util)
        do.Login()
        self.assertTrue(util.isElementPresent(element.dashboard_title), "no dashboard page found")
        do.OpenCreateNewProgramWindow(element.programs_widget_add_program_button)
        random_number = str(time.time()).replace(".","")
        program_name = "program-auto-test"+random_number
        do.PopulateProgramData(program_name)
        link_to_the_object=do.VerifyObjectIsCreated("programs", program_name)
        do.NavToWidgetInfoPage(link_to_the_object)
        #do.WaitForLeftNavToLoad()
        do.OpenEditWindow()
        do.PopulateProgramInEditWindow( program_name)
        
        
        
if __name__ == "__main__":
    unittest.main()