# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

from lib import base
from lib.element import lhn
from lib.constants import locator


class LhnMenu(base.Page):
    locators = locator.LhnMenu

    def __init__(self, *args, **kwargs):
        super(LhnMenu, self).__init__(*args, **kwargs)
        self._my_objects = base.Tab(self._driver, self.locators.MY_OBJECTS)
        self._all_objects = base.Tab(self._driver, self.locators.ALL_OBJECTS)

        self.programs = lhn.Programs(self._driver, self.locators.PROGRAMS)
        self.workflows = lhn.Workflows(self._driver, self.locators.WORKFLOWS)
        self.audits = lhn.Audits(self._driver, self.locators.AUDITS)
        self.control_assessments = lhn.ControlAssesments(
            self._driver, self.locators.CONTROL_ASSESSMENTS)
        self.requests = lhn.Requests(self._driver, self.locators.REQUESTS)
        self.issues = lhn.Issues(self._driver, self.locators.ISSUES)

        self.directives = lhn.Directives(self._driver, self.locators.DIRECTIVES)
        self.regulations = lhn.Regulations(self._driver,
                                           self.locators.REGULATIONS)
        self.policies = lhn.Policies(self._driver, self.locators.POLICIES)
        self.standards = lhn.Standards(self._driver, self.locators.STANDARDS)
        self.contracts = lhn.Contracts(self._driver, self.locators.CONTRACTS)
        self.clauses = lhn.Clauses(self._driver, self.locators.CLAUSES)
        self.sections = lhn.Sections(self._driver, self.locators.SECTIONS)

        self.controls_or_objectives = lhn.ControlsOrObjectives(
            self._driver, self.locators.CONTROLS_OR_OBJECTIVES)
        self.controls = lhn.Controls(self._driver, self.locators.CONTROL)
        self.objectives = lhn.Objectives(self._driver, self.locators.OBJECTIVES)

        self.people_or_groups = lhn.PeopleOrGroups(
            self._driver, self.locators.PEOPLE_OR_GROUPS)
        self.people = lhn.People(self._driver, self.locators.PEOPLE)
        self.org_groups = lhn.OrgGroups(self._driver, self.locators.ORG_GROUPS)
        self.vendoers = lhn.Vendors(self._driver, self.locators.VENDORS)

        self.access_groups = lhn.AccessGroups(self._driver,
                                              self.locators.ACCESS_GROUPS)

        self.assets_or_business = lhn.AssetsOrBusiness(
            self._driver, self.locators.ASSETS_OR_BUSINESS)
        self.systems = lhn.Systems(self._driver, self.locators.SYSTEMS)
        self.processes = lhn.Processes(self._driver, self.locators.PROCESSES)
        self.data_assets = lhn.DataAssets(self._driver,
                                          self.locators.DATA_ASSETS)
        self.products = lhn.Products(self._driver, self.locators.PRODUCTS)
        self.projects = lhn.Projects(self._driver, self.locators.PROJECTS)
        self.facilities = lhn.Facilities(self._driver, self.locators.FACILITIES)
        self.markets = lhn.Markets(self._driver, self.locators.MARKETS)

        self.risks_or_threats = lhn.RisksOrThreats(
            self._driver, self.locators.RISK_OR_THREATS)
        self.risks = lhn.Risks(self._driver, self.locators.RISKS)
        self.threats = lhn.Threats(self._driver, self.locators.THREATS)
        self._refresh_member_count()

    def _refresh_member_count(self):
        """Each dropdown in LHN has a count of members in brackets which we
        update."""
        self.programs_count = base.Label(self._driver,
                                         self.locators.PROGRAMS_COUNT)
        self.workflows_count = base.Label(self._driver,
                                          self.locators.WORKFLOWS_COUNT)
        self.audits_count = base.Label(self._driver,
                                       self.locators.AUDITS_COUNT)
        self.control_assessments_count = base.Label(
            self._driver, self.locators.CONTROL_ASSESSMENTS_COUNT)
        self.requests_count = base.Label(self._driver,
                                         self.locators.REQUESTS_COUNT)
        self.regulations_count = base.Label(self._driver,
                                            self.locators.REGULATIONS_COUNT)
        self.policies_count = base.Label(self._driver,
                                         self.locators.POLICIES_COUNT)
        self.issues_count = base.Label(self._driver,
                                       self.locators.ISSUES_COUNT)
        self.standards_count = base.Label(self._driver,
                                          self.locators.STANDARDS_COUNT)
        self.contracts_count = base.Label(self._driver,
                                          self.locators.CONTRACTS_COUNT)
        self.clauses_count = base.Label(self._driver,
                                        self.locators.CLAUSES_COUNT)
        self.sections_count = base.Label(self._driver,
                                         self.locators.SECTIONS_COUNT)
        self.controls_count = base.Label(self._driver,
                                         self.locators.CONTROL_COUNT)
        self.objectives_count = base.Label(self._driver,
                                           self.locators.OBJECTIVES_COUNT)
        self.people_count = base.Label(self._driver,
                                       self.locators.PEOPLE_COUNT)
        self.org_groups_count = base.Label(self._driver,
                                           self.locators.ORG_GROUPS_COUNT)
        self.vendors_count = base.Label(self._driver,
                                        self.locators.VENDORS_COUNT)
        self.access_groups_count = base.Label(self._driver,
                                              self.locators.ACCESS_GROUPS_COUNT)
        self.systems_count = base.Label(self._driver,
                                        self.locators.SYSTEMS_COUNT)
        self.processes_count = base.Label(self._driver,
                                          self.locators.PROCESSES_COUNT)
        self.data_assets_count = base.Label(self._driver,
                                            self.locators.DATA_ASSETS_COUNT)
        self.products_count = base.Label(self._driver,
                                         self.locators.PRODUCTS_COUNT)
        self.projects_count = base.Label(self._driver,
                                         self.locators.PROJECTS_COUNT)
        self.facilities_count = base.Label(self._driver,
                                           self.locators.FACILITIES_COUNT)
        self.markets_count = base.Label(self._driver,
                                        self.locators.MARKETS_COUNT)
        self.risks_count = base.Label(self._driver,
                                      self.locators.RISKS_COUNT)
        self.threats_count = base.Label(self._driver,
                                        self.locators.THREATS_COUNT)

    def select_my_objects(self):
        """In LHN selects the tab "My Objects" """
        self._my_objects.click()
        self._all_objects.is_activated = False
        self._refresh_member_count()

    def select_all_objects(self):
        """ In LHN selects the tab "All Objects" """
        self._all_objects.click()
        self._my_objects.is_activated = False
        self._refresh_member_count()


class HeaderPage(base.Page):
    def __init__(self, driver):
        super(HeaderPage, self).__init__(driver)
        self.lhn_menu = base.Button(self._driver, locator.PageHeader.BUTTON_LHN)

    def open_lhn_menu(self):
        """Opens LHN on the Dashboard

        Returns:
            LhnMenu
        """
        self.lhn_menu.click()
        return LhnMenu(self._driver)
