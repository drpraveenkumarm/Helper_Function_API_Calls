import pandas as pd
import requests
from pandas.io.json import json_normalize
from requests.auth import HTTPBasicAuth
authentication = HTTPBasicAuth('','')

def get_pref_symbol(string, version = "v1_6_5_patch_2"):
    url = "https://preview.nferx.com/nucleus-api/v2/get_entities_for_token?fold_related=1&token_info=attributes%2Curl%2Chighest_priority_type%2Csources_claiming_synonym&token_sources=1&?"
    params = {
        "token" : string,
        "version" : version
    }
    x = requests.get(url, params=params,auth = authentication)
    result = pd.json_normalize(x.json()["result"])
    return result


def get_pref_symbol_multi(token):
    loop_list = []
    if len(get_pref_symbol(token)["data"][0]) >0:
        response = get_pref_symbol(token)["data"][0][0]["tokens"]
        for i, value in enumerate(response):
            if response[value]["highest_priority_type"] == "PREF_SYMBOL":
                loop_list.append(value.upper())
    return loop_list 

token = "epidermal growth factor receptor"

get_pref_symbol_multi(token)
