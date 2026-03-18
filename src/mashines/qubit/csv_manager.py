import pandas as pd
from pathlib import Path

def load_csv(directory: Path):
    csv_file = list(directory.glob("*.csv"))
    if not csv_file:
        raise FileNotFoundError(f"No CSV file found in {directory}")
    return pd.read_csv(csv_file[0])
