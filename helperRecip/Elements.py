'''
Created on Jun 18, 2013

@author: diana.tzinov
'''


class Elements(object):
       
        
        logo = "//div[contains(@class,\"logo\")]/a"
        login_button = "//a[2]"
        
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
        
        left_nav_expand_object_section_link = "//ul[@class=\"top-level\"]//li[@data-model-name=\"OBJECT\"]/a"
        left_nav_object_section_add_button = "//ul[@class=\"top-level\"]//li[@data-model-name=\"OBJECT\"]//li[@class=\"add-new\"]/a"
        left_nav_last_created_object_link = "//ul[@class=\"top-level\"]//li[@data-model-name=\"SECTION\"]//li[1][contains(.,\"OBJECT_TITLE\")]/a"
        left_nav_first_object_link_in_the_section = "//ul[@class=\"top-level\"]//li[@data-model-name=\"SECTION\"]//li[1]/a"
        left_nav_first_object_link_in_the_section_object_name ="//ul[@class=\"top-level\"]//li[@data-model-name=\"SECTION\"]//li[1]/a//span[@class=\"lhs-item\"]"
       
       
        inner_nav_object_link = "//div[@class=\"inner-nav\"]//div[@class=\"object-nav\"]//a[contains(@href,\"OBJECT\")]"
       
        #map_to_this_object_link = "//a[@class=\"primary map-to-page-object\"]"
        map_to_this_object_link = "//div[@id=\"extended-info\"]//a[contains(@class, \"map-to-page-object\")]"
        mapped_object = "//section[contains(@id,\"OBJECT\")]//li[@data-object-id=ID]"
        
        
        modal_window_show_hidden_fields_link = "//a[@class=\"show-hidden-fields\"]"
        modal_window_delete_button = "//a[contains(@class,\"danger\")]"
        modal_window_confirm_delete_button = "//div[@class=\"confirm-buttons\"]/a[@data-method=\"delete\"]"
        modal_window ="//form"
        modal_window_hidden_fields_area = "//div[@class=\"hidden-fields-area\"]"
        modal_window_save_button = "//div[@class=\"confirm-buttons\"]//a[contains(text(),\"Save\")]"
        
        object_detail_page_edit_link = "//section[contains(@id,\"info_widget\")]//a[contains(@title,\"Edit\")]"
        object_detail_page_info_section = "//section[contains(@id,\"info_widget\")]"

        object_info_page_edit_link ="//a[@class=\"info-edit\"]"
        object_title= "//div[@class=\"modal-body\"]/form//input[@name=\"title\"]"
        object_iFrame = "//ul[contains(@id,\"FRAME_NAME\")]/parent::div/iFrame"
        object_owner="//input[contains(@placeholder,\"email address\")]"
        object_url ="//div[@class=\"modal-body\"]//div[@class=\"row-fluid\"][2]//input[@name=\"url\"]"
        object_code ="//div[@class=\"hidden-fields-area\"]//input[@name=\"slug\"]"
        object_organization ="//div[@class=\"hidden-fields-area\"]//input[@name=\"organization\"]"
        object_scope ="//div[@class=\"hidden-fields-area\"]//input[@name=\"scope\"]"
        object_dropdown ="//div[@class=\"hidden-fields-area\"]//select[@name=\"NAME\"]" 
        object_dropdown_selected_option = "//div[@class=\"hidden-fields-area\"]//select[@name=\"NAME\"]/option[@selected]"
        
        section_active ="//section[contains(@id,\"SECTION\")][contains(@class,\"active\")]"