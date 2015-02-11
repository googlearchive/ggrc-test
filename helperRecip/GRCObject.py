'''
Created on Jul 20, 2013

@author: diana.tzinov

'''

from Elements import Elements

class GRCObject(object):
    elem = Elements()

    contract_elements = {
                        "title":elem.object_title,   
                         "owner":elem.object_owner, 
                        "description":elem.object_iFrame,
                        "url":elem.object_url,
                        "code":elem.object_code
                        } 

    clause_elements = {
                        "title":elem.object_title,   
                         "owner":elem.object_owner,
                        "code":elem.object_code
                        } 

    vendor_elements = {
                        "title":elem.object_title,   
                         "owner":elem.object_owner, 
                        "description":elem.object_iFrame,
                        "url":elem.object_url,
                        "code":elem.object_code
                        } 

    contract_values = {
                      'title':"",  
                      'owner':"",
                      "description":"",
                      'url': "http://www.google.com", 
                      "code":"auto-populated-code"
                      }
    
    clause_values = {
                      'title':"",  
                      'owner':"",
                      "code":"auto-populated-code"
                      }    

    vendor_values = {
                      'title':"",  
                      'owner':"",
                      "description":"",
                      'url': "http://www.google.com", 
                      "code":"auto-populated-code"
                      }

    #PEOPLE
    people_elements = {
                        "name":elem.object_title,   
                         "email":elem.object_owner, 
                         "company":elem.object_iFrame,
                      }


    #CONTROL
    control_elements = {
                        "title":elem.object_title,   
                         "owner":elem.object_owner, 
                         "description":elem.object_iFrame,
                        "url":elem.object_url,
                        "code":elem.object_code,
                        "kind":elem.object_dropdown,
                        "fraud_related":elem.object_dropdown,
                        "key_control":elem.object_dropdown,
                        "means":elem.object_dropdown
                        } 

    control_values = {
                      'title':"",  
                      'owner':"",
                      "description":"",
                      'url': "http://www.google.com", 
                      "code":"auto-populated-code",
                      "kind":3,
                      "fraud_related":2,
                      "key_control":2,
                      "means":2
                      }

    #DATA ASSET
    data_asset_elements = {
                        "title":elem.object_title,   
                        "owner":elem.object_owner,  
                         "description":elem.object_iFrame,
                        "url":elem.object_url,
                        "code":elem.object_code
                        } 

    data_asset_values = {
                      'title':"",  
                      'owner':"",
                      "description":"",
                      'url': "http://www.google.com", 
                      "code":"auto-populated-code"
                      }

    #FACITY
    facility_elements = {
                        "title":elem.object_title,  
                        "owner":elem.object_owner,  
                         "description":elem.object_iFrame,
                        "url":elem.object_url,
                        "code":elem.object_code
                        } 

    facility_values = {
                      'title':"",  
                      'owner':"",
                      "description":"",
                      'url': "http://www.google.com", 
                      "code":"auto-populated-code"
                      }

    #MARKET
    market_elements = {
                        "title":elem.object_title,  
                        "owner":elem.object_owner,  
                         "description":elem.object_iFrame,
                        "url":elem.object_url,
                        "code":elem.object_code
                        } 



    market_values = {
                      'title':"",  
                      'owner':"",
                      "description":"",
                      'url': "http://www.google.com", 
                      "code":"auto-populated-code"
                      }


    #ORGGROUPS
    org_group_elements = {
                        "title":elem.object_title,    
                        "owner":elem.object_owner,
                         "description":elem.object_iFrame,
                        "url":elem.object_url,
                        "code":elem.object_code
                        } 



    org_group_values = {
                      'title':"",  
                      'owner':"",
                      "description":"",
                      'url': "http://www.google.com", 
                      "code":"auto-populated-code"
                      }
        #POLICY

    policy_elements = {
                        "title":elem.object_title, 
                        "owner":elem.object_owner, 
                         "description":elem.object_iFrame,  
                        "url":elem.object_url,
                        "code":elem.object_code,
                        "kind":elem.object_dropdown
                        #"kind":elem.object_kind
                        } 

    policy_values = {
                      'title':"",  
                       'owner':"",
                      "description":"",
                      'url': "http://www.google.com", 
                       "code":"auto-populated-code",
                       "kind":3
                      }

    #PROCESS
    process_elements = {
                        "title":elem.object_title,  
                        "owner":elem.object_owner,
                       "description":elem.object_iFrame,  
                        "url":elem.object_url,
                        "code":elem.object_code,
                         "notes":elem.object_iFrame,
                         "network_zone":elem.object_dropdown,
                        } 

    process_values = {
                      'title':"",  
                      'owner':"",
                      "description":"",
                      'url': "http://www.google.com", 
                      "code":"auto-populated-code",
                      "notes":"",
                      "network_zone":2
                      }

    #POLICY
    product_elements = {
        "title": elem.object_title,
        "owner": elem.object_owner,
        "description": elem.object_iFrame,
        "url": elem.object_url,
        "code": elem.object_code,
        "kind": elem.object_dropdown
    }

    product_values = {
        'title': "",  
        'owner': "",
        "description": "",
        'url':  "http: //www.google.com", 
        "code": "auto-populated-code",
        "kind": 3
    }

    #PROGRAM
    program_elements = {
        "title": elem.object_title,
        #"owner": elem.object_owner,
        "description": elem.object_iFrame,
        "url": elem.object_url,
        "code": elem.object_code,
    }
    program_values = {
        'title': "",  
        #'owner': "",
        "description": "",
        'url':  "http: //www.google.com", 
        "code": "auto-populated-code",
    }

    #PROJECT
    project_elements = {
                        "title":elem.object_title,  
                        "owner":elem.object_owner,
                         "description":elem.object_iFrame,  
                        "url":elem.object_url,
                        "code":elem.object_code
                        } 

    project_values = {
                      'title':"",  
                      'owner':"",
                      "description":"",
                      'url': "http://www.google.com", 
                      "code":"auto-populated-code"
                      }

    #REGULATION
    regulation_elements = {
                        "title":elem.object_title,  
                        "owner":elem.object_owner,  
                        "description":elem.object_iFrame,
                        "url":elem.object_url,
                        "code":elem.object_code
                        } 

    regulation_values = {
                      'title':"",  
                      'owner':"",
                      "description":"",
                      'url': "http://www.google.com", 
                      "code":"auto-populated-code"
                      }

    #OBJECTIVE
    objective_elements = {
                        "title":elem.object_title,  
                        "owner":elem.object_owner,  
                        "description":elem.object_iFrame,
                        "url":elem.object_url,
                        "code":elem.object_code
                        } 

    objective_values = {
                      'title':"",  
                      'owner':"",
                      "description":"",
                      'url': "http://www.google.com", 
                      "code":"auto-populated-code"
                      }

    #ORG GROUP
    group_elements = {
                        "title":elem.object_title,  
                        "owner":elem.object_owner,  
                        "description":elem.object_iFrame,
                        "url":elem.object_url,
                        "code":elem.object_code
                        } 

    group_values = {
                      'title':"",  
                      'owner':"",
                      "description":"",
                      'url': "http://www.google.com", 
                      "code":"auto-populated-code"
                      }


    #STANDARD
    standard_elements = {
                        "title":elem.object_title,  
                        "owner":elem.object_owner,  
                        "description":elem.object_iFrame,
                        "url":elem.object_url,
                        "code":elem.object_code
                        } 

    standard_values = {
                      'title':"",  
                      'owner':"",
                      "description":"",
                      'url': "http://www.google.com", 
                      "code":"auto-populated-code"
                      }

    section_elements = {
                        "title":elem.object_title,
                        "owner":elem.object_owner,  
                        "description":elem.object_iFrame,
                        "code":elem.object_code
                        } 

    section_values = {
                      'title':"",  
                      'owner':"",
                      "description":"",
                      "code":"auto-populated-code"
                      }

    system_elements = {
                        "title":elem.object_title,  
                        "owner":elem.object_owner, 
                       "description":elem.object_iFrame, 
                        "url":elem.object_url,
                        "code":elem.object_code,
                        "notes":elem.object_iFrame,
                         "network_zone":elem.object_dropdown,
                        "network_zone":elem.object_dropdown
                        } 

    system_values = {
                      'title':"",  
                      'owner':"",
                      "description":"",
                      'url': "http://www.google.com", 
                      "code":"auto-populated-code",
                      "notes":"",
                      "network_zone":2
                      }

    program_map_to_lhn = ["Vendor",
                         "Regulation", "Contract", 
                         "Policy", 
                         "Standard", "Control", "Objective", 
                         "System", "Process", "Data", "Product", "Project", "Facility", "Market", "Group",
                         #"Person" CORE-1170
                          ]

    

    program_map_to_widget = ["Vendor",
                            "Control", "Objective", "System",
                            "Regulation",  "Contract", "Policy", "Standard", "Process", 
                            "Org_Group", "Data_Asset",  "Product", "Project", "Facility", "Market",
                             #"Person" CORE-1170                          
                             ]

