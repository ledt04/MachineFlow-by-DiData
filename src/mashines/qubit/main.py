import os
import json
from pathlib import Path
from src.mashines.qubit.api_manager import get_state_id, get_entities
from src.mashines.qubit.csv_manager import load_csv
from src.mashines.qubit.sample_classifier import sample_classifier
from src.config.settings import get_qubit_genomics, get_workflow_id_by_name, set_workflow_id, get_local_directory, get_qubit_id, get_workflow_id
from dotenv import load_dotenv

def main(session):
    load_dotenv()
    workflow_id = get_workflow_id_by_name(session, os.getenv("WORKFLOW"))
    set_workflow_id(workflow_id)
    
    # renaming:
    # get samplenames from Didata
    # -> "DNA Quantification"
    # -> "16S PCR Quantification"
    # -> "16S Library Quantification"
    genomics = [get_qubit_genomics("dna"), get_qubit_genomics("pcr"), get_qubit_genomics("lib")]
    state_ids = get_state_id(session, genomics, get_workflow_id())
    didata_sample_names = get_entities(session, state_ids.values())

    # load csv file
    df = load_csv(Path(get_local_directory(get_qubit_id())))
    csv_sample_names = df["Sample Name"]

    # debug
    # print(json.dumps(samples, indent=4))
    # print("\n")
    # print(sample_names)
    
    # find matching sample name in csv file and stored didata names
    # detect which step (dna, pcr, lib)
    if not sample_classifier(csv_sample_names, didata_sample_names):
        return
    
    # rename rest and std -> Standard

    # format to correct step

    # upload csv to correct step