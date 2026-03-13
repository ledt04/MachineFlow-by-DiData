def handle_login_responses(response):
    if response.status_code == 200:
        print("Login successful")
        return
    elif response.status_code != 200:
        raise ValueError(f"{response.status_code}: {response.json().get("error", "Unknown error")}")
    
def handle_logout_responses(response):
    if response.status_code == 204:
        print("Logout successful")
        return
    elif response.status_code != 204:
        raise ValueError(f"{response.status_code}: {response.json().get("error", "Unknown error")}")
    