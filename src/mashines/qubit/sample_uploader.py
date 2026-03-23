from src.config.settings import API_BASE_URL
from src.utils.auth import get_headers
from src.utils.error_handling import handle_upload_responses

def upload_dna(session, csv, didata):
    # get id from first sample name
    # find id group and match
    for group in didata:
        for sample in group:
            if sample["sample_id"] == csv["Sample Name"].iloc[0]:
                target_group = group
                break
        if target_group:
            break
    
    if not target_group:
        print(f"No group found for: {csv["Sample Name"].iloc[0]}")
        return None
    
    # Qubit Raw Data -> DiData Names
    # Test Date -> Quantification Date
    # Assay Name -> Kit Name DNA Quantification
    # Sample Name -> Sample ID
    # Original Sample -> Extracted DNA
    # Sample Volume (uL) -> DNA Volume(ul) = DNA Volume(ul) - Sample Volume(uL)
    # Move to next node
    
    

    return

def upload_pcr():
    # get id and find group
    pass

def upload_lib():
    pass