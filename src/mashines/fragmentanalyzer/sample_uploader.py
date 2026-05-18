from src.mashines.fragmentanalyzer.sample_filter import need_human_validation
from src.config.settings import API_BASE_URL, get_kit_name_post_pcr_visualization_number, get_method_number, get_state_id_by_name
from src.utils.auth import get_headers
import datetime

def upload_fa(session, sample_peaks, qc):
    payload = {
        "data": [],
        "options": {
            "identify_entities_by": ["id"], # how to find the row/entity you want to update
            "upsert": False                 # what to do if it cannot find that row/entity
        }
    }
    
    print(sample_peaks)
    print(qc)
    
    # FA Raw Data -> DiData Names
    # Correct Size BP -> Fragment_Size_bp_DNA
    # Is_visualized: True
    # Visualization_date: DD-MM-YYYY HH:MM:SS
    # Kit_Name_Post_PCR_Visualization: 563
    # Method: 522

    for sample_name, peaks in sample_peaks.items():
        # 2 diffrent payload data, one for if human validation is needed, one for if not
        data, human_validation_needed = need_human_validation(peaks)
        
        # if human validation is needed, put all peaks in Fragment_size_bp_options as a String example: "100, 200, 300"
        # if not needed, put the correct peak as a number in Fragment_Size_bp_DNA

        if human_validation_needed:
            payload["data"].append({
                "id": sample_name,
                "Is_visualized": True,
                "Visualization_date": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                "Kit_Name_Post_PCR_Visualization": get_kit_name_post_pcr_visualization_number("HS NGS Fragment Kit (1-6000bp)"),
                "Method": get_method_number("FA"),
                "Fragment_size_bp_options": ", ".join(str(peak) for peak in data),
                "Need_Human_Validation": True,
                "Status": qc
            })
        else:
            payload["data"].append({
                "id": sample_name,
                "Is_visualized": True,
                "Visualization_date": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                "Kit_Name_Post_PCR_Visualization": get_kit_name_post_pcr_visualization_number("HS NGS Fragment Kit (1-6000bp)"),
                "Method": get_method_number("FA"),
                "Fragment_Size_bp_DNA": data,
                "Need_Human_Validation": False,
                "Status": qc
            })

    response = session.put(f"{API_BASE_URL}/api/entities/batch", headers=get_headers(), json=payload)
    return response