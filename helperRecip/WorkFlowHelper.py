'''
Created on May 26, 2014

@author: uduong
@description This class is created to hold all functions related to WorkFlow only.  Elements are also stored locally to the function that uses it.
It's unlikely that elements are used by others when you purposely write it for the specified function.  Also, when Elements and Helpers classes 
are getting bigger they become unmanageable.  

All public functions have "WF" as a post-fix to signify that the function is not from the parent class.

'''

from datetime import datetime
import time

from helperRecip.Helpers import Helpers, log_time

class WorkFlowHelper(Helpers):
    
    '''
    Any elements that are shared among the functions can go here
    '''

    startWorkflow_bt = '//button[@type="submit" and @href="#workflowStart"]'
    endWorkflow_bt = '//button[@type="submit" and @class="btn end-workflow"]'
    
    @log_time
    # objecName: Controls or Projects, etc.
    # relevantTo: Program
    def addObjectsWF(self, objectName, relevantTo, whatItem):
        add_object_lk = '//a[@href="#objectSelector" and @data-mapping="objects"]' 
        add_new_rule_lk = '//a[@id="addFilterRule"]'
        object_select_drdn = '//select[@id="objects_type"]' 
        add_selected_bt = '//a[@id="addSelected"]'
        relevantTo_drdn = '//div[@id="filters"]//select[@class="input-small"]'
        search_txtbx = '//div[@id="filters"]//select[@class="input-small"]/../div[@class="objective-selector"]//input'
        search_bt = '//a[@id="objectReview"]'
        total_count = '//div[@id="middle_column"]/section[@class="widget objectives objects_widget widget-active"]//span[@id="objectsCounter"]'
        # check the count first
        
        countBefore = self.util.getTextFromXpathString(total_count)
        print countBefore
        
        self.util.clickOn(add_object_lk)
        self.util.selectFromDropdownByValue(object_select_drdn, objectName)
        self.util.selectFromDropdownByValue(relevantTo_drdn, relevantTo)
        self.util.inputTextIntoField(whatItem, search_txtbx)
        self.util.clickOn(search_bt)
        
        # TODO no real data is shown so can't progress further
        
        self.util.clickOn(add_selected_bt)

        # wait before checking count
        time.sleep(1)
        countAfter = self.util.getTextFromXpathString(total_count)

        if countAfter > countBefore:
            return True
        else:
            return False

    @log_time
    # Return true if addTask succeed and not error out
    # If taskName is blank, it will auto assign a unique name, e.g, Task-auto + timestamp
    def addTaskWF(self, taskName="", selectAll=False): 
        add_task_lk = '//a[@href="#objectSelector" and @data-mapping="tasks"]' 
        checkboxAll_chbx = '//input[@id="objectAll"]'
        addSelected_bt = '//a[@id="addSelected"]'
        task_table = '//div[@id="objectSelector"]/div[@class="results"]//ul'

        if selectAll == True:
            self.util.clickOn(addSelected_bt)  # just click on the button
        else:
            self.util.clickOn(checkboxAll_chbx)  # it's checked by default so click to uncheck it

            count = self.util.countChildren(task_table) 
            print "DEBUG, count: " + count

            for x in range(2, count):
                xpath = task_table + '/li[' + x + ']//div[@class="tree-title-area"]/i'
                title = self.util.getTextFromXpathString(xpath)
                print "DEBUG, title: " + title
                if title == taskName:  # if found, click on the checkbox next to it
                    self.util.clickOn(task_table + '//input[@type="checkbox"]')  # check it
                    break  # get out
        
        self.util.clickOn(addSelected_bt)
        return True

    @log_time
    # Create a new task from a window popped up by "add task" and return the task name if in auto create mode
    # Pre-condition: the window must already be up
    # To test the Cancel feature, set save=False
    def createNewTaskWF(self, title="", detail_description, save=True):
        create_task_bt = '//a[@class="btn btn-add addTaskModal"]'
        summary_title_txtbx = '//input[@id="task-title"]'
        detail_txtbx = '//div[@id="newTask"]//textarea[@id="program_description"]'
        save_bt = '//a[@id="addTask"]' 
        cancel_bt = '//a[@id="addTask"]/../../../div/div/a[@data-dismiss="modal"]'

        if title == "":
            title = "Task-auto-" + self.getTimeId()

        self.util.clickOn(create_task_bt)
        self.util.inputTextIntoField(title, summary_title_txtbx)
        self.util.inputTextIntoField(detail_description, detail_txtbx)
        if save==True:
            self.util.clickOn(save_bt)
        else:
            self.util.clickOn(cancel_bt)
        return title

    @log_time
    # Return true if addPerson succeed and not error out
    def addPersonWF(self, personName="", selectAll=False):
        add_person_lk = '//a[@href="#objectSelector" and @data-mapping="person"]' 
        checkboxAll_chbx = '//input[@id="objectAll"]'
        addSelected_bt = '//a[@id="addSelected"]'
        task_table = '//div[@id="objectSelector"]/div[@class="results"]//ul'
        if selectAll == True:
            self.util.clickOn(addSelected_bt)  # just click on the button
        else:
            count = self.util.countChildren(task_table) 
            print "count: " + count
            
            for x in range(2, count):
                xpath = task_table + '/li[' + x + ']//div[@class="tree-title-area"]/i'
                title = self.util.getTextFromXpathString(xpath)
                print "title: " + title
                if title == personName:  # if found, click on the checkbox next to it
                    self.util.clickOn(task_table + '//input[@type="checkbox"]')  # check it
                    break  # get out
        self.util.clickOn(addSelected_bt)
        return True

    @log_time
    # Return true if addTaskGroup succeed and not error out
    # if you want to test the Cancel feature then set save=False
    # date format: "2014_05_27", for test purpose please use current date
    def addTaskGroupWF(self, groupName, personName, date, save=True):
        group_txtbx = '//input[@id="new_object_name"]'
        search_txtbox = '//input[@id="new_object_name"]'
        save_bt = '//a[@id="addTaskGroup"]'
        cancel_bt = '//a[@id="cancelTaskGroup"]'
        calendar_picker = '//input[@id="tg_end_date"]'
        month_label = '//div[@id="ui-datepicker-div"]//span[@class="ui-datepicker-month"]'
        year_label = '//div[@id="ui-datepicker-div"]//span[@class="ui-datepicker-year"]'
        date_table = '//table[@class="ui-datepicker-calendar"]/tbody'

        self.util.inputTextIntoField(groupName, group_txtbx)
        self.util.inputTextIntoField(personName, search_txtbox)
        
        if save == True:
            self.util.clickOn(save_bt)
        else:
            self.util.clickOn(cancel_bt)

        day = str(datetime.now())
        
        day = day[8:10]
        
        # dateTable = WebElement(self.driver.findElement(By.TAG_NAME("table")));
        # List<WebElement> tableRows = yourTable.findElements(By.TAG_NAME("tr"));
        
        # just pick the current day from the day table        
        for row in range (1, 5):
            for column in range (1, 7):
                xpath = str(date_table + '/tr[' + row + ']/td[' + column + ']/a')
                theDay = self.util.clickOn(xpath)
                if (day == theDay):
                    self.util.clickOn(xpath)
                    break  # inner loop
                else:
                    continue;

            break  # outer loop

        return True

    @log_time
    def startWorkFlowWF(self, proceed=True):       
        proceed_bt = '//a[@id="confirmStartWorkflow"]'
        cancel_bt = '//a[@id="cancelStartWorkflow"]'
        self.util.clickOn(self.startWorkflow_bt)
        time.sleep(.5)
        if proceed == True:
            self.util.clickOn(proceed_bt)
        else:
            self.util.clickOn(cancel_bt)

    @log_time
    # prerequisite: Already have "Workflow"menu open
    def stopWorkFlowWF(self):
        self.util.clickOn(self.endWorkflow_bt)
        
    ### NOTE:     searchObjectInWidgetPanelWF vs.  searchObjectInAddObjectToWorkflowWind ###
    ###           widget panel is next to inner nav  ###    
        
    @log_time
    # Search for an object in the table.  Return TRUE if found and FALSE otherwise.
    def searchObjectInWidgetPanelWF(self, title, expandItIfFound=False):

        count = self._workflowObjectCount()
        for index in range [1:count]:
            xpath = '//div[@id="filters"]/ul[1]/li[' + index + ']//div[@class="tree-title-area"]'
     
            titleText = self.util.getTextFromXpathString(xpath)
            
            if titleText == title:
                if expandItIfFound == True:
                    self.util.clickOn(xpath)
                    
                return True
            else:
                return False
            
    @log_time
    # Search for the named object and ummap it
    # Return the current total number count of workflows 
    def _workflowObjectCount(self):
        count_str_unfiltered = '//span[@id="objectsCounter"]' 
        
        count_str_filtered = self.util.getTextFromXpathString(count_str_unfiltered)
        endix = count_str_filtered.index(']')
        
        count = count_str_unfiltered[1:endix]
        
        return count

    @log_time
    def unmapObjectsWF(self, objectName):
        # TODO add search by title in the future; call _searchStringInTable()
        unmap_lk = '//div[@id="middle_column"]//div[@class="tier-2-info item-content content-open"]//a[@class="info-action unmap pull-right"]'
        total_count_label = '//div[@id="middle_column"]/section[@class="widget entities people_widget widget-active"]//span[@class="object_count"]'
        count = self.util.getTextFromXpathString(total_count_label)
        first_item = '//div[@id="middle_column"]//section[@class="widget objectives objects_widget widget-active"]//li[@class="tree-item object-top" and @data-index="0"]'

        self.util.hoverOver(first_item)
        self.util.clickOn(first_item)
        self.util.clickOn(unmap_lk)

    @log_time
    def unmapTasksWF(self, taskName):
        # TODO add search by title in the future; call _searchStringInTable()
        unmap_lk = '//div[@id="middle_column"]//div[@class="tier-2-info item-content content-open"]//a[@class="info-action unmap pull-right"]'
        total_count_label = '//div[@id="middle_column"]/section[@class="widget entities people_widget widget-active"]//span[@class="object_count"]'
        count = self.util.getTextFromXpathString(total_count_label)
        first_item = '//div[@id="middle_column"]//section[@class="widget objectives objects_widget widget-active"]//li[@class="tree-item object-top" and @data-index="0"]'
        
        self.util.hoverOver(first_item)
        self.util.clickOn(first_item)
        self.util.clickOn(unmap_lk)

    @log_time
    # Unmap first item in the list -- from the top
    def unmapPersonWF(self, personName):
        # TODO add search by title in the future; call _searchStringInTable()
        
        firstItem = '//div[@id="middle_column"]/section[@class="widget entities people_widget widget-active"]//span[@class="person-holder"]'
        unmap_lk = '//div[@id="middle_column"]//a[@class="info-action unmap pull-right"]'
        total_count_label = '//div[@id="middle_column"]/section[@class="widget entities people_widget widget-active"]//span[@class="object_count"]'
        count = self.util.getTextFromXpathString(total_count_label)

        self.util.hoverOver(firstItem)
        self.util.clickOn(firstItem)
        self.util.clickOn(unmap_lk)

    # Search for a specified text int the table, and return TRUE if found
    def _searchStringInTable(self, element, searchName, tableSize):
        
        for x in range[1:tableSize]:
            name = self.util.getTextFromXpathString(element)
            
            if name==searchName:
                return True
            else:
                continue

    @log_time
    # Unmap first item in the list -- from the top
    def deleteTaskGroupWF(self, groupName):        
        # TODO add search by title in the future
        count_xpath = '//div[@id="middle_column"]/section[@class="widget programs task_groups_widget widget-active"]//h2'
        title = '//div[@id="middle_column"]/section[@class="widget programs task_groups_widget widget-active"]//div[@class="tree-title-area"]'
        trash_icon = '//span[@class="counter removeTaskGroup"]/i'
        
        countBefore = self.util.getTextFromXpathString(count_xpath)
        # TODO Need to parse out the counter

        self.util.clickOn(trash_icon)
        time.sleep(1)

        if self.util.getTextFromXpathString(count_xpath) == countBefore-1:
            return True
        else:
            return False

    @log_time
    # Navigate inner panel on WorkFlow, e.g., Objects, Task Groups
    def navigateToMenuItemWF(self, fromWhatWorkflow, menuItem):
        workflow_menu  = '//li[@class="programs accordion-group workflow-group"]'
        workflow_items = '//li[@class="programs accordion-group workflow-group"]/ul[@class="sub-level"]/li[INDEX]//span'
        count_xpath = '//li[@class="programs accordion-group workflow-group"]//span[@class="item-count"]'

        self.util.clickOn(workflow_menu) # click on WorkFlow to expand it

        count = self.util.getTextFromXpathString(count_xpath)

        for x in count:
            label_text = self.util.getTextFromXpathString(workflow_items.replace("INDEX", x)) # click on WorkFlow to expand it
            
            if fromWhatWorkflow==label_text:
                self.util.clickOn(workflow_items.replace("INDEX", x))
                break
            else:
                continue

    @log_time
    # Return true if a named workflow exists, otherwise return false
    def doesWorkflowExist(self, wfName):
        workflow_menu  = '//li[@class="programs accordion-group workflow-group"]'
        workflow_items = '//li[@class="programs accordion-group workflow-group"]/ul[@class="sub-level"]/li[INDEX]//span'
        count_xpath = '//li[@class="programs accordion-group workflow-group"]//span[@class="item-count"]'

        self.util.clickOn(workflow_menu) # click on WorkFlow to expand it

        count = self.util.getTextFromXpathString(count_xpath)

        for x in count:
            label_text = self.util.getTextFromXpathString(workflow_items.replace("INDEX", x)) # click on WorkFlow to expand it
            
            if wfName==label_text:
                return True
            else:
                continue
        return False

    @log_time
    # Create a new work flow
    # If wfName is blank, it automatically create WF-auto + a timestamp, and return it
    def createWorkflow(self, wfName="", owner="", theFrequency):
        # TODO include more elements testing to support regression automation

        workflow_menu_lk  = '//li[@class="programs accordion-group workflow-group"]'
        workflow_items_lk = '//li[@class="programs accordion-group workflow-group"]/ul[@class="sub-level"]/li[INDEX]//span'
        wf_create_new_lk = '//li[@class="programs accordion-group workflow-group"]//li[@class="add-new"]'
        frequency_drdn = '//select[@id="frequency"]'
        
        title_txtbx = '//div[@id="editAssessmentStandAlone"]//input[@class="input-block-level required"]'
        owner_txtbx = '//div[@id="editAssessmentStandAlone"]//input[@name="lead_email"]'
        save_bt = '//a[@id="saveAssessment"]'

        if (wfName == ""):
            wfName = "WF-auto-" + self.getTimeId()

        self.selectCreateNew()

        self.util.waitForElementToBePresent(title_txtbx, 8)
        self.util.inputTextIntoField(wfName, title_txtbx)
        self.util.inputTextIntoField(owner, owner_txtbx)
        self.util.selectFromDropdownByValue(frequency_drdn, theFrequency)
        self.util.clickOn(save_bt)
        time.sleep(2)
        
        return wfName

    #click on Create New (Workflow) link
    def selectCreateNewWF(self):
        wf_create_new_lk = '//li[@class="programs accordion-group workflow-group"]//li[@class="add-new"]'

    #click on Create New (Task) link 
    def pressCreateNewTaskLinkWF(self):
        expandTask_lhs = '//....'
        wf_create_new_lk = '//li[@class="programs accordion-group workflow-group"]//li[@class="add-new"]'      
      
        self.util.clickOn(expandTask_lhs)
        self.util.waitForElementToBeClickable(wf_create_new_lk, 5)
      
      
    def selectAWorkflowWF(self, workflowName):
        workflow_items_lk = '//li[@class="programs accordion-group workflow-group"]/ul[@class="sub-level"]/li[INDEX]//span'
             
        for index in range[1:self.workflowCountOnHLS()]:
            str =  self.util.getTextFromXpathString(workflow_items_lk.replace("INDEX", index))
            if str == workflowName:
                self.util.clickOn(workflow_items_lk.replace("INDEX", index))
       
    def countWorkflowOnHLS(self):   
       wf_count = '//li[@class="programs accordion-group workflow-group"]/a/small/span'

       return  self.util.getTextFromXpathString(wf_count)

    @log_time
    # Already in WorkFlow window, just want to select different menu item, e.g., Workflow Info, or Task Groups
    def selectInnerNavMenuItemWF(self, menuItem):
        ul_menu = '//ul[@class="nav internav innernav-arrow program cms_controllers_inner_nav ui-sortable workflow-nav"]'
        li_WorkflowInfo = ul_menu + '/li[1]'
        li_Objects = ul_menu + '/li[2]'
        li_Tasks = ul_menu + '/li[2]'
        li_People = ul_menu + '/li[2]'
        li_TaskGroups = ul_menu + '/li[2]'
        li_History = ul_menu + '/li[@class="history_object"]'
        li_CurrentCycle = ul_menu + '/li[@class="progress-object  finished"]'

        if menuItem == "Workflow Info":
            self.util.clickOn(li_WorkflowInfo)
        elif menuItem == "Objects":
            self.util.clickOn(li_Objects)
        elif menuItem == "Tasks":
            self.util.clickOn(li_Tasks)
        elif menuItem == "People":
            self.util.clickOn(li_People)
        elif menuItem == "Task Groups":
            self.util.clickOn(li_TaskGroups)
        elif menuItem == "History":
            self.util.clickOn(li_History)
        elif menuItem == "Current Cycle":
            self.util.clickOn(li_CurrentCycle)

    @log_time
    # Edit a specified workflow
    def editWorkflowWF(self, workflowName, title="", owner="", save=True):
        edit_lk = '//div[@id="middle_column"]//a[@href="#editAssessmentStandAlone" and @title="Edit"]'
        my_title = '//div[@id="editAssessmentStandAlone"]//input[@name="title"]'
        my_owner = '//div[@id="editAssessmentStandAlone"]//input[@name="lead_email"]' 
        cancel_bt = '//div[@id="editAssessmentStandAlone"]//div[@class="deny-buttons"]/a'
        save_bt = '//a[@id="saveAssessment"]'

        self.navigateToMenuItemWF(workflowName, "Work Info")
        self.util.clickOn(edit_lk)
        self.util.waitForElementToBePresent(my_title, 8)

        self.util.inputTextIntoField(title, my_title)
        self.util.inputTextIntoField(owner, my_owner)

        # TODO add more other fields to support regression automation

        if save==True:
            self.util.clickOn(save_bt)
        else:
            self.util.clickOn(cancel_bt)

    @log_time
    # Clone a specified workflow
    def cloneWorkflowWF(self, workflowName, title="", owner="", save=True, copyTask=True, copyPeople=True, copyObjects=True, copyTaskGroup=True):
        self.navigateToMenuItemWF(workflowName, "Work Info")
        self._cloneWorkflow(title, owner, save, copyTask, copyPeople, copyObjects, copyTaskGroup)

    # Expand more link and click on Clone Workflow button
    def _cloneWorkflowWF(self, title="", owner="", save=True, copyTask=True, copyPeople=True, copyObjects=True, copyTaskGroup=True):
        more_lk = '//a[@class="dropdown-toggle info-edit"]'
        clone_workflow_bt = '//a[@href="#cloneWorkflow"]'
        cancel_bt = '//div[@id="cloneWorkflow"]//div[@class="deny-buttons"]/a'
        save_bt = '//a[@id="cloneWorkflowSave"]'

        myTitle = '//div[@id="cloneWorkflow"]//input[@name="title"]'
        myOwner = '//div[@id="cloneWorkflow"]//input[@name="lead_email"]'

        self.util.clickOn(more_lk)
        self.util.clickOn(clone_workflow_bt)
        self.util.waitForElementToBePresent(myTitle, 5)

        if (title != ""):
            self.util.inputTextIntoField(title, myTitle)

        if (owner != ""):
            self.util.inputTextIntoField(owner, myOwner)

        # by default, all checkboxes are checked
        if copyTask==False:
            self.util.clickOn('//div[@id="cloneWorkflow"]//label[1]/input[@type="checkbox"]')
        elif copyPeople==False:
            self.util.clickOn('//div[@id="cloneWorkflow"]//label[2]/input[@type="checkbox"]')
        elif copyObjects==False:
            self.util.clickOn('//div[@id="cloneWorkflow"]//label[3]/input[@type="checkbox"]')
        elif copyTaskGroup==False:
            self.util.clickOn('//div[@id="cloneWorkflow"]//label[4]/input[@type="checkbox"]')

        if save==False:
            self.util.clickOn(cancel_bt)
        else:
            self.util.clickOn(save_bt)

    @log_time
    # Prerequisite:  Add objects to workflow window is already up.  Add New Rule link is already there
    # Set add=False, to test the Cancel feature
    def addNewRule(self, object_type, relevantTo, searchItem, add=True, selectAll=False):
        select_all_drdn = '//select[@id="objects_type"]'
        add_new_rule_lk = '//a[@id="addFilterRule"]'
        relevant_to_drdn = '//div[@id="objectSelector"]//div[@class="indent-row"]//select'
        search_txtbx = '//div[@class="objective-selector"]//input[@class="input-large search-icon"]'
        search_bt = '//a[@id="objectReview"]'
        add_selected_bt = '//a[@id="addSelected"]'
        cancel_bt = '//div[@id="objectSelector"]//div[@class="deny-buttons"]'
        task_table = '//div[@class="tree-title-area"]/span/strong'

        self.util.selectFromDropdownByValue(select_all_drdn, object_type)
        self.util.clickOn(add_new_rule_lk)
        self.util.selectFromDropdownByValue(relevant_to_drdn, relevantTo)
        self.util.inputTextIntoField(searchItem, search_txtbx)

        self.util.clickOn(search_bt)

        if selectAll == True:
            self.util.clickOn(add_selected_bt)  # just click on the button
        else:
            count = self.util.countChildren(task_table) 
            idex = count.index(' ')
            count = count[0:idex]

            print "count: " + count

            for x in range(2, count):
                xpath = task_table + '/li[' + x + ']//div[@class="tree-title-area"]/i'
                title = self.util.getTextFromXpathString(xpath)
                print "title: " + title
                if title == searchItem:  # if found, click on the checkbox next to it
                    self.util.clickOn(task_table + '//input[@type="checkbox"]')  # check it
                    break  # get out

        if add==True:
            self.util.clickOn(add_selected_bt)
        else:
            self.util.clickOn(cancel_bt)

    @log_time
    # End the current cycle.  
    def endCycle(self):
        # select Current Cycle -> End Cycle
        end_cycle_bt = '//button[@class="btn end-cycle"]'

        self.selectInnerNavMenuItemWF("Current Cycle")
        self.util.waitForElementToBePresent(end_cycle_bt, 8)
        self.util.clickOn(end_cycle_bt)

    @log_time
    # Count the total of Objects in WF and return the number.
    # If count is messed up, just return 911
    def countObjectsWF(self): 
        cnt_xpath_from_widget = '//span[@id="objectsCounter"]'
        cnt_xpath_from_innerNav = '//span[@id="objectsMainCounter"]'

        count_from_innerNav = self.util.getTextFromXpathString(cnt_xpath_from_innerNav) # count
        count_from_widget = str(self.util.getTextFromXpathString(cnt_xpath_from_widget)) # (count); filter out parenthesis
        index = count_from_widget.index(")")
        count_from_widget = count_from_widget[1:index]

        if count_from_innerNav == count_from_widget:
            return count_from_innerNav
        else:
            return 911
