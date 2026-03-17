import os
from src.mashines.qubit.api_manager import get_samples
from src.config.settings import get_qubit_genomics, set_workflow_id, _WORKFLOW_ID
from dotenv import load_dotenv

def main(session):
    load_dotenv()
    set_workflow_id(session, os.getenv("WORKFLOW"))
    # renaming:
    # get samplenames from Didata
    # -> "DNA Quantification"
    # -> "16S PCR Quantification"
    # -> "16S Library Quantification"
    get_samples(session, get_qubit_genomics("dna"), _WORKFLOW_ID)

    # load csv file
    # find matching sample name in csv file and stored didata names
    # detect which step (dna, pcr, lib)
    # rename rest and std -> Standard

    # format to correct step

    # upload csv to correct step
    pass

if __name__ == "__main__":
    main()