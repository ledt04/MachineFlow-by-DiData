def sample_classifier(csv_names, didata_names):
    csv_names = csv_names.tolist()
    
    for csv_name in csv_names:
        for state in didata_names["states"]:
            for sample in state["samples"]:
                if csv_name == sample["sample_name"]:
                    return state["state_id"]
    print("No matching sample names has been found")
    return None
    
    '''
    for state in didata_names["states"]:
        for sample in state["samples"]:
            print(sample["sample_name"])
            
    print("\n")
    
    csv_names = csv_names.tolist()
    for name in csv_names:
        print(name)
    '''
    