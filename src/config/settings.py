import os
import json
from pathlib import Path
from dotenv import load_dotenv
from src.utils.auth import get_headers, set_auth
from src.utils.error_handling import handle_get_project_id_responses, handle_get_workflow_id_responses

load_dotenv()

PROJECT = os.getenv("PROJECT")
WORKFLOW = os.getenv("WORKFLOW")
API_BASE_URL = os.getenv("API_BASE_URL")
MACHINE_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "machine_config.json")
_workflow_id = None

def load_machine_config():
    with open(MACHINE_CONFIG_PATH, 'r') as file:
        config_data = json.load(file)
    return config_data

MACHINE_CONFIG = load_machine_config()

def get_local_directory(machine_id):
    project_root = Path(__file__).resolve().parents[2]

    for machine in MACHINE_CONFIG["machines"]:
        if machine["machine_id"] == machine_id:
            qubit_directory = machine["source_config"]["local_directory"]
            full_directory = os.path.join(project_root, qubit_directory)
            return full_directory
    return None

def get_qubit_id():
    for machine in MACHINE_CONFIG["machines"]:
        if machine["display_name"] == "qubit":
            return machine["machine_id"]
    return None

def get_fragmentanalyzer_id():
    for machine in MACHINE_CONFIG["machines"]:
        if machine["display_name"] == "fragmentanalyzer":
            return machine["machine_id"]
    return None

def get_qubit_genomics(genomic):
    for machine in MACHINE_CONFIG["machines"]:
        if machine["display_name"] == "qubit":
            return machine["api_config"][genomic]
    return None

def get_project_id(session, name):
    response = session.get(f"{API_BASE_URL}/api/access-rights/projects", headers=get_headers())
    handle_get_project_id_responses(response)
    projects = response.json()
    for project in projects:
        if project["name"] == name:
            return int(project["id"])
    return None

def get_workflow_id_by_name(session, name):
    response = session.get(f"{API_BASE_URL}/api/workflows", headers=get_headers())
    handle_get_workflow_id_responses(response)
    workflows = response.json()
    for workflow in workflows:
        if workflow["name"] == name:
            return workflow["id"]
    return None

def set_workflow_id(id):
    global _workflow_id
    _workflow_id = id

def get_workflow_id():
    global _workflow_id
    return _workflow_id