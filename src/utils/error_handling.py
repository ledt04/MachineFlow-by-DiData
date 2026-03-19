def handle_login_responses(response):
    if response.status_code == 200:
        print("Login successful")
        return
    else:
        raise ValueError(f"{response.status_code}: {response.json().get("error", "Unknown error")}")
    
def handle_logout_responses(response):
    if response.status_code == 204:
        print("Logout successful")
        return
    else:
        raise ValueError(f"{response.status_code}: {response.json().get("error", "Unknown error")}")

def handle_get_project_id_responses(response):
    if response.status_code == 200:
        print("Get Project Id successful")
        return
    else:
        raise ValueError(f"{response.status_code}: {response.json().get("error", "Unknown error")}")
    
def handle_get_workflow_id_responses(response):
    if response.status_code == 200:
        print("Get Workflow Id successful")
        return
    else:
        raise ValueError(f"{response.status_code}: {response.json().get("error", "Unknown error")}")

def handle_get_state_id_responses(response):
    if response.status_code == 200:
        print("Get State Id successful")
        return
    else:
        raise ValueError(f"{response.status_code}: {response.json().get("error", "Unknown error")}")

def handle_get_entities_responses(response):
    if response.status_code == 200:
        print("Get Entities successful")
        return
    else:
        raise ValueError(f"{response.status_code}: {response.json().get("error", "Unknown error")}")
