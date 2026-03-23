from datetime import datetime

def sample_classifier(csv_names, didata_names):
    csv_names = csv_names.tolist()
    
    for csv_name in csv_names:
        for state in didata_names["states"]:
            for sample in state["samples"]:
                if csv_name == sample["sample_id"]:
                    return state["state_id"]
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

def group_samples_by_id(didata_names, state_id):
    for state in didata_names["states"]:
        if state_id == state["state_id"]:
             target_samples = state["samples"]
             break
    
    if not target_samples:
        return None
    
    target_samples.sort(key=lambda x: int(x["id"])) # sort all valuables by id
    
    groups = []
    current_group = [target_samples[0]]
    time_fmt = "%d-%m-%Y %H:%M:%S"
    
    for i in range(1, len(target_samples)):
        prev = target_samples[i-1]
        curr = target_samples[i]
        
        prev_id = int(prev["id"])
        curr_id = int(curr["id"])
        
        t_prev = datetime.strptime(prev["created_at"], time_fmt)
        t_curr = datetime.strptime(curr["created_at"], time_fmt)
        
        if (curr_id - prev_id <= 1) and (abs((t_curr - t_prev).total_seconds()) <= 3600):
            current_group.append(curr)
        else:
            groups.append(current_group)
            current_group = [curr]
            
    groups.append(current_group)
    return groups