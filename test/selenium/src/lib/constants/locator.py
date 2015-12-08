# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

from selenium.webdriver.common.by import By


class Login(object):
    BUTTON_LOGIN = (By.CSS_SELECTOR, "a.btn.btn-large.btn-info")


class PageHeader(object):
    BUTTON_LHN = (By.CSS_SELECTOR, ".lhn-trigger")

    # dropdown toggle
    PEOPLE_LIST_WIDGET = (By.CSS_SELECTOR,
                          '[href="/admin#people_list_widget"]')


class LhnMenu(object):
    LHN_MENU = (By.ID, "lhn")
    MODAL = (By.CSS_SELECTOR, '[id="ajax-modal-javascript:--"]')
    LHS_ITEM = (By.CSS_SELECTOR, '[test-data-id="lhs-item_3ad27b8b"]')
    ALL_OBJECTS = (By.CSS_SELECTOR, '[data-test-id="all_objects_e0345ec4"]')
    MY_OBJECTS = (By.CSS_SELECTOR, '[data-test-id="my_objects_6fa95ae1"]')

    # lhn items
    PROGRAMS = (By.CSS_SELECTOR, '[data-model-name="Program"]')
    WORKFLOWS = (By.CSS_SELECTOR, '[data-model-name="Workflow"]')
    AUDITS = (By.CSS_SELECTOR, '[data-model-name="Audit"]')
    CONTROL_ASSESSMENTS = (By.CSS_SELECTOR,
                           '[data-model-name="ControlAssessment"]')
    REQUESTS = (By.CSS_SELECTOR, '[data-model-name="Request"]')
    ISSUES = (By.CSS_SELECTOR, '[data-model-name="Issue"]')
    DIRECTIVES = (By.CSS_SELECTOR, '[data-test-id="directives_66116337"]')
    REGULATIONS = (By.CSS_SELECTOR, '[data-model-name="Regulation"]')
    POLICIES = (By.CSS_SELECTOR, '[data-model-name="Policy"]')
    STANDARDS = (By.CSS_SELECTOR, '[data-model-name="Standard"]')
    CONTRACTS = (By.CSS_SELECTOR, '[data-model-name="Contract"]')
    CLAUSES = (By.CSS_SELECTOR, '[data-model-name="Clause"]')
    SECTIONS = (By.CSS_SELECTOR, '[data-model-name="Section"]')
    CONTROLS_OR_OBJECTIVES = (By.CSS_SELECTOR,
                              '[data-test-id="controls/objectives_66116337"]')
    CONTROL = (By.CSS_SELECTOR, '[data-model-name="Control"]')
    OBJECTIVES = (By.CSS_SELECTOR, '[data-model-name="Objective"]')
    PEOPLE_OR_GROUPS = (By.CSS_SELECTOR,
                        '[data-test-id="people/groups_66116337"]')
    PEOPLE = (By.CSS_SELECTOR, '[data-model-name="Person"]')
    ORG_GROUPS = (By.CSS_SELECTOR, '[data-model-name="OrgGroup"]')
    ASSETS_OR_BUSINESS = (By.CSS_SELECTOR,
                          '[data-test-id="assets/business_66116337"]')
    SYSTEMS = (By.CSS_SELECTOR, '[data-model-name="System"]')
    PROCESSES = (By.CSS_SELECTOR, '[data-model-name="Process"]')
    DATA_ASSETS = (By.CSS_SELECTOR, '[data-model-name="DataAsset"]')
    ACCESS_GROUPS = (By.CSS_SELECTOR, '[data-model-name="AccessGroup"]')
    VENDORS = (By.CSS_SELECTOR, '[data-model-name="Vendor"]')
    PRODUCTS = (By.CSS_SELECTOR, '[data-model-name="Product"]')
    PROJECTS = (By.CSS_SELECTOR, '[data-model-name="Project"]')
    RISK_OR_THREATS = (By.CSS_SELECTOR,
                       '[data-test-id="risk/threats_66116337"]')
    RISKS = (By.CSS_SELECTOR, '[data-model-name="Risk"]')
    FACILITIES = (By.CSS_SELECTOR, '[data-model-name="Facility"]')
    MARKETS = (By.CSS_SELECTOR, '[data-model-name="Market"]')
    THREATS = (By.CSS_SELECTOR, '[data-model-name="Threat"]')

    # buttons create new modal
    BUTTON_CREATE_NEW_PROGRAM = (
        By.CSS_SELECTOR,
        '[data-model-name="Program"] ['
        'data-test-id="button_lhn_create_new_program_522c563f"]')
    BUTTON_CREATE_NEW_WORKFLOW = (
        By.CSS_SELECTOR,
        '[data-model-name="Workflow"] ['
        'data-test-id="button_lhn_create_new_program_522c563f"]')
    BUTTON_CREATE_NEW_AUDIT = (
        By.CSS_SELECTOR,
        '[data-model-name="Audit"] ['
        'data-test-id="button_lhn_create_new_program_522c563f"]')
    BUTTON_CREATE_NEW_CONTROL_ASSESSMENT = (
        By.CSS_SELECTOR,
        '[data-model-name="ControlAssessment"] ['
        'data-test-id="button_lhn_create_new_program_522c563f"]')
    BUTTON_CREATE_NEW_REQUEST = (
        By.CSS_SELECTOR,
        '[data-model-name="Request"] ['
        'data-test-id="button_lhn_create_new_program_522c563f"]')
    BUTTON_CREATE_ISSUE = (
        By.CSS_SELECTOR,
        '[data-model-name="Issue"] ['
        'data-test-id="button_lhn_create_new_program_522c563f"]')

    # count locators
    PROGRAMS_COUNT = (By.CSS_SELECTOR, '[data-model-name="Program"] '
                                       '.item-count')
    WORKFLOWS_COUNT = (By.CSS_SELECTOR, '[data-model-name="Workflow"] '
                                        '.item-count')
    AUDITS_COUNT = (By.CSS_SELECTOR, '[data-model-name="Audit"] .item-count')
    CONTROL_ASSESSMENTS_COUNT = (By.CSS_SELECTOR,
                                 '[data-model-name="ControlAssessment"] '
                                 '.item-count')
    ISSUES_COUNT = (By.CSS_SELECTOR, '[data-model-name="Issue"] .item-count')
    REQUESTS_COUNT = (By.CSS_SELECTOR, '[data-model-name="Request"] '
                                       '.item-count')
    REGULATIONS_COUNT = (By.CSS_SELECTOR,
                         '[data-model-name="Regulation"] .item-count')
    POLICIES_COUNT = (By.CSS_SELECTOR,
                      '[data-model-name="Policy"] .item-count')
    STANDARDS_COUNT = (By.CSS_SELECTOR,
                       '[data-model-name="Standard"] .item-count')
    CONTRACTS_COUNT = (By.CSS_SELECTOR,
                       '[data-model-name="Clause"] .item-count')
    CLAUSES_COUNT = (By.CSS_SELECTOR,
                     '[data-model-name="Regulation"] .item-count')
    SECTIONS_COUNT = (By.CSS_SELECTOR,
                      '[data-model-name="Section"] .item-count')
    CONTROL_COUNT = (By.CSS_SELECTOR, '[data-model-name="Control"] .item-count')
    OBJECTIVES_COUNT = (By.CSS_SELECTOR, '[data-model-name="Objective"] '
                                         '.item-count')
    PEOPLE_COUNT = (By.CSS_SELECTOR, '[data-model-name="Person"] .item-count')
    ORG_GROUPS_COUNT = (By.CSS_SELECTOR, '[data-model-name="OrgGroup"] '
                                         '.item-count')
    VENDORS_COUNT = (By.CSS_SELECTOR, '[data-model-name="Vendor"] .item-count')
    ACCESS_GROUPS_COUNT = (By.CSS_SELECTOR, '[data-model-name="AccessGroup"] '
                                            '.item-count')
    SYSTEMS_COUNT = (By.CSS_SELECTOR, '[data-model-name="System"] .item-count')
    PROCESSES_COUNT = (By.CSS_SELECTOR, '[data-model-name="Process"] '
                                        '.item-count')
    DATA_ASSETS_COUNT = (By.CSS_SELECTOR, '[data-model-name="DataAsset"] '
                                          '.item-count')
    PRODUCTS_COUNT = (By.CSS_SELECTOR, '[data-model-name="Product"] '
                                       '.item-count')
    PROJECTS_COUNT = (By.CSS_SELECTOR, '[data-model-name="Project"] '
                                       '.item-count')
    FACILITIES_COUNT = (By.CSS_SELECTOR, '[data-model-name="Facility"] '
                                        '.item-count')
    MARKETS_COUNT = (By.CSS_SELECTOR, '[data-model-name="Market"] .item-count')
    RISKS_COUNT = (By.CSS_SELECTOR, '[data-model-name="Risk"] .item-count')
    THREATS_COUNT = (By.CSS_SELECTOR, '[data-model-name="Threat"] .item-count')


