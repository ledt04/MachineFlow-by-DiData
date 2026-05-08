def sample_classifier(csv_names, didata_names):
    # 1. Build the lookup map
    lookup = {
        samp['sample_id']: st['state_id'] 
        for st in didata_names['states'] 
        for samp in st['samples']
    }

    # 2. Collect all unique state IDs found for the provided names
    # Using set comprehension for speed and automatic uniqueness
    found_state_ids = {lookup[name] for name in csv_names if name in lookup}

    # 3. Validation Logic
    if len(found_state_ids) == 1:
        # Exactly one state ID was found for all matching samples
        return found_state_ids.pop()
    
    # Returns None if:
    # - No samples were found (len == 0)
    # - Samples are split across different states (len > 1)
    return None