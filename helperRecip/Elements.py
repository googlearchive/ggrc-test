'''
Created on Jun 18, 2013

@author: diana.tzinov
'''


class Elements(object):
       
        
        logo = "//div[contains(@class,\"logo\")]/a"
        login_button = "//a[2]"
        dashboard_page = ""
        
        business_object_widget_nav_tabs_link = "//section[@id=\"business_objects_widget\"]//ul[@class=\"nav nav-tabs\"]//a[@data-object-singular=\"OBJECT\"]"
        business_object_widget_nav_tabs_markets_link="//section[@id=\"business_objects_widget\"]//ul[@class=\"nav nav-tabs\"]//a[@data-object-singular=\"Market\"]"
        business_object_widget_nav_tabs_process_link="//section[@id=\"business_objects_widget\"]//ul[@class=\"nav nav-tabs\"]//a[@data-object-singular=\"Process\"]"
        business_object_widget_nav_tabs_org_groups_link = "//section[@id=\"business_objects_widget\"]//ul[@class=\"nav nav-tabs\"]//a[@data-object-singular=\"OrgGroup\"]"
        business_object_widget_nav_tabs_facilities_link = "//section[@id=\"business_objects_widget\"]//ul[@class=\"nav nav-tabs\"]//a[@data-object-singular=\"Facility\"]"
        business_object_widget_nav_tabs_products_link = "//section[@id=\"business_objects_widget\"]//ul[@class=\"nav nav-tabs\"]//a[@data-object-singular=\"Product\"]"
        business_object_widget_nav_tabs_data_asset_name_link =  "//section[@id=\"business_objects_widget\"]//ul[@class=\"nav nav-tabs\"]//a[@data-object-singular=\"DataAsset\"]"
        business_object_widget_nav_tabs_projects_link = "//section[@id=\"business_objects_widget\"]//ul[@class=\"nav nav-tabs\"]//a[@data-object-singular=\"Project\"]"
        business_object_widget_nav_tabs_systems_link = "//section[@id=\"business_objects_widget\"]//ul[@class=\"nav nav-tabs\"]//a[@data-object-singular=\"System\"]"
        business_object_add_button = "//section[@id=\"business_objects_widget\"]//a[contains(@class,\"btn-add\")][@data-object-singular=\"OBJECT\"]"
        
        
        gmail_userid_textfield = "//input[@id=\"Email\"]"
        gmail_password_textfield = "//input[@id=\"Passwd\"]"
        gmail_submit_credentials_button = "//input[@type=\"submit\"]"
        
        dashboard_title= "//h1[@class=\"dashboard-title\"]"
        dashboard_widget_last_created_object = "//div[contains(@id,\"WIDGET\")]//li[1]//*[contains(@class,\"title\")][contains(.,\"OBJECT_TITLE\")]"
        
        edit_window ="//div[@class=\"modal-header\"]//*[contains(text(),\"Edit\")]"
        edit_window_show_hidden_fields_link = "//a[@class=\"show-hidden-fields\"]"
        
        jasmine_results = "//div[@class=\"results\"]"
        jasmine_all_tests_passing_element = "//div[@class=\"alert\"]//span[contains(text(),\"Passing\")][contains(text(),\"spec\")]"
        
        governance_widget_nav_tabs_link = "//section[@id=\"governance_widget\"]//ul[@class=\"nav nav-tabs\"]//a[@data-object-singular=\"OBJECT\"]"
        governance_widget_object_add_button = "//section[@id=\"governance_widget\"]//a[contains(@class,\"btn-add\")][@data-object-singular=\"OBJECT\"]"
        governance_widget_nav_tabs_contracts_link = "//section[@id=\"governance_widget\"]//ul[@class=\"nav nav-tabs\"]//a[@data-object-singular=\"Contract\"]"
        governance_widget_nav_tabs_policies_link = "//section[@id=\"governance_widget\"]//ul[@class=\"nav nav-tabs\"]//a[@data-object-singular=\"Policy\"]"
        governance_widget_nav_tabs_regulations_link = "//section[@id=\"governance_widget\"]//ul[@class=\"nav nav-tabs\"]//a[@data-object-singular=\"Regulation\"]"
        governance_widget_nav_tabs_controls_link = "//section[@id=\"governance_widget\"]//ul[@class=\"nav nav-tabs\"]//a[@data-object-singular=\"Control\"]"
        
        risk_widget_object_add_button  = "//section[@id=\"risk_widget\"]//a[contains(@class,\"btn-add\")][@data-object-singular=\"Risk\"]"
        
        
        widget_program_edit_page_edit_link = "//section[contains(@id,\"info_widget\")]//a[contains(@title,\"Edit\")]"
        widget_governance_edit_page_edit_link ="//section[contains(@id,\"info\")]//a[contains(@title,\"Edit\")]"
        #widget_governance_edit_page_edit_link = "
        widget_view_link ="//div[contains(@id,\"WIDGET\")]//div[contains(@class,\"item-content\")]//a[@data-original-title=\"View \"]"
        
        left_nav_governance_controls_numbers = "//li[contains(@class,\"governance\")][1]/a//span[@class=\"item-count\"]"
        left_nav_governance_controls_numbers_not_loaded = "//li[contains(@class,\"governance\")][1]/a//span[contains(.,\"...\")]"
        left_nav_governance_contracts_numbers = "//li[contains(@class,\"governance\")][2]/a//span[@class=\"item-count\"]"
        left_nav_governance_contracts_numbers_not_loaded = "//li[contains(@class,\"governance\")][2]/a//span[contains(.,\"...\")]"
        left_nav_governance_policies_numbers = "//li[contains(@class,\"governance\")][3]/a//span[@class=\"item-count\"]"
        left_nav_governance_policies_numbers_not_loaded= "//li[contains(@class,\"governance\")][3]/a//span[contains(.,\"...\")]"
        left_nav_governance_regulations_numbers ="//li[contains(@class,\"governance\")][4]/a//span[@class=\"item-count\"]"
        left_nav_governance_regulations_numbers_not_loaded="//li[contains(@class,\"governance\")][4]/a//span[contains(.,\"...\")]"
        
        modal_save_button = "//div[@class=\"confirm-buttons\"]//a[@href=\"javascript://\"]"
        
        
        programs_widget_add_program_button = "//section[@id=\"programs_widget\"]//a[contains(@class,\"btn\")][@data-object-singular=\"Program\"]"
        modal = "//div[@class=\"modal-body\"]"
        modal_title_textfield= "//div[@class=\"modal-body\"]//input[@name=\"title\"]"
        modal_owner_textfield = "//input[contains(@placeholder,\"email address\")]"
        
        #progarm_object= [grcobject.title,
        #owner", "url", "code", "organization", "scope"]
        
            
        object_title= "//div[@class=\"modal-body\"]/form//input[@name=\"title\"]"
        object_description ="//div[@class=\"modal-body\"]/form//*[@name=\"description\"]"
        object_owner="//div[@class=\"modal-body\"]/form//input[@name=\"owner\"]"
        object_url ="//div[@class=\"modal-body\"]//div[@class=\"row-fluid\"][2]//input[@name=\"url\"]"
        object_code ="//div[@class=\"hidden-fields-area\"]//input[@name=\"slug\"]"
        object_organization ="//div[@class=\"hidden-fields-area\"]//input[@name=\"org_name\"]"
        object_scope ="//div[@class=\"hidden-fields-area\"]//input[@name=\"scope\"]"
        object_kind ="//div[@class=\"hidden-fields-area\"]//select[@name=\"kind\"]"
        object_kind_selected_option = "//select/option[contains(@selected, \"selected\")]"