class ModalCreateNewProgram(object):
    TITLE_UI = (By.CSS_SELECTOR,
                '[data-test-id="new_program_field_title_a63ed79d"]')
    DESCRIPTION_UI = (By.CSS_SELECTOR,
                      '[data-test-id="new_program_field_description_1fb8bc06"]'
                      '>iframe.wysihtml5-sandbox')
    NOTES_UI = (By.CSS_SELECTOR,
                '[data-test-id="new_program_field_notes_75b8bc05"]'
                '>iframe.wysihtml5-sandbox')
    CODE_UI = (By.CSS_SELECTOR,
               '[data-test-id="new_program_field_code_334276e2"]')
    STATE_UI = (By.CSS_SELECTOR,
                '[data-test-id="new_program_dropdown_state_036a1fa6"]')
    BUTTON_HIDE_OPTIONAL_FIELDS = (By.ID, "formHide")
    BUTTON_SHOW_ALL_OPTIONAL_FIELDS = (By.ID, "formHide")
    PRIMARY_CONTACT_UI = (By.CSS_SELECTOR, '[data-test-id='
                          '"new_program_field_primary_contact_86160053"]')
    DROPDOWN_CONTACT = (By.CSS_SELECTOR, '.ui-menu-item')
    SECONDARY_CONTACT_UI = (By.CSS_SELECTOR, '[data-test-id='
                            '"new_program_field_secondary_contact_'
                            '86160053"]')
    BUTTON_SAVE_AND_CLOSE = (By.CSS_SELECTOR, '[data-toggle="modal-submit"]')
    BUTTON_SAVE_AND_ADD_ANOTHER = (
        By.CSS_SELECTOR, '[data-toggle="modal-submit-addmore"]')
    PROGRAM_URL_UI = (By.CSS_SELECTOR, '[data-test-id='
                      '"new_program_field_program_url_86160053"]')
    REFERENCE_URL_UI = (By.CSS_SELECTOR, '[data-test-id='
                        '"new_program_field_reference_url_86160053"]')
    EFFECTIVE_DATE_UI = (By.CSS_SELECTOR, '[data-test-id='
                         '"new_program_field_effective_date_f2783a28"]')
    STOP_DATE_UI = (By.CSS_SELECTOR, '[data-test-id='
                    '"new_program_field_stop_date_f2783a28"]')
    DATE_PICKER = (By.CSS_SELECTOR, '.ui-datepicker-calendar ['
                   'data-handler="selectDay"]')
    TITLE = (By.CSS_SELECTOR, '[data-test-id="label_title_2c925d94"]')
    DESCRIPTION = (By.CSS_SELECTOR,
                   '[data-test-id="label_description_2c925d94"]')

    PRIVACY = (By.CSS_SELECTOR, '[data-test-id="label_privacy_2c925d94"]')
    PROGRAM_URL = (By.CSS_SELECTOR,
                   '[data-test-id="label_program_url_2c925d94"]')


