import os
import requests
from dotenv import load_dotenv
from src.config.settings import API_BASE_URL
from src.utils.error_handling import handle_login_responses, handle_logout_responses
from src.utils.auth import set_auth, clear_auth, get_headers


def login():
    load_dotenv()
    session = requests.Session()
    response = session.post(f"{API_BASE_URL}/api/login", json={
        "username": os.getenv("USERNAME"),
        "password": os.getenv("PASSWORD")
    })
    handle_login_responses(response)
    
    token = response.json().get("token")
    project_id = int(os.getenv("PROJECT_ID"))
    set_auth(token, project_id)
    return response

def logout():
    response = requests.post(f"{API_BASE_URL}/api/logout", headers=get_headers())
    handle_logout_responses(response)
    clear_auth()