import time
import unittest

from helperRecip.Elements import Elements
from helperRecip.Helpers import Helpers
from helperRecip.WebdriverUtilities import WebdriverUtilities
from helperRecip.WorkFlowHelper import WorkFlowHelper
from helperRecip.testcase import *


class WorkflowSmokeTest(WebDriverTestCase):
       
    def testWorkflowSmokeTest(self):
        self.testname="TestWorkflowSmokeTest"
        self.setup()
        util = WebdriverUtilities()
        util.setDriver(self.driver)
        element = Elements()
        do = WorkFlowHelper(self)
        do.setUtils(util)
        do.login()

        print "TEST THAT YOU CAN CREATE A WORKFLOW" 
        myWorkflow_1 = do.createWorkflow("", "uduong@google.com") #wf is not blank after created successfully
        self.assertNotEqual(myWorkflow_1, "", "Failed creating a work flow 1 .")
        
        myWorkflow_2 = do.createWorkflow("", "uduong@google.com") #wf is not blank after created successfully
        self.assertNotEqual(myWorkflow_2, "", "Failed creating a work flow 2.")

        print "TEST THAT YOU CAN SELECT A WORKFLOW"
        do.selectAWorkflowWF(myWorkflow_1)
        
        do.selectInnerNavMenuItemWF("Objects")
        
        print "TEST THAT YOU CAN CREATE OBJECT"
        countBefore = do.countObjectsWF("Objects")
        self.assertTrue(do.addObjectsWF("Controls", "Program", "Secure Backups"), "Failed to add a Workflow object.")
        countAfter = do.countObjectsWF("Objects")
        self.assertTrue(do.searchObjectInWidgetPanelWF("Secure Backups", False), "Object is not found in the widget panel.")
        self.assertEqual(countBefore + 1, countAfter, "Object count is messed up.")
        
        
        # TEST THAT YOU CAN CREATE TASK
        do.pressCreateNewTaskLinkWF()        
        new_task_name = do.createNewTaskWF("", "This is task is auto created.", True)
        
        do.selectInnerNavMenuItemWF("Tasks")
        
        # TEST THAT YOU CAN ADD TASK
        do.addTaskWF(new_task_name, True)
        
        do.selectInnerNavMenuItemWF("People")
        
        # TEST THAT YOU CAN ADD PEOPLE
        self.assertTrue(do.addPersonWF("", True), "Failed to create a person.")
        
        do.selectInnerNavMenuItemWF("Task Groups")
        # TEST THAT YOU CAN CREATE A TASK GROUP
        do.addTaskGroupWF("", "Dan Ring", time.date.now(), True)
        
        # TEST CLONING A WORKFLOW
        countBefore = do.countWorkflowOnHLS()
        do.selectInnerNavMenuItemWF("Workflow Info")
        do.cloneWorkflowWF(myWorkflow_1, "Clone It", "uduong") # name must be valid on Google network
        countAfter = do.countWorkflowOnHLS()
        self.assertEqual(countBefore + 1, countAfter, "Count of workflow is not incrementing correctly.")
        self.assertTrue(do.doesWorkflowExist("Clone It"), "Clone It nof found in the LHS")
        
        
        
        

        
        
        
        
        
        
        
        
        
        
        
        
        


        
       
        
        
        
if __name__ == "__main__":
    unittest.main()
 