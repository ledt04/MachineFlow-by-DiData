_headers = {}

def set_auth(token: str, project_id: str = None):
    global _headers
    _headers = {
        "Authorization":     f"Bearer {token}",
        "Content-Type":      "application/json",
        "Accept":            "application/json",
    }
    if project_id:
        _headers["Didata-Project-Id"] = project_id
            
def get_headers():
    global _headers
    return _headers

def clear_auth():
    global _headers
    _headers = {}