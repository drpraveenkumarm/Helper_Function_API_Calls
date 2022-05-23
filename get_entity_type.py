import pandas as pd
import requests
from pandas.io.json import json_normalize
from requests.auth import HTTPBasicAuth
authentication = HTTPBasicAuth('','')

def get_entity_type(string,other_entity_type = False, version = "v1_6_5_patch_1"):
    url = "https://preview.nferx.com/nucleus-api/v2/get_entities_for_token?fold_related=1&token_info=attributes%2Curl%2Chighest_priority_type%2Csources_claiming_synonym&token_sources=1&?"
    params = {
        "token" : string,
        "version" : version
    }
    x = requests.get(url, params=params,auth = authentication)
    result = pd.json_normalize(x.json()["result"])
    if other_entity_type == False:
        if len(result["data"][0]) >= 1:
            entity_type = result["data"][0][0]["entity_type"]
        else:
            entity_type = "NOT_RECOGNIZED"
        return entity_type
    elif other_entity_type == True:
        if len(result["data"][0]) >= 1:
            lstinloop = []
            lstinloop.append(result["data"][0][0]["entity_type"])
            lstinloop.append(result["data"][0][0]["other_entity_types"])
        else:
            lstinloop = "NOT_RECOGNIZED"
        return lstinloop


get_entity_type("pembrolizumab",other_entity_type=True, version = "v1_6_4_patch_1")


get_entity_type("heart failure")

f = open("testcases_FDA_Approved_2020.txt","r")
listItems = f.read().splitlines()

for i in range(0, len(listItems)):
    print(listItems[i],get_entity_type(listItems[i]))
    
f = open("testcases_Laboratory_ProcedureORLab_Data.txt","r")
listItems = f.read().splitlines()

for i in range(0, len(listItems)):
    print(listItems[i],get_entity_type(listItems[i],other_entity_type=True))
