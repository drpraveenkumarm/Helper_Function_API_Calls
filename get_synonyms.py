import pandas as pd
import requests
from pandas.io.json import json_normalize
from requests.auth import HTTPBasicAuth
authentication = HTTPBasicAuth(username="",
                               password="")

def get_synonyms_result(string,require_empty_df = False):
    url = "https://preview.nferx.com/nucleus-api/v2/get_entities_for_token?fold_related=1&token_info=attributes%2Curl%2Chighest_priority_type%2Csources_claiming_synonym&token_sources=1&?"
    params = {
        "token": string
    }
    x = requests.get(url, params=params, auth = authentication)
    df = pd.json_normalize(x.json()["result"])
    if len(df["data"][0]) >= 1:
        terms = list(df["data"][0][0]["tokens"].keys())
        cols = ["Term","Property","Good_Synonym"]
        lst = []
        for i in range(0,len(terms)):
            lstinloop = []
            lstinloop.append(terms[i])
            lstinloop.append(df["data"][0][0]["tokens"][list(df["data"][0][0]["tokens"].keys())[i]]["highest_priority_type"])
            lstinloop.append(df["data"][0][0]["tokens"][list(df["data"][0][0]["tokens"].keys())[i]]["attributes"]["good_synonym"])
            lst.append(lstinloop)
        return_df = pd.DataFrame(lst, columns=cols)
        return_df.index += 1
        return return_df
    else:
        if require_empty_df == True:
            cols = ["Term","Property","Good_Synonym"]
            lst = []
            return_df = pd.DataFrame(lst, columns=cols)
            return return_df
        else:
            not_recognized = "NOT_RECOGNIZED"
            print(not_recognized)   
            
final_list = []
for i, disease in enumerate(list_diseases):
    list_loop = []
    if len(get_synonyms_result(disease,require_empty_df=True)["Term"]) <1:
        print("I am skipping the disease ", disease)
    else:
        df_output = get_synonyms_result(disease)
    print("Looking at", disease)
    list_loop.append(disease)
    list_loop.append(df_output[df_output.Good_Synonym == True].Term.to_list())
    final_list.append(list_loop)
    
    
pd.DataFrame(final_list).to_csv("Disease_Synonyms.csv")
