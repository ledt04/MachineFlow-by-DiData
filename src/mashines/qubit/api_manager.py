from src.config.settings import API_BASE_URL
from src.utils.auth import get_headers
from src.utils.error_handling import handle_get_state_id_responses, handle_get_entities_responses

def get_state_id(session, genomics: list, workflow_id: int):
    response = session.get(f"{API_BASE_URL}/api/workflows/{workflow_id}", headers=get_headers())
    handle_get_state_id_responses(response)
    nodes = response.json().get("nodes", [])
    
    state_ids = {}
    for genomic in genomics:
        for node in nodes:
            if node["name"] == genomic:
                state_ids[genomic] = node["state_id"]
    
    if state_ids:
        return state_ids
    return None

def get_entities(session, state_ids):
    response = session.get(f"{API_BASE_URL}/api/entities", headers=get_headers())
    handle_get_entities_responses(response)
    data = {"states": []}

    for state_id in state_ids:
        samples = []
        for entity in response.json():
            if entity.get("Status") == state_id:
                sample = {
                    "sample_id": entity.get("Sample__Id"),
                    "id": entity.get("id"),
                    "created_at": entity.get("created_at"),
                    "dna_volume": entity.get("output_volume"),           
                    "pool1": entity.get("ng_ul"),
                    "pool2": entity.get("ng_ul_pool_2"),
                    "pool3": entity.get("ng_ul_pool_3"),
                }
                samples.append(sample)
        if samples:
            data["states"].append({
                "state_id": state_id,
                "samples": samples
            })
    
    return data
