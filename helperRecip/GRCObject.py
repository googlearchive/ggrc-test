'''
Created on Jul 20, 2013

@author: diana.tzinov

'''

from Elements import Elements

class GRCObject(object):
    elem = Elements()
    
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
    

    