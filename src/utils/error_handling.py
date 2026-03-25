def handle_login_responses(response):
    if response.status_code == 200:
        print("Login successful")
        return
    else:
        raise ValueError(f"{response.status_code}: {response.json().get("error", "Unknown Login error")}")
    
def handle_logout_responses(response):
    if response.status_code == 204:
        print("Logout successful")
        return
    else:
        raise ValueError(f"{response.status_code}: {response.json().get("error", "Unknown Logout error")}")

def handle_get_project_id_responses(response):
    if response.status_code == 200:
        print("Get Project Id successful")
        return
    else:
        raise ValueError(f"{response.status_code}: {response.json().get("error", "Unknown Get Project Id error")}")
    
def handle_get_workflow_id_responses(response):
    if response.status_code == 200:
        print("Get Workflow Id successful")
        return
    else:
        raise ValueError(f"{response.status_code}: {response.json().get("error", "Unknown Get Workflow Id error")}")

def handle_get_state_id_responses(response):
    if response.status_code == 200:
        print("Get State Id successful")
        return
    else:
        raise ValueError(f"{response.status_code}: {response.json().get("error", "Unknown Get State Id error")}")

def handle_get_entities_responses(response):
    if response.status_code == 200:
        print("Get Entities successful")
        return
    else:
        raise ValueError(f"{response.status_code}: {response.json().get("error", "Unknown Get Entities error")}")

def handle_upload_responses(response, genomic):
    if response.status_code == 200:
        print(f"Upload to DiData to Node {genomic} successful")
        return
    else:
        raise ValueError(f"{response.status_code}: {response.json().get("error", f"Unknown {genomic} Upload error")}")
    
def handle_find_data_group_return(group, csv):
    if not group:
        raise ValueError(f"No group found for: {csv["Sample Name"].iloc[0]}")
    return