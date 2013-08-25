'''
Created on Jun 18, 2013

@author: diana.tzinov
'''


class Elements(object):
       
        
        logo = "//div[contains(@class,\"logo\")]/a"
        login_button = "//a[2]"
        #dashboard_page = ""
        
        gmail_userid_textfield = "//input[@id=\"Email\"]"
        gmail_password_textfield = "//input[@id=\"Passwd\"]"
        gmail_submit_credentials_button = "//input[@type=\"submit\"]"
        
        dashboard_title= "//h1[@class=\"dashboard-title\"]"
        
        left_nav_governance_controls_numbers = "//li[contains(@class,\"governance\")][1]/a//span[@class=\"item-count\"]"
        left_nav_governance_controls_numbers_not_loaded = "//li[contains(@class,\"governance\")][1]/a//span[contains(.,\"...\")]"
        left_nav_governance_contracts_numbers = "//li[contains(@class,\"governance\")][2]/a//span[@class=\"item-count\"]"
        left_nav_governance_contracts_numbers_not_loaded = "//li[contains(@class,\"governance\")][2]/a//span[contains(.,\"...\")]"
        
        left_nav_governance_policies_numbers = "//li[contains(@class,\"governance\")][3]/a//span[@class=\"item-count\"]"
        left_nav_governance_policies_numbers_not_loaded= "//li[contains(@class,\"governance\")][3]/a//span[contains(.,\"...\")]"
        left_nav_governance_regulations_numbers ="//li[contains(@class,\"governance\")][4]/a//span[@class=\"item-count\"]"
        left_nav_governance_regulations_numbers_not_loaded="//li[contains(@class,\"governance\")][4]/a//span[contains(.,\"...\")]"
        
        
        
        #"//ul[@class=\"top-level\"]//li[@data-model-name=\"SECTION\"]//li[1][contains(.,\"OBJECT_TITLE\")]/a"
        left_nav_expand_object_section_link = "//ul[@class=\"top-level\"]//li[@data-model-name=\"OBJECT\"]/a"
        left_nav_object_section_add_button = "//ul[@class=\"top-level\"]//li[@data-model-name=\"OBJECT\"]//li[@class=\"add-new\"]/a"
        left_nav_last_created_object_link = "//ul[@class=\"top-level\"]//li[@data-model-name=\"SECTION\"]//li[1][contains(.,\"OBJECT_TITLE\")]/a"
        
        #edit_window ="//div[@class=\"modal_window-header\"]//*[contains(text(),\"Edit\")]"
        modal_window_show_hidden_fields_link = "//a[@class=\"show-hidden-fields\"]"
        modal_window_delete_button = "//a[contains(@class,\"danger\")]"
        modal_window_confirm_delete_button = "//div[@class=\"confirm-buttons\"]/a[@data-method=\"delete\"]"
        
        modal_window_description_frame = "//iFrame[@class=\"wysihtml5-sandbox\"]"
        modal_window ="//form"
        #modal_window = "//div[@class=\"modal_window-body\"]"
        modal_window_title_textfield= "//div[@class=\"modal-body\"]//input[@name=\"title\"]"
        modal_window_owner_textfield = "//input[contains(@placeholder,\"email address\")]"
        modal_window_save_button = "//div[@class=\"confirm-buttons\"]//a[contains(text(),\"Save\")]"
        
        object_detail_page_edit_link = "//section[contains(@id,\"info_widget\")]//a[contains(@title,\"Edit\")]"
        object_detail_page_info_section = "//section[contains(@id,\"info_widget\")]"

        object_info_page_edit_link ="//a[@class=\"info-edit\"]"
        object_title= "//div[@class=\"modal-body\"]/form//input[@name=\"title\"]"
        object_description = "//iFrame[@class=\"wysihtml5-sandbox\"]"
        object_owner="//input[contains(@placeholder,\"email address\")]"
        object_url ="//div[@class=\"modal-body\"]//div[@class=\"row-fluid\"][2]//input[@name=\"url\"]"
        object_code ="//div[@class=\"hidden-fields-area\"]//input[@name=\"slug\"]"
        object_organization ="//div[@class=\"hidden-fields-area\"]//input[@name=\"org_name\"]"
        object_scope ="//div[@class=\"hidden-fields-area\"]//input[@name=\"scope\"]"
        object_kind ="//div[@class=\"hidden-fields-area\"]//select"
        object_kind_option = "//div[@class=\"hidden-fields-area\"]//select/option[TOKEN]"
        object_kind_selected_option = "//div[@class=\"hidden-fields-area\"]//select/option[contains(@selected, \"selected\")]"