import os
import json
from pathlib import Path
from src.mashines.qubit.api_manager import get_state_id, get_entities
from src.mashines.qubit.csv_manager import load_csv
from src.mashines.qubit.sample_classifier import sample_classifier, group_samples_by_id
from src.config.settings import get_qubit_genomics, get_workflow_id_by_name, set_workflow_id, get_local_directory, get_qubit_id, get_workflow_id
from src.mashines.qubit.sample_uploader import upload_dna, upload_lib, upload_pcr
from src.utils.error_handling import handle_upload_responses
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
    csv_df = load_csv(Path(get_local_directory(get_qubit_id())))
    csv_sample_names = csv_df["Sample Name"]

    # debug
    # print(json.dumps(samples, indent=4))
    # print("\n")
    # print(sample_names)
    
    # find matching sample name in csv file and stored didata names
    # detect which step (dna, pcr, lib)
    sample_state_id = sample_classifier(csv_sample_names, didata_sample_names)
    if not sample_state_id:
        print("No matching sample names has been found")
        return

    # upload csv to correct step
    for state_name, state_id in state_ids.items():
        if state_id == sample_state_id:
            print(f"Detected Samples are in {state_name}")
            genomic = state_name

    # print(json.dumps(group_samples_by_id(didata_sample_names, sample_state_id), indent=4))
    grouped_didata_samples = group_samples_by_id(didata_sample_names, sample_state_id)
    
    match genomic:
        case _ if genomic == genomics[0]:
            response = upload_dna(session, csv_df, grouped_didata_samples)
            handle_upload_responses(response, genomic)
            
        case _ if genomic == genomics[1]:
            response = upload_pcr(session, csv_df, grouped_didata_samples)
            handle_upload_responses(response, genomic)
            
        case _ if genomic == genomics[3]:
            response = upload_lib(session, csv_df, grouped_didata_samples)
            handle_upload_responses(response, genomic)
    return