'''
Created on Jul 20, 2013

@author: diana.tzinov

'''

from Elements import Elements

class GRCObject(object):
    elem = Elements()
    """
    program_elements = {
                        "title":elem.object_title,
                        "owner":elem.object_owner, 
                        "url":elem.object_url, 
                        "code":elem.object_code, 
                        "organization":elem.object_organization, 
                        "scope":elem.object_scope}
                        
                        
    program_values = {
                      'title':"",  
                      'owner':"testrecip@gmail.com", 
                      'url': "http://www.google.com", 
                      'code':"PCI", 
                      'organization': "ORG", 
                      'scope': ""}
    """
    
        #CONTRACT
    
    contract_elements = {
                        "title":elem.object_title,    
                        "description":elem.object_description,
                        "url":elem.object_url,
                        "code":elem.object_code
                        } 
 
    
    
    contract_values = {
                      'title':"",  
                      "description":"",
                      'url': "http://www.google.com", 
                      "code":"auto-populated-code"
                      }
    
        
    #CONTROL
    control_elements = {
                        "title":elem.object_title,    
                        "description":elem.object_description,
                        "url":elem.object_url,
                        "code":elem.object_code
                        } 
 
    
    
    control_values = {
                      'title':"",  
                      "description":"",
                      'url': "http://www.google.com", 
                      "code":"auto-populated-code"
                      }
    
    
    
    #DATA ASSET
    data_asset_elements = {
                        "title":elem.object_title,    
                        "description":elem.object_description,
                        "url":elem.object_url,
                        "code":elem.object_code
                        } 
 
    
    
    data_asset_values = {
                      'title':"",  
                      "description":"",
                      'url': "http://www.google.com", 
                      "code":"auto-populated-code"
                      }
    
    #FACITY
    facility_elements = {
                        "title":elem.object_title,    
                        "description":elem.object_description,
                        "url":elem.object_url,
                        "code":elem.object_code
                        } 
 
    
    
    facility_values = {
                      'title':"",  
                      "description":"",
                      'url': "http://www.google.com", 
                      "code":"auto-populated-code"
                      }
    
    #MARKET
    market_elements = {
                        "title":elem.object_title,    
                        "description":elem.object_description,
                        "url":elem.object_url,
                        "code":elem.object_code
                        } 
 
    
    
    market_values = {
                      'title':"",  
                      "description":"",
                      'url': "http://www.google.com", 
                      "code":"auto-populated-code"
                      }
    
    
    #ORGGROUPS
    org_group_elements = {
                        "title":elem.object_title,    
                        "description":elem.object_description,
                        "url":elem.object_url,
                        "code":elem.object_code
                        } 
 
    
    
    org_group_values = {
                      'title':"",  
                      "description":"",
                      'url': "http://www.google.com", 
                      "code":"auto-populated-code"
                      }
        #POLICY
        
    policy_elements = {
                        "title":elem.object_title,  
                        "description":elem.object_description,   
                        "url":elem.object_url,
                        "code":elem.object_code
                        } 
 
    
    
    policy_values = {
                      'title':"",  
                      "description":"",
                      'url': "http://www.google.com", 
                       "code":"auto-populated-code"
                      }
    
    
    #PROCESS
        
    process_elements = {
                        "title":elem.object_title,  
                        "description":elem.object_description,   
                        "url":elem.object_url,
                        "code":elem.object_code
                        } 
 
    
    
    process_values = {
                      'title':"",  
                      "description":"",
                      'url': "http://www.google.com", 
                      "code":"auto-populated-code"
                      }
    
    #POLICY
        
    product_elements = {
                        "title":elem.object_title,  
                        "description":elem.object_description,   
                        "url":elem.object_url,
                        "code":elem.object_code
                        } 
 
    
    
    product_values = {
                      'title':"",  
                      "description":"",
                      'url': "http://www.google.com", 
                      "code":"auto-populated-code"
                      }
    
    
    #PROGRAM
    
    
    program_elements = {
                        "title":elem.object_title,    
                        "description":elem.object_description,
                        "url":elem.object_url,
                        "code":elem.object_code
                        } 
 
    
    
    program_values = {
                      'title':"",  
                      "description":"",
                      'url': "http://www.google.com", 
                      "code":"auto-populated-code"
                      }
    

    #PROJECT
        
    project_elements = {
                        "title":elem.object_title,  
                        "description":elem.object_description,   
                        "url":elem.object_url,
                        "code":elem.object_code
                        } 
 
    
    
    project_values = {
                      'title':"",  
                      "description":"",
                      'url': "http://www.google.com", 
                      "code":"auto-populated-code"
                      }

    
    #REGULATION
    regulation_elements = {
                        "title":elem.object_title,    
                        "description":elem.object_description,
                        "url":elem.object_url,
                        "code":elem.object_code
                        } 
 
    
    
    regulation_values = {
                      'title':"",  
                      "description":"",
                      'url': "http://www.google.com", 
                      "code":"auto-populated-code"
                      }
    
    
  
    #System
        
    system_elements = {
                        "title":elem.object_title,  
                        "description":elem.object_description,   
                        "url":elem.object_url,
                        "code":elem.object_code
                        } 
 
    
    
    system_values = {
                      'title':"",  
                      "description":"",
                      'url': "http://www.google.com", 
                      "code":"auto-populated-code"
                      }
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    """
    
    
    
    policy_elements = {
                        "title":elem.object_title,  
                        "owner":elem.object_owner, 
                        "url":elem.object_url, 
                        "code":elem.object_code, 
                        "kind":elem.object_kind
                       }
    policy_values = {
                      'title':"",  
                      'owner':"testrecip@gmail.com", 
                      'url': "http://www.google.com", 
                      'code':"PCI", 
                      'kind': "Company Policy"}
    
    regulation_elements = {
                        "title":elem.object_title,  
                        "owner":elem.object_owner, 
                        "url":elem.object_url, 
                        "code":elem.object_code 
                       }
    regulation_values = {
                      'title':"",  
                      'owner':"testrecip@gmail.com", 
                      'url': "http://www.google.com", 
                      'code':"PCI"}
    
    contract_elements = {
                        "title":elem.object_title,  
                        "owner":elem.object_owner, 
                        "url":elem.object_url, 
                        "code":elem.object_code 
                       }
    contract_values = {
                      'title':"",  
                      'owner':"testrecip@gmail.com", 
                      'url': "http://www.google.com", 
                      'code':"PCI"}
    
    
    regulation = []
    contract =[]
    

    """