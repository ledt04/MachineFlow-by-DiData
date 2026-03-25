from src.config.settings import API_BASE_URL, get_kit_name_dna_quantification_fc_number
from src.utils.error_handling import handle_find_data_group_return
from src.utils.auth import get_headers
from datetime import datetime
import json

def find_data_group(csv, didata):
    target_group = []
    
    for group in didata:
        for sample in group:
            if sample["sample_id"] == csv["Sample Name"].iloc[0]:
                target_group = group
                break
        if target_group:
            break
    
    handle_find_data_group_return(target_group, csv)
    return target_group

def upload_dna(session, csv, didata):
    # get id from first sample name
    # find id group and match
    target_group = find_data_group(csv, didata)
    
    # Qubit Raw Data -> DiData Names
    # Test Date -> Quantification Date
    # Assay Name -> Kit Name DNA Quantification
    # Sample Name -> Sample ID
    # Original Sample -> Extracted DNA
    # Sample Volume (uL) -> DNA Volume(ul) = DNA Volume(ul) - Sample Volume(uL)
    # Move to next node
    
    payload = {
        "data": [],
        "options": {
            "identify_entities_by": ["id"], # how to find the row/entity you want to update
            "upsert": False                 # what to do if it cannot find that row/entity
        }
    }
    
    for i in range(len(target_group)):
        payload["data"].append(
            {
            "id": target_group[i]["id"],
            "Extracted_DNA_ng_ul": str(csv["Original Sample Conc."][i]),
            "Kit_name_DNA_quantification_fc": get_kit_name_dna_quantification_fc_number(csv["Assay Name"][i]),
            "Quantification_date": datetime.strptime(csv["Test Date"][i], "%d/%m/%Y %I:%M:%S %p").strftime("%d-%m-%Y %H:%M:%S"),
            "output_volume": int(target_group[i]["dna_volume"] - csv["Sample Volume (uL)"][i])
            }
        )
        
    response = session.put(f"{API_BASE_URL}/api/entities/batch", headers=get_headers(), json=payload)
    return response

def upload_pcr(session, csv, didata):
    # get id and find group
    target_group = find_data_group(csv, didata)
    
    # Qubit Raw Data -> DiData Names
    # PCR Quantification
    # Test Date -> Post PCR date
    # Assay Name -> Kit Name DNA Post PCR
    # Always 3 different pools, Always. -> could be more Excel files

    # Add in Post PCR Visualization % CLean up for Entities
    # in case -> no pooled -> must be repeated
    # if value under 1 -> not pooled

    # Option: Create Action for Is Pooled or not mechanism

    payload = {
        "data": [],
        "options": {
            "identify_entities_by": ["id"], # how to find the row/entity you want to update
            "upsert": False                 # what to do if it cannot find that row/entity
        }
    }
    
    for i in range(len(target_group)):
        payload["data"].append(
            {
            "id": target_group[i]["id"],
            "ng_ul": str(csv["Original Sample Conc."][i]),
            "ng_ul_pool_2": str(csv["Original Sample Conc."][i]),
            "ng_ul_pool_3": str(csv["Original Sample Conc."][i]),
            "Kit_name_DNA_Post_PCR": get_kit_name_dna_quantification_fc_number(csv["Assay Name"][i]),
            "Post_PCR_date": datetime.strptime(csv["Test Date"][i], "%d/%m/%Y %I:%M:%S %p").strftime("%d-%m-%Y %H:%M:%S"),
            "Is_pooled": True,
            "output_volume": int(target_group[i]["dna_volume"] - csv["Sample Volume (uL)"][i])
            }
        )
        
    response = session.put(f"{API_BASE_URL}/api/entities/batch", headers=get_headers(), json=payload)
    return response

def upload_lib(session, csv, didata):
    pass