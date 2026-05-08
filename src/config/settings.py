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
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
_workflow_id = None

def load_CONFIG_PATH():
    with open(CONFIG_PATH, 'r') as file:
        config_data = json.load(file)
    return config_data

CONFIG_PATH = load_CONFIG_PATH()

def get_local_directory(machine_id):
    project_root = Path(__file__).resolve().parents[2]

    for machine in CONFIG_PATH["machines"]:
        if machine["machine_id"] == machine_id:
            qubit_directory = machine["source_config"]["local_directory"]
            full_directory = os.path.join(project_root, qubit_directory)
            return full_directory
    return None

def get_qubit_id():
    for machine in CONFIG_PATH["machines"]:
        if machine["display_name"] == "qubit":
            return machine["machine_id"]
    return None

def get_fragmentanalyzer_id():
    for machine in CONFIG_PATH["machines"]:
        if machine["display_name"] == "fragmentanalyzer":
            return machine["machine_id"]
    return None

def get_qubit_genomics(genomic):
    for machine in CONFIG_PATH["machines"]:
        if machine["display_name"] == "qubit":
            return machine["api_config"][genomic]
    return None

def get_fa_qc(qc):
    for machine in CONFIG_PATH["machines"]:
        if machine["display_name"] == "fragmentanalyzer":
            return machine["api_config"][qc]
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

def get_kit_name_dna_quantification_fc_number(name):
    return CONFIG_PATH["machines"][0]["kit_name_dna_quantification_fc"][name]

import json

def save_target_group(group):
    sample_dict = {item['sample_id']: item['id'] for item in group}
    config_changed = False

    for machine in CONFIG_PATH["machines"]:
        if machine["display_name"] == "qubit":
            if sample_dict not in machine["temporary_groups"]:
                machine["temporary_groups"].append(sample_dict)
                config_changed = True
    
    if config_changed:
        try:
            with open(CONFIG_PATH, 'w') as file:
                json.dump(CONFIG_PATH, file, indent=4)
        except Exception:
            pass

    return

def get_target_group():
    return CONFIG_PATH["machines"][0]["temporary_groups"]

def get_state_id_by_name(name):
    return CONFIG_PATH["didata"]["state_id"].get(name)

def get_state_id_by_id(id):
    for name, state_id in CONFIG_PATH["didata"]["state_id"].items():
        if state_id == id:
            return name
    return None

def delete_file(path):
    try:
        os.remove(path)
        print(f"Deleted file: {path}")
    except FileNotFoundError:
        print(f"File not found, could not delete: {path}")
    except Exception as e:
        print(f"Error deleting file {path}: {e}")