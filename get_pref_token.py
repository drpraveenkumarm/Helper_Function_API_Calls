import pandas as pd
import requests
from pandas.io.json import json_normalize
from requests.auth import HTTPBasicAuth
authentication = HTTPBasicAuth('','')


def get_pref_token(string, version = "v1_6_5_patch_1"):
    url = "https://preview.nferx.com/nucleus-api/v2/get_entities_for_token?fold_related=1&token_info=attributes%2Curl%2Chighest_priority_type%2Csources_claiming_synonym&token_sources=1&?"
    params = {
        "token": string,
        "version" : version
    }
    x = requests.get(url, params=params, auth = authentication)
    df = pd.json_normalize(x.json()["result"])
    lst = []
    if len(df["data"][0])>=1:
        lst.append(df["query_token"][0])
        lst.append(df["data"][0][0]["PREFERRED_TOKEN"])
        return lst
    else:
        lst.append(string)
        lst.append("No Result")
        return lst

get_pref_token("atezolizumab")


f = open("antibody_FDA_approved.txt","r")
list_tokens = f.read().split()

list_output = []
for i in range(0,len(list_tokens)):
    list_iter = get_pref_token(list_tokens[i], version="v1_6_4_patch_1")
    list_output.append(list_iter)

pd.DataFrame(list_output,columns=["Search_Token","Pref_Name"]).to_csv("Therapeutic_antibody.csv")
