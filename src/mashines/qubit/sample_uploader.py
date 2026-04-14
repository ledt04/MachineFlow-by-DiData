from src.config.settings import API_BASE_URL, get_kit_name_dna_quantification_fc_number, save_target_group, get_target_group, get_state_id_by_name
from src.utils.error_handling import handle_find_data_group_return, handle_qubit_and_didata_amount_check
from src.utils.auth import get_headers
from datetime import datetime
import json
import re

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

def remove_standard_from_csv(csv):
    std_re = re.compile(r"^(?:\d*)(std|std|sntdrd|stndrd|stand|stad|standard)[_\-\s]*(\d*)$", re.IGNORECASE)
    
    # remove standard from df
    for i, sample in enumerate(csv["Sample Name"]):
        if std_re.match(sample):
            csv = csv.drop(i)
    
    return csv

def upload_dna(session, csv, didata):
    csv = remove_standard_from_csv(csv)
    # get id from first sample name
    # find id group and match
    target_group = find_data_group(csv, didata)
    handle_qubit_and_didata_amount_check(csv, target_group, genomic="DNA")
    save_target_group(target_group) # Save the target group for later use in LIB uploads
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
        dna_vol = target_group[i]["dna_volume"] or 0
        sample_vol = csv["Sample Volume (uL)"][i] or 0
        
        payload["data"].append(
            {
            "id": target_group[i]["id"],
            "Extracted_DNA_ng_ul": str(csv["Original Sample Conc."][i]),
            "Kit_name_DNA_quantification_fc": get_kit_name_dna_quantification_fc_number(csv["Assay Name"][i]),
            "Quantification_date": datetime.strptime(csv["Test Date"][i], "%d/%m/%Y %I:%M:%S %p").strftime("%d-%m-%Y %H:%M:%S"),
            "output_volume": int(dna_vol - sample_vol),
            "Status": get_state_id_by_name("DNA Quantification")
            }
        )
        
            # Status
            # 85, DNA Quantification
            # 91, 16S PCR
        
    response = session.put(f"{API_BASE_URL}/api/entities/batch", headers=get_headers(), json=payload)
    return response

def helper_monolithic_pcr(csv, didata):
    
    # New Logic
    # Check if didata sample have any pools in there
    # multiply amount of samples in didata times 3
    # how many samples in didata of the ng/ul, ng/ul pool2, ng/ul pool3 are existing?
    # total amount = amount didata * 3
    # Example: if 2 already exist in didata, and total amount is 9, we know theres 3 samples for each pool
    # so we know the first sample of the csv is the number 3 of the ng/ul pool1
    
    # check if 3 diffrent pools exist
    didata_sample_count = len(didata)
    csv_sample_count = len(csv["Sample Name"])
    if csv_sample_count / didata_sample_count == 3:
        print(f"Qubit Sample Quantitiy: {csv_sample_count}")
        print(f"DiData Sample Quantitiy: {didata_sample_count}")
    

    for i, value in enumerate(csv["Original Sample Conc."]):
        pool_group = i // 3 
        row_idx = i % 3

        match pool_group:
            case 0:
                column = "ng_ul"
            case 1:
                column = "ng_ul_pool_2"
            case 2:
                column = "ng_ul_pool_3"
            case _:
                column = "unknown_pool" # Safety fallback

        csv.at[row_idx, column] = value # .at is used to set value by index and column name, row_idx is the index of the sample in the group of 3 and column is the column name based on the pool group
    
    return csv.iloc[:didata_sample_count]

