# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com


class LandingPage(object):
    BUTTON_LOGIN = "Login"
    PROGRAM_INFO_TAB = "Program Info"


class PageHeader(object):
    # dropdown toggle
    PROPLE_LIST_WIDGET = "Admin Dashboard"


class LhnMenu(object):
    # create new program
    DATE_FORMATTING = "%d/%m/%Y"
    OBJECT_REVIEW = "Object Review"
    PRIVATE_PROGRAM = "Private Program"
    DESCRIPTION = "Description"
    NOTES = "Notes"
    MANAGER = "Manager"
    PROGRAM_URL = "Program URL"
    STATE = "State"
    PRIMARY_CONTACT = "Primary Contact"
    SECONDARY_CONTACT = "Secondary Contact"
    REFERENCE_URL = "Reference URL"
    CODE = "Code"
    EFFECTIVE_DATE = "Effective Date"
    STOP_DATE = "Stop Date"


class WidgetBar(object):
    # dropdown
    CLAUSES = "Clauses"
    CONTRACTS = "Contracts"
    DATA_ASSETS = "Data Assets"
    FACILITIES = "Facilities"
    MARKETS = "Markets"
    ORG_GROUPS = "Org Groups"
    POLICIES = "Policies"
    PROCESSES = "Processes"
    PRODUCTS = "Products"
    PROJECTS = "Projects"
    STANDARDS = "Standards"
    SYSTEMS = "Systems"
    VENDORS = "Vendors"
    THREAD_ACTORS = "Thread Actors"
    RISKS = "Risks"
    TASKS = "Tasks"


class WidgetProgramInfo(object):
    SUBMIT_FOR_REVIEW = "Submit For Review"

    # state in modal create new page
    DRAFT = "Draft"
    FINAL = "Final"
    EFFECTIVE = "Effective"
    INEFFECTIVE = "Ineffective"
    LAUNCHED = "Launched"
    NOT_LAUNCHED = "Not Launched"
    IN_SCOPE = "In Scope"
    NOT_IN_SCOPE = "Not in Scope"
    DEPRECATED = "Deprecated"

    # button settings dropdown elements
    EDIT_PROGRAM = "Edit Program"
    GET_PERMALINK = "Get permalink"
    DELETE = "Delete"
    BUTTON_SETTINGS_DROPDOWN_ITEMS = [EDIT_PROGRAM, GET_PERMALINK, DELETE]

    ALERT_LINK_COPIED = "Link has been copied to your clipboard."
