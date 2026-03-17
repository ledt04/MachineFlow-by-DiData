import os
from pathlib import Path
from src.mashines.qubit.api_manager import get_state_id, get_entities
from src.mashines.qubit.csv_manager import load_csv
from src.config.settings import get_qubit_genomics, set_workflow_id, _WORKFLOW_ID, get_local_directory, get_qubit_id
from dotenv import load_dotenv

def main(session):
    load_dotenv()
    set_workflow_id(session, os.getenv("WORKFLOW"))
    # renaming:
    # get samplenames from Didata
    # -> "DNA Quantification"
    # -> "16S PCR Quantification"
    # -> "16S Library Quantification"
    genomics = [get_qubit_genomics("dna"), get_qubit_genomics("pcr"), get_qubit_genomics("lib")]
    state_ids = get_state_id(session, genomics, _WORKFLOW_ID)
    sample_ids = get_entities(session, state_ids)

    # load csv file
    df = load_csv(Path(get_local_directory(get_qubit_id)))
    sample_names = df["Sample Name"]

    # debug
    print(sample_ids)
    print("\n")
    print(sample_names)
    # find matching sample name in csv file and stored didata names
    
    # detect which step (dna, pcr, lib)
    # rename rest and std -> Standard

    # format to correct step

    # upload csv to correct step
    pass

if __name__ == "__main__":
    main()