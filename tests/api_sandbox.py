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
r = s.put(f"{BASE}/api/entities/53004", headers=headers, json={
    "Extracted_DNA_ng_ul": "15.4",
    "Kit_name_DNA_quantification_fc": 559,
    "Quantification_date": "25-02-2025 10:36:53",
    "output_volume" : 40
})
'''
payload = {
    "data": [
        {
            "id": 53004,
            "Extracted_DNA_ng_ul": "14.5",
            "Kit_name_DNA_quantification_fc": 559,
            "Quantification_date": "25-02-2025 10:36:53",
            "output_volume": 100
        },
        {
            "id": 53005,
            "Extracted_DNA_ng_ul": "16.5",
            "Kit_name_DNA_quantification_fc": 557,
            "Quantification_date": "25-02-2025 10:36:53",
            "output_volume": 100
        }
    ],
    "options": {
        "identify_entities_by": ["id"], # how to find the row/entity you want to update
        "upsert": False                 # what to do if it cannot find that row/entity
    }
}

r = s.put(f"{BASE}/api/entities/batch", headers=headers, json=payload)


print(r.status_code)
print(r.json())

s.post(f"{BASE}/api/logout", headers=headers)
'''
Kit_name_DNA_quantification_fc
559 -> Qubit ssDNA Assay Kit
558 -> Qubit 1X dsDNA BR Assay Kit
557 -> Qubit 1X dsDNA HS Assay Kit

'''



'''
r = s.get(f"{BASE}/api/entities", headers=headers)

samples = []

for entity in r.json():
    if entity.get("Status") == 85:
        samples.append({
            "sample_name": entity.get("Sample__Id"),
            "sample_id": int(entity.get("id")),  # make sure it's numeric
            "created_at": entity.get("created_at")
        })

# Sort by sample_id first
samples = sorted(samples, key=lambda x: x["sample_id"])

grouped_samples = []
current_group = []

for sample in samples:
    if not current_group:
        current_group.append(sample)
    else:
        prev_id = current_group[-1]["sample_id"]
        curr_id = sample["sample_id"]

        if curr_id - prev_id == 1:
            current_group.append(sample)
        else:
            grouped_samples.append(current_group)
            current_group = [sample]

# Add the last group
if current_group:
    grouped_samples.append(current_group)

# Example print showing both sample name and ID
for i, group in enumerate(grouped_samples, 1):
    sample_info = [(x['sample_name'], x['sample_id']) for x in group]
    print(f"Group {i}: {sample_info}")
    '''