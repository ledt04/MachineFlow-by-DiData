_headers = {}

def set_auth(token: str, project_id: int):
    global _headers
    _headers = {
        "Authorization":        f"Bearer {token}",
        "Content-Type":         "application/json",
        "Accept":               "application/json",
        "Didata-Project-Id":    project_id
    }
    
def get_headers():
    return _headers

def clear_auth():
    global _headers
    _headers = {}