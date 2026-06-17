'''
Qubit E2E Test Cases
case 1: DNA
- Success Scenario
- Exception Handling

case 2: PCR (single CSV File only)
- Success Scenario
- Exception Handling

case 3: PCR (multiple CSV Files)
- Success Scenario
- Exception Handling

case 4: LIB
- Success Scenario
- Exception Handling

case 5: LIB (missing samples in DiData)
- Success Scenario
- Exception Handling

For all Cases
Step 1: Upload Dummy Data to DiData
Step 2: Create CSV Files for Qubit with Dummy Data
Step 3: Run MasterController and check if data is uploaded to correct step in DiData
Step 4: Check Uploaded Data in DiData and compare with CSV Files
Step 5: Check if files are deleted after processing


FA E2E Test Cases

'''

import os
import json
import requests
from dotenv import load_dotenv
API_BASE_URL = os.getenv("API_BASE_URL")

def response_check(r):
    if r.status_code == 200:
        print("Request successful")
    else:
        print("STATUS:", r.status_code)
        print("TEXT:", r.text)

load_dotenv()
s = requests.Session()
r = s.post(f"{API_BASE_URL}/api/login", json={
    "username": os.getenv("DIDATA_USERNAME"),
    "password": os.getenv("DIDATA_PASSWORD")
})

print(f"Login: {r.status_code}")
token = r.json().get("token")

headers = {
        "Authorization":     f"Bearer {token}",
        "Content-Type":      "application/json",
        "Accept":            "application/json",
        "Didata-Project-Id": "1"
}

choice = 2

if choice == 1:
    # Upload Dummy Data
    print("Uploading Dummy Data for DNA Test Case")
    payload = {
        "data": [
            {
                "entitytype_id": 11,
                "Sample__Id": "TEST-001D1",
                "output_volume": 100,
                "Status": 85
            },
            {
                "entitytype_id": 11,
                "Sample__Id": "TEST-002D1",
                "output_volume": 100,
                "Status": 85
            },
            {
                "entitytype_id": 11,
                "Sample__Id": "TEST-003D1",
                "output_volume": 100,
                "Status": 85
            },
            ]
    }

    r = s.post(f"{API_BASE_URL}/api/entities/batch", headers=headers, json=payload)
    response_check(r)
    
elif choice == 2:
    # Upload Dummy Data
    print("Resetting Dummy Data for DNA Test Case")
    payload = {
        "data": [
            {
                "id": 63124,
                "Extracted_DNA_ng_ul": None,
                "Kit_name_DNA_quantification_fc": None,
                "Quantification_date": None,
                "output_volume": 100,
            },
            {
                "id": 63125,
                "Extracted_DNA_ng_ul": None,
                "Kit_name_DNA_quantification_fc": None,
                "Quantification_date": None,
                "output_volume": 100,
            },
            {
                "id": 63126,
                "Extracted_DNA_ng_ul": None,
                "Kit_name_DNA_quantification_fc": None,
                "Quantification_date": None,
                "output_volume": 100,
            }
            ],
        "options": {
            "identify_entities_by": ["id"],
            "upsert": False
        }
    }
    r = s.put(f"{API_BASE_URL}/api/entities/batch", headers=headers, json=payload)
    response_check(r)

if choice == 3:
    # Upload Dummy Data
    print("Uploading Dummy Data for PCR Test Case")
    payload = {
        "data": [
            {
                "entitytype_id": 11,
                "Sample__Id": "TEST-001PD1",
                "output_volume": 100,
                "Status": 518
            },
            {
                "entitytype_id": 11,
                "Sample__Id": "TEST-002PD1",
                "output_volume": 100,
                "Status": 518
            },
            {
                "entitytype_id": 11,
                "Sample__Id": "TEST-003PD1",
                "output_volume": 100,
                "Status": 518
            },
            ]
    }

    r = s.post(f"{API_BASE_URL}/api/entities/batch", headers=headers, json=payload)
    response_check(r)

