import requests
import json
import os

BASE = "http://immvmdidata02.d.immlan.unizh.ch/test"
USERNAME = "res_admin"
PASSWORD = "imm.FoEg.567"

s = requests.Session()
r = s.post(f"{BASE}/api/login", json={
    "username": USERNAME,
    "password": PASSWORD
})

token = r.json()["token"]

headers = {
    "Authorization":        f"Bearer {token}",
    "Content-Type":         "application/json",
    "Accept":               "application/json",
    "Didata-Project-Id":    "1"
}

payload1 = {
    "data": [
        {
            "id": 55127,
            "Status": 518,
        },
        {
            "id": 55128,
            "Status": 518
        },
        {
            "id": 55129,
            "Status": 518
        }
    ],
    "options": {
        "identify_entities_by": ["id"], # how to find the row/entity you want to update
        "upsert": False                 # what to do if it cannot find that row/entity
    }
}

payload2 = {
    "data": [
        {
            "id": 55127,
            "Extracted_DNA_ng_ul": None,
            "Kit_name_DNA_quantification_fc": None,
            "Quantification_date": None,
            "output_volume": 100,
            "Status": 85,
        },
        {
            "id": 55128,
            "Extracted_DNA_ng_ul": None,
            "Kit_name_DNA_quantification_fc": None,
            "Quantification_date": None,
            "output_volume": 100,
            "Status": 85
        },
        {
            "id": 55129,
            "Extracted_DNA_ng_ul": None,
            "Kit_name_DNA_quantification_fc": None,
            "Quantification_date": None,
            "output_volume": 100,
            "Status": 85
        }
    ],
    "options": {
        "identify_entities_by": ["id"], # how to find the row/entity you want to update
        "upsert": False                 # what to do if it cannot find that row/entity
    }
}

payload3 = {
    "data": [
        {
            "id": 55127,
            "ng_ul": None,
            "ng_ul_pool_2": None,
            "ng_ul_pool_3": None,
            "Is_pooled": None,
            "Kit_Name_Post_PCR_Visualization": None,
            "Post_PCR_date": None,
            "output_volume": 98,
            "Status": 518
        },
        {
            "id": 55128,
            "ng_ul": None,
            "ng_ul_pool_2": None,
            "ng_ul_pool_3": None,
            "Is_pooled": None,
            "Kit_Name_Post_PCR_Visualization": None,
            "Post_PCR_date": None,
            "output_volume": 98,
            "Status": 518
        },
        {
            "id": 55129,
            "ng_ul": None,
            "ng_ul_pool_2": None,
            "ng_ul_pool_3": None,
            "Is_pooled": None,
            "Kit_Name_Post_PCR_Visualization": None,
            "Post_PCR_date": None,
            "output_volume": 98,
            "Status": 518
        }
    ],
    "options": {
        "identify_entities_by": ["id"], # how to find the row/entity you want to update
        "upsert": False                 # what to do if it cannot find that row/entity
    }
}


# 85, DNA Quantification
# 518, 16S PCR Quantification
# 529, 16S Library Quantification

r = s.put(f"{BASE}/api/entities/batch", headers=headers, json=payload3)

print(r.status_code)
print(r.json())


'''
Kit_name_DNA_quantification_fc
559 -> Qubit ssDNA Assay Kit
558 -> Qubit 1X dsDNA BR Assay Kit
557 -> Qubit 1X dsDNA HS Assay Kit

'''