#LHN GOVERNANCE OBJECTS

    regulation_map_to_lhn = ["Vendor",
                            "Program",
                            "System", "Process", "Data", "Product", "Project", "Facility", "Market", "Group",
                            #"Person" CORE-1170
                          ]

    contract_map_to_lhn =  ["Vendor", 
                            "Objective", "Facility", "Program",
                            "Control", "System", "Process", "Data", "Product", "Project", "Clause", "Market",
                            "Group"
                            #"Person" CORE-1170
                           ]
    
    vendor_map_to_lhn =  ["Facility", "Program",
                            "Objective", "Contract", "Standard", "Regulation", "Policy", 
                            "Control", "System", "Process", "Data", "Product", "Project", "Clause", "Market",
                            "Group", "Section",
                            #"Person" CORE-1170
                           ]    
    
    standard_map_to_lhn =  ["Vendor",
                            "Regulation", "Program",  "Policy",
                            "Clause", "Objective", "Control", "System", "Process", 
                            "Data", "Product", "Project", "Facility", "Market", "Group",
                            #"Person",  
                            #"Contract" CORE-307
                           ]
    

    control_map_to_lhn =  ["Vendor",
                        "System", "Process",  "Project", "Facility", "Market", "Group","Contract",
                        "Policy", "Objective", "Data",
                        "Product","Program", "Regulation", "Standard", "Section", "Clause",
                         #"Person" CORE-1170
                          ]

    policy_map_to_lhn = ["Vendor",
                         "Program",
                         "System", "Process", "Data", "Product", "Project", "Facility", "Market", "Group",
                         #"Person" CORE-1170                 
                        ]

    objective_map_to_lhn = ["Vendor",
                            "Program", "Regulation", "Standard", "Section", "Clause",
                            "System", "Process", "Data", "Product", "Project", "Facility", "Market", "Group",
                            "Contract", "Policy", "Control",
                            #"Person" CORE-1170
                          ]