elif choice == 4:
    # Upload Dummy Data
    print("Resetting Dummy Data for PCR Test Case")
    payload = {
        "data": [
            {
                "id": 63127,
                "Kit_name_DNA_Post_PCR": None,
                "Post_PCR_date": None,
                "Is_pooled": None,
                "output_volume": 100,
                "ng_ul": None,
                "ng_ul_pool_2": None,
                "ng_ul_pool_3": None,
            },
            {
                "id": 63128,
                "Kit_name_DNA_Post_PCR": None,
                "Post_PCR_date": None,
                "Is_pooled": None,
                "output_volume": 100,
                "ng_ul": None,
                "ng_ul_pool_2": None,
                "ng_ul_pool_3": None,
            },
            {
                "id": 63129,
                "Kit_name_DNA_Post_PCR": None,
                "Post_PCR_date": None,
                "Is_pooled": None,
                "output_volume": 100,
                "ng_ul": None,
                "ng_ul_pool_2": None,
                "ng_ul_pool_3": None,
            }
            ],
        "options": {
            "identify_entities_by": ["id"],
            "upsert": False
        }
    }
    r = s.put(f"{API_BASE_URL}/api/entities/batch", headers=headers, json=payload)
    response_check(r)
    
if choice == 5:
    # Upload Dummy Data
    print("Uploading Dummy Data for LIB Test Case")
    payload = {
        "data": [
            {
                "entitytype_id": 1,
                "Sample__Id": "TEST-001L1",
                "Status": 529
            },
            {
                "entitytype_id": 1,
                "Sample__Id": "TEST-002L1",
                "Status": 529
            },
            {
                "entitytype_id": 1,
                "Sample__Id": "TEST-003L1",
                "Status": 529
            },
            ]
    }

    r = s.post(f"{API_BASE_URL}/api/entities/batch", headers=headers, json=payload)
    response_check(r)
    
elif choice == 6:
    # Upload Dummy Data
    print("Resetting Dummy Data for LIB Test Case")
    payload = {
        "data": [
            {
                "id": 63130,
                "Library_ng_ul": None,
                "Kit_Name_16s_Library_Quant": None,
                "16S_library_quantification_date": None,
                "Volume_taken_for_16s_library_quantification_": None
            },
            {
                "id": 63131,
                "Library_ng_ul": None,
                "Kit_Name_16s_Library_Quant": None,
                "16S_library_quantification_date": None,
                "Volume_taken_for_16s_library_quantification_": None
            },
            {
                "id": 63132,
                "Library_ng_ul": None,
                "Kit_Name_16s_Library_Quant": None,
                "16S_library_quantification_date": None,
                "Volume_taken_for_16s_library_quantification_": None
            }
            ],
        "options": {
            "identify_entities_by": ["id"],
            "upsert": False
        }
    }
    r = s.put(f"{API_BASE_URL}/api/entities/batch", headers=headers, json=payload)
    response_check(r)
    
elif choice == 7:
    # Upload Dummy Data
    print("Resetting Dummy Data for FA PCR Test Case")
    payload = {
        "data": [
            {
                "id": 62040, # <-- Added comma
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62041, # <-- Added comma
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62042,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62043,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62044,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62045,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62046,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62047,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62048,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62049,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62050,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62051,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62052,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62053,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62054,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62055,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62056,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62057,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62058,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62059,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62060,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62061,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62062,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62063,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62064,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62065,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62066,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62067,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62068,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62069,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62070,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62071,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62072,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62073,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62074,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62075,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62076,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62077,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62078,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62079, # <-- Added comma
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62080,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62081, # <-- Added comma
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62082,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62083,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62084,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            },
            {
                "id": 62085,
                "Need_Human_Validation": None,
                "Fragment_size_bp_options": None,
                "Fragment_Size_bp_DNA": None,
                "Is_visualized": None,
                "Visualization_date": None,
                "Kit_Name_Post_PCR_Visualization": None,
                "Method": None,
            } # Removed unnecessary trailing comma here
        ],
        "options": {
            "identify_entities_by": ["id"],
            "upsert": False
        }
    }
    r = s.put(f"{API_BASE_URL}/api/entities/batch", headers=headers, json=payload)
    response_check(r)