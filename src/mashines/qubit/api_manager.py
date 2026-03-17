from src.config.settings import API_BASE_URL
from src.utils.auth import get_headers

def get_state_id(session, genomics: list, workflow_id):
    response = session.get(f"{API_BASE_URL}/api/workflow/{workflow_id}", headers=get_headers())
    nodes = response.json().get("nodes", [])

    state_ids = []
    for genomic in genomics:
        for node in nodes:
            if node["name"] == genomic:
                state_ids.append(node["state_id"])
    if state_ids:
        return state_ids
    return None

def get_entities(session, state_ids):
    response = session.get(f"{API_BASE_URL}/api/entities", headers=get_headers())

    sample_ids = {}
    for state_id in state_ids:
        filtered_entities = []
        for entity in response:
            if entity["Status"] == state_id:
                filtered_entities.append(entity["Sample_Id"])
        if filtered_entities:
            sample_ids[state_id] = filtered_entities
    return sample_ids