def helper_modular_pcr(csv, didata):
    # Implementation for modular PCR handling
    # Calculate Total amount of samples of all 3 pools -> DiData Sample Quantity * 3
    # Get the Quantity of all Pools of all Samples that have a Value -> get pool1, pool2, pool3 quantity
    # if Quantity of Values > 2/3 of Total amount -> Quantity of Values - 2/3 of Total Amount = Position of Sample in Pool 3
    # if Quantity of Values > 1/3 of Total amount -> Quantity of Values - 1/3 of Total Amount = Position of Sample in Pool 2
    # else -> Position of Sample in Pool 1
    # return new csv while empty spots are filled with 0 or None
    
    didata_sample_count = len(didata)
    csv_sample_count = len(csv["Sample Name"])
    total_pools = didata_sample_count * 3
    
    # if pool data even exist
    quant_pool_didata = sum(
        1 for sample in didata 
        if sample.get("pool1") or sample.get("pool2") or sample.get("pool3")
    )
    
    print(f"Qubit Sample Quantitiy: {csv_sample_count}")
    print(f"DiData Sample Quantitiy: {didata_sample_count}")
    print(f"Total Pools: {total_pools}")
    print(f"Quantity Pools in DiData: {quant_pool_didata}")
    
    # Decide where filling starts
    if quant_pool_didata > (2 / 3) * total_pools:
        print("Filling in Data starting from Pool 3")
        start_pool = 2
        start_row = quant_pool_didata - (2 * didata_sample_count)
    elif quant_pool_didata > (1 / 3) * total_pools:
        print("Filling in Data starting from Pool 2")
        start_pool = 1
        start_row = quant_pool_didata - didata_sample_count
    else:
        print("Filling in Data starting from Pool 1")
        start_pool = 0
        start_row = quant_pool_didata

    # Fill values starting from the correct pool and row
    for i, value in enumerate(csv["Original Sample Conc."]):
        absolute_pos = start_row + i
        pool_group = start_pool + (absolute_pos // didata_sample_count)
        row_idx = absolute_pos % didata_sample_count

        match pool_group:
            case 0:
                column = "ng_ul"
            case 1:
                column = "ng_ul_pool_2"
            case 2:
                column = "ng_ul_pool_3"
            case _:
                column = "unknown_pool"

        if column != "unknown_pool":
            csv.at[row_idx, column] = value

    return csv.iloc[:didata_sample_count]

def upload_pcr(session, csv, didata):
    csv = remove_standard_from_csv(csv)
    # get id and find group
    target_group = find_data_group(csv, didata)
    print(target_group)
    save_target_group(target_group) # Save the target group for later use in LIB uploads
    
    payload = {
        "data": [],
        "options": {
            "identify_entities_by": ["id"], # how to find the row/entity you want to update
            "upsert": False                 # what to do if it cannot find that row/entity
        }
    }
    
    if handle_qubit_and_didata_amount_check(csv, target_group, genomic="PCR"):   
        csv = helper_monolithic_pcr(csv, target_group)
        
        # Qubit Raw Data -> DiData Names
        # PCR Quantification
        # Test Date -> Post PCR date
        # Assay Name -> Kit Name DNA Post PCR
        # Always 3 different pools, Always. -> could be more Excel files

        # Add in Post PCR Visualization % CLean up for Entities
        # in case -> no pooled -> must be repeated
        # if value under 1 -> not pooled
    else:
        csv = helper_modular_pcr(csv, target_group)
        print(csv)
        # the csv will be the same for universal use, but the ones that are missing values will have a "None"
        # So only if the pool has a value it will be added to the payload, otherwise it will be skipped and not uploaded to DiData, so we can handle both modular and monolithic PCR with the same upload function and just different helper functions to rearrange the csv accordingly

    is_pooled = True

    # Option: Create Action for Is Pooled or not mechanism -> done
    
    for i in range(len(target_group)):
        if csv["ng_ul"][i] and csv["ng_ul_pool_2"][i] and csv["ng_ul_pool_3"][i]:
            if csv["ng_ul"][i] < 1 or csv["ng_ul_pool_2"][i] < 1 or csv["ng_ul_pool_3"][i] < 1:
                print("Value under 1 detected -> likely not pooled")
                is_pooled = False
            else:
                is_pooled = True
            
        entry = {
            "id": target_group[i]["id"],
            "Kit_name_DNA_Post_PCR": get_kit_name_dna_quantification_fc_number(csv["Assay Name"][i]),
            "Post_PCR_date": datetime.strptime(csv["Test Date"][i], "%d/%m/%Y %I:%M:%S %p").strftime("%d-%m-%Y %H:%M:%S"),
            "Is_pooled": is_pooled,
            "output_volume": int(target_group[i]["dna_volume"] - csv["Sample Volume (uL)"][i]),
            "Status": get_state_id_by_name("16S PCR Quantification")
        }
        if str(csv["ng_ul"][i]):
            entry["ng_ul"] = str(csv["ng_ul"][i])
        if str(csv["ng_ul_pool_2"][i]):
            entry["ng_ul_pool_2"] = str(csv["ng_ul_pool_2"][i])
        if str(csv["ng_ul_pool_3"][i]):
            entry["ng_ul_pool_3"] = str(csv["ng_ul_pool_3"][i])
            
        payload["data"].append(entry)

    # print(json.dumps(payload, indent=4))
    response = session.put(f"{API_BASE_URL}/api/entities/batch", headers=get_headers(), json=payload)
    return response

def get_base_name(sample_id):
    return re.sub(r'(P?D\d+|L\d+)$', '', sample_id) # find D1, PD1, L1 at the end of the string and remove it to get the base name

def find_match(group):
    old_target_group = []
    start_id = None
    
    for i in range(len(group)):
        for j in range(len(get_target_group())):
            for k in range(len(get_target_group()[j])):
                if get_base_name(group[i]['sample_id']) == get_base_name(list(get_target_group()[j])[k]):
                    print(f"Match found: {group[i]['sample_id']}, {list(get_target_group()[j])[k]}")
                    old_target_group = get_target_group()[j]
                    start_id = group[i]['id']
                    break
            if old_target_group and start_id:
                break
        if old_target_group and start_id:
            break
    return old_target_group, start_id

def helper_lib(target_group, didata):
    # Samples are missing due to failure in Post PCR Visualization & Clean up -> Status 524
    # Task: Find the missing Library ID and add them to the Target Group
    # print(didata[0]['sample_id'])
    # print(list(get_target_group()[0])[0])
    # print(get_base_name(didata[0]['sample_id']))
    # print(get_base_name(list(get_target_group()[0])[0]))
    
    old_target_group, start_id = find_match(target_group)
    old_ids = list(old_target_group.values())
    new_ids = [sample['id'] for group in didata for sample in group]
    
    # since old ids and new ids have completly diffrent id, we have to look by algorithm
    for i in range(len(old_ids)-1):
        old_id_diff = abs(old_ids[i] - old_ids[i+1])
        if start_id + old_id_diff in new_ids:
            print(f"Found missing ID: {start_id + old_id_diff}")
            target_group.append({
                "id": start_id + old_id_diff
            })
        start_id += old_id_diff
    # Find out which position of the group is missing and then regroup the Library IDs from DiData
    print(f"Updated Target Group: {target_group}")
    return target_group

def upload_lib(session, csv, didata):
    csv = remove_standard_from_csv(csv)
    # get id and find group
    target_group = find_data_group(csv, didata)
    print(f"Initial Target Group: {target_group}")
    if not (handle_qubit_and_didata_amount_check(csv, target_group, genomic="LIB")):
        target_group = helper_lib(target_group, didata)
    # Qubit Raw Data -> DiData Names
    # Test Date -> 16S library quantification date
    # Assay Name -> Kit Name 16S Library Quant
    # Sample Name -> Sample ID
    # Original Sample -> Library ng/ul
    # Sample Volume (uL) -> Volume taken for quantification
    
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
            "Library_ng_ul": str(csv["Original Sample Conc."][i]),
            "Kit_Name_16s_Library_Quant": get_kit_name_dna_quantification_fc_number(csv["Assay Name"][i]),
            "16S_library_quantification_date": datetime.strptime(csv["Test Date"][i], "%d/%m/%Y %I:%M:%S %p").strftime("%d-%m-%Y %H:%M:%S"),
            "Volume_taken_for_16s_library_quantification_": int(csv["Sample Volume (uL)"][i]),
            "Status": get_state_id_by_name("16S Library Quantification")
            }
        )
    
            # Status
            # 529, 16S Library Quantification
            # 530, 16S Library Visualization & 2nM
    response = session.put(f"{API_BASE_URL}/api/entities/batch", headers=get_headers(), json=payload)
    return response
    