class WidgetBar(object):
    BUTTON_ADD = (By.CSS_SELECTOR,
                  '[data-test-id="button_widget_add_2c925d94"]')
    TAB_ACTIVE = (By.CSS_SELECTOR, ".object-nav .active")


class WidgetBarButtonAddDropdown(object):
    AUDITS = (By.CSS_SELECTOR, '[data-test-id="button_widget_add_2c925d94"] '
                               '[href="#audit_widget"]')
    CONTROLS = (By.CSS_SELECTOR, '[data-test-id="button_widget_add_2c925d94"] '
                                 '[href="#control_widget"]')
    DATA_ASSETS = (By.CSS_SELECTOR,
                   '[data-test-id="button_widget_add_2c925d94"] '
                   '[href="#data_asset_widget"]')
    ISSUES = (By.CSS_SELECTOR, '[data-test-id="button_widget_add_2c925d94"] '
                               '[href="#issues_widget"]')
    OBJECTIVES = (By.CSS_SELECTOR,
                  '[data-test-id="button_widget_add_2c925d94"] '
                  '[href="#objective_widget"]')
    POLICIES = (By.CSS_SELECTOR, '[data-test-id="button_widget_add_2c925d94"] '
                                 '[href="#policy_widget"]')
    PRODUCTS = (By.CSS_SELECTOR, '[data-test-id="button_widget_add_2c925d94"] '
                                 '[href="#product_widget"]')
    REGULATIONS = (By.CSS_SELECTOR,
                   '[data-test-id="button_widget_add_2c925d94"] '
                   '[href="#regulation_widget"]')
    SYSTEMS = (By.CSS_SELECTOR, '[data-test-id="button_widget_add_2c925d94"] '
                                '[href="#system_widget"]')
    RISKS = (By.CSS_SELECTOR, '[data-test-id="button_widget_add_2c925d94"] '
                              '[href="#risk_widget"]')
    WORKFLOWS = (By.CSS_SELECTOR, '[data-test-id="button_widget_add_2c925d94"] '
                                  '[href="#workflow_widget"]')
    CONTRACTS = (By.CSS_SELECTOR, '[data-test-id="button_widget_add_2c925d94"] '
                                  '[href="#contract_widget"]')
    CONTROL_ASSESSMENTS = (By.CSS_SELECTOR,
                           '[data-test-id="button_widget_add_2c925d94"] '
                           '[href="#control_assessment_widget"]')
    FACILITIES = (By.CSS_SELECTOR,
                  '[data-test-id="button_widget_add_2c925d94"] '
                  '[href="#facility_widget"]')
    MARKETS = (By.CSS_SELECTOR, '[data-test-id="button_widget_add_2c925d94"] '
                                '[href="#market_widget"]')
    ORG_GROUPS = (By.CSS_SELECTOR,
                  '[data-test-id="button_widget_add_2c925d94"] '
                  '[href="#org_groups_widget"]')
    PROCESSES = (By.CSS_SELECTOR, '[data-test-id="button_widget_add_2c925d94"] '
                                  '[href="#process_widget"]')
    PROJECTS = (By.CSS_SELECTOR, '[data-test-id="button_widget_add_2c925d94"] '
                                 '[href="#project_widget"]')
    STANDARDS = (By.CSS_SELECTOR, '[data-test-id="button_widget_add_2c925d94"] '
                                  '[href="#standard_widget"]')
    VENDORS = (By.CSS_SELECTOR, '[data-test-id="button_widget_add_2c925d94"] '
                                '[href="#vendor_widget"]')
    THREAD_ACTORS = (By.CSS_SELECTOR,
                     '[data-test-id="button_widget_add_2c925d94"] '
                     '[href="#thread_actors_widget"]')
    WORKFLOW_TASKS = (By.CSS_SELECTOR,
                      '[data-test-id="button_widget_add_2c925d94"] '
                      '[href="#TASK_widget"]')