#BUSINESS OBJECT LHN

    system_map_to_lhn = ["Vendor",
                         "Program", "Regulation", "Contract", "Policy", "Standard", "Section",
                          "Clause", "Control", "Objective",
                          "Process", "Data", "Product", "Project", "Facility", "Market", "Group",
                          #"Person" CORE-1170
                        ]

    process_map_to_lhn = ["Vendor",
                          "Program", "Regulation", "Contract", "Policy", "Standard", "Section",
                          "Clause", "Control", "Objective",
                          "System", "Data", "Product", "Project", "Facility", "Market", "Group",
                          #"Person" CORE-1170
                         ]

    data_asset_map_to_lhn = ["Vendor",
                            "Clause", # blocked by CORE-319
                            "Policy",
                            "Standard", "Section",
                            "Regulation", "Contract",  "Control", "Objective", "Program",
                            "System", "Process", "Product", "Project", "Facility", "Market", 
                            "Group",
                            #"Person" CORE-1170
                        ]

    product_map_to_lhn = ["Vendor",
                        "Program", "Regulation", "Contract", "Policy", "Standard", "Section",
                        "Clause", "Control", "Objective",
                        "System", "Process", "Data", "Project", "Facility", "Market", "Group",
                        #"Person" CORE-1170
                        ]

    project_map_to_lhn = ["Vendor",
                        "Program", "Regulation", "Contract", "Policy", "Standard", "Section",
                        "Clause", "Control", "Objective", 
                        "System", "Process", "Data", "Product", "Facility", "Market", "Group",
                        #"Person" CORE-1170
                          ]

    facility_map_to_lhn = ["Vendor",
                        "Program", "Regulation", "Contract", "Policy", "Control", "Objective", 
                        "System", "Process", "Data", "Standard", "Section", "Clause",
                        "Project", "Product", "Market", "Group",
                         #"Person" CORE-1170
                          ]


    market_map_to_lhn= ["Vendor",
                        "Standard", "Section", "Clause", "Control",
                        "Program", "Regulation", "Contract", "Policy", "Objective",
                        "System", "Process", "Data", "Product", "Project", "Facility", "Group",
                        #"Person" CORE-1170
                        ]

    org_group_map_to_lhn= ["Vendor",
                            "Standard", "Section", "Clause", 
                            "Program", "Regulation", "Contract", "Policy", "Control", "Objective", 
                            "System", "Process", "Data", "Product", "Project", "Facility", "Market",
                            #"Person" CORE-1170
                           ]


