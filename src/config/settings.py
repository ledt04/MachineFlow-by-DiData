import os
import json
from pathlib import Path

DEBUG = True
API_BASE_URL = "http://immvmdidata02.d.immlan.unizh.ch/test"
MACHINE_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "machine_config.json")

def load_machine_config():
    with open(MACHINE_CONFIG_PATH, 'r') as file:
        config_data = json.load(file)
    return config_data

MACHINE_CONFIG = load_machine_config()

def get_local_directory(machine_id):
    project_root = Path(__file__).resolve().parents[1]

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