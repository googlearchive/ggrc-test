'''
Created on Jul 20, 2013

@author: diana.tzinov

'''

from Elements import Elements

class GRCObject(object):
    elem = Elements()
    
    #program_elements = {"title":elem.object_title, "description":elem.object_description, "owner":elem.object_owner, "url":elem.object_url, "code":elem.object_code, "organization":elem.object_organization, "scope":elem.object_scope}
    program_elements = {"title":elem.object_title}
    #program_values = {'title':"", 'description':"", 'owner':"", 'url': "http://www.cnn.com", 'code':"ABCD", 'organization': "ORG", 'scope': ""}
    program_values = {'title':""}
    
    policy = []
    
    regulation = []
    contract =[]
    

    