#WIDGET GOVERNANCE OBJECTS
    regulation_map_to_widget = ["Vendor",
                                "Section", "Program",  "Org_Group", "Person",
                                "System", "Process", "Data_Asset", "Product", "Project", "Facility", "Market"
                                ]

    contract_map_to_widget = [ "Vendor",                             
                               "Project", "Facility", "Market", "Org_Group", "System",  "Data_Asset", "Product", 
                               "Clause", "Objective", "Control", "Process", "Person", "Program", 
                          ]

    standard_map_to_widget = ["Vendor",
                            "Section", "Objective", "Control", "Person", 
                            "Program", "System", "Process", "Data_Asset", "Product", "Project", "Facility", "Market", "Org_Group"
                             ]

    policy_map_to_widget = ["Vendor",
                            "Section", "Objective", "Control", "Program", "Person",
                            "System", "Process", "Data_Asset", "Product", 
                            "Project", "Facility", "Market", "Org_Group"                            
                          ]

    control_map_to_widget = ["Vendor",
                            "Objective","Org_Group", "Program", "Regulation", "Clause", "Section", "Standard", 
                            "Person", "System", "Process", "Data_Asset", "Product", "Project", "Facility", 
                            "Market", "Contract", "Policy"
                          ]
    objective_map_to_widget = ["Vendor",
                            "Program", "Regulation", "Contract", "Policy", "Standard", "Section", "Clause", "Market", 
                            "Control", "System", "Process", "Product", "Project", "Facility", "Data_Asset", "Org_Group", "Person"
                            ]

#WIDGET BUSINESS OBJECTS

    system_map_to_widget = ["Vendor",
                            "Program", "Regulation", "Contract", "Policy", "Standard", "Section", "Clause",
                             "Objective", "Control", "Process", "Data_Asset", "Product", "Facility", "Project",
                             "Market", "Org_Group", "Person"
                             ]

    vendor_map_to_widget =  [
                            "Facility", "Program",
                            "Objective", "Contract", "Standard", "Person", "Regulation", "Policy", 
                            "Control", "System", "Process", "Data_Asset", "Product", "Project", 
                            "Clause", "Market",
                            "Org_Group", "Section"
                           ] 

    process_map_to_widget = ["Vendor",
                            "Program", "Regulation", "Contract", "Policy", "Standard", "Section", "Clause",
                            "Objective", "Control", "System", "Product", "Project", "Facility", "Market", "Org_Group", "Person"
                             ]

    data_asset_map_to_widget = ["Vendor",
                                "Program", "Regulation", "Contract", "Policy", "Standard", "Section", "Clause",
                                "Objective", "Control", "System", "Process", "Product", "Project", "Facility", "Market", "Org_Group", "Person"
                                ]

    product_map_to_widget = ["Vendor",
                            "Section", 
                            "Program", "Regulation", "Contract", "Policy", "Standard", "Clause", "Objective", 
                            "Control", "System", "Process", "Project", "Facility", "Market", "Data_Asset", "Org_Group", "Person"
                             ]

    project_map_to_widget = ["Vendor",
                            "Program", "Regulation", "Contract", "Policy", "Standard", "Section", "Clause",
                            "Objective", "Control", "System", "Process", "Data_Asset", "Product", "Facility", 
                            "Market", "Org_Group", "Person"
                             ]

    facility_map_to_widget = ["Vendor",
                                "Program", "Regulation", "Objective", "Contract", "Policy", "Standard", "Section", "Clause", "Control", 
                                "System", "Process", "Data_Asset", "Product", "Project", "Market", "Org_Group", "Person"
                              ]

    market_map_to_widget = ["Vendor",
                            "Program", "Regulation", "Contract", "Policy", "Standard", "Section", "Clause", "Objective", 
                            "Control", "System", "Process", "Product", "Project", "Facility", "Data_Asset", "Org_Group", "Person"
                            ]

    org_group_map_to_widget = [ "Vendor",
                                "Program", "Regulation", "Contract", "Policy", "Standard", "Section", "Clause",
                                "Objective", "Control", "System", "Process", "Product", "Project", "Facility", 
                                "Market", "Data_Asset", "Person"
                               ]

    objective_title = ["ARTY Objective 1", "ARTY Objective 2", "ARTY Objective 3"]

    objective_description = ["the Text of the section text is auto copied to the Objective description", "multiple objectives per sesction is easily supported and working", "creation of a control under the section works as well"]
