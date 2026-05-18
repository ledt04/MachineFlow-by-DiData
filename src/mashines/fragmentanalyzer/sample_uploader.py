from src.mashines.fragmentanalyzer.sample_filter import need_human_validation

def upload_fa(session, sample_peaks, qc):
    payload = {
        "data": [],
        "options": {
            "identify_entities_by": ["id"], # how to find the row/entity you want to update
            "upsert": False                 # what to do if it cannot find that row/entity
        }
    }
    
    # FA Raw Data -> DiData Names
    # Correct Size BP -> Fragment_Size_bp_DNA
    