class Widget(object):
    DROPDOWN_SETTINGS = (By.CSS_SELECTOR, '.info-pane-utility')
    DROPDOWN_SETTINGS_MEMBERS = (By.CSS_SELECTOR, '.info-pane-utility'
                                                  ' .dropdown-menu li')
    ALERT_LINK_COPIED = (By.CSS_SELECTOR, '.alert.alert-success')
    DROPDOWN_DELETE = (By.CSS_SELECTOR,
                       '[data-test-id="dropdown_delete_0839163b"]')
    MODAL_DELETE = (By.ID, '[id="ajax-modal-javascript:--"]')
    MODAL_DELETE_CLOSE = (By.CSS_SELECTOR, '.modal .grcicon-x-grey')

    TITLE = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h6')
    TITLE_ENTERED = (By.CSS_SELECTOR, '[data-test-id="title_0ad9fbaf"] h3')
    OBJECT_REVIEW = (By.CSS_SELECTOR,
                     '[data-test-id="title_review_0ad9fbaf"] h6')
    SUBMIT_FOR_REVIEW = (By.CSS_SELECTOR,
                         '[data-test-id="title_review_0ad9fbaf"] '
                         '[href="javascript://"]')
    DESCRIPTION = (By.CSS_SELECTOR,
                   '[data-test-id="title_description_7a906d2e"] h6')
    DESCRIPTION_ENTERED = (By.CSS_SELECTOR,
                           '[data-test-id="title_description_'
                           'content_7a906d2e"]')
    NOTES = (By.CSS_SELECTOR, '[data-test-id="title_notes_ef5bc3a71e88"] '
                              'h6')
    NOTES_ENTERED = (By.CSS_SELECTOR,
                     '[data-test-id="title_notes_content_ef5bc3a71e88"]')
    MANAGER = (By.CSS_SELECTOR, '[data-test-id="title_manager_7a906d2e"] '
                                'h6')
    MANAGER_ENTERED = (By.CSS_SELECTOR,
                       '[data-test-id="title_manager_7a906d2e"] '
                       '[data-test-id="text_manager_7a906d2e"]')
    PROGRAM_URL = (By.CSS_SELECTOR,
                   '[data-test-id="title_program_url_aa7d1a65"] h6')
    PROGRAM_URL_ENTERED = (By.CSS_SELECTOR,
                           '[data-test-id="text_program_url_aa7d1a65"]')
    REFERENCE_URL = (By.CSS_SELECTOR,
                     '[data-test-id="title_reference_url_aa7d1a65"]')
    REFERENCE_URL_ENTERED = (By.CSS_SELECTOR,
                             '[data-test-id="text_reference_url_aa7d1a65"]')
    BUTTON_SHOW_ADVANCED = (By.CSS_SELECTOR,
                            '[data-test-id="button_advanced_cf47bc01"]')
    CODE = (By.CSS_SELECTOR, '[data-test-id="title_code_cf47bc01"] h6')
    CODE_ENTERED = (By.CSS_SELECTOR,
                    '[data-test-id="title_code_cf47bc01"]>p')
    EFFECTIVE_DATE = (By.CSS_SELECTOR,
                      '[data-test-id="title_effective_date_cf47bc01"] h6')
    EFFECTIVE_DATE_ENTERED = (By.CSS_SELECTOR,
                              '[data-test-id="title_effective_date_'
                              'cf47bc01"] p')
    STOP_DATE = (By.CSS_SELECTOR,
                 '[data-test-id="title_stop_date_cf47bc01"] h6')
    STOP_DATE_ENTERED = (By.CSS_SELECTOR,
                         '[data-test-id="title_stop_date_cf47bc01"] p')
    BUTTON_SHOW_CUSTOM_ATTR = (By.CSS_SELECTOR, '[data-test-id="button_'
                                                'custom_attrs_cf47bc01"]')
    STATE = (By.CSS_SELECTOR,
             '[dadata-test-id="new_program_button_save_and_new_86160053"'
             ' ta-test-id="title_state_0ad9fbaf"] h6')
    STATE_ENTERED = (By.CSS_SELECTOR,
                     '[data-test-id="title_state_value_0ad9fbaf"]')
    PRIMARY_CONTACT = (By.CSS_SELECTOR, '[data-test-id="title_primary_'
                                        'contact_696de7244b84"] h6')
    PRIMARY_CONTACT_ENTERED = (
        By.CSS_SELECTOR, '[data-test-id="text_primary_contact_'
                         '696de7244b84"] [data-test-id="text_'
                         'manager_7a906d2e"]')
    SECONDARY_CONTACT = (
        By.CSS_SELECTOR, '[data-test-id="title_contacts_696de7244b84"] '
                         'h6:nth-child(2)')
    SECONDARY_CONTACT_ENTERED = (
        By.CSS_SELECTOR, '[data-test-id="text_secondary_contact_'
                         '696de7244b84"] [data-test-id="text_manager_'
                         '7a906d2e"]')
    PRIVATE_PROGRAM = (By.CSS_SELECTOR,
                       '[data-test-id="title_private_ec758af9"] h6')
    ICON_LOCK = (By.CSS_SELECTOR, '[data-test-id="icon_private_ec758af9"]')
