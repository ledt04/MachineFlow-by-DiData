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
'''
r = s.post(f"{BASE}/api/entities", headers=headers, json={
    "entitytype_id": 11,          # DNA
    "Sample__Id": "TEST-001",     # your sample ID
    "Extracted_DNA_ng_ul": "12.5", # Qubit value
    "Status": 85,                 # places it on DNA Quantification node
})
'''
r = s.delete(f"{BASE}/api/entities/53003", headers=headers)

print(r.status_code) 
# print(json.dumps(r.json(), indent=4))
print(r.json())