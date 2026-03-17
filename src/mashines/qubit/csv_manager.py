import pandas as pd

def load_csv(directory):
    try:
        df = pd.read_csv(directory)
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
