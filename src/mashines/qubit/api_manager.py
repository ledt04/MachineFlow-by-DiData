import requests
from src.config.settings import API_BASE_URL, get_qubit_genomics

def get_samples(session, genomic, workflow_id):
    response = session.get(f"{API_BASE_URL}/api/workflow/{workflow_id}")
    nodes = response.json().get("nodes", [])
    for node in nodes:
        if node["name"] == genomic