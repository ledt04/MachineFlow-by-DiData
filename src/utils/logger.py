import os
from pathlib import Path
import requests
from dotenv import load_dotenv
from src.config.settings import API_BASE_URL, get_project_id
from src.utils.error_handling import handle_login_responses, handle_logout_responses
from src.utils.auth import set_auth, clear_auth, get_headers

def login():
    session = requests.Session()
    response = session.post(f"{API_BASE_URL}/api/login", json={
        "username": os.getenv("DIDATA_USERNAME"),
        "password": os.getenv("DIDATA_PASSWORD")
    })
    handle_login_responses(response)
    token = response.json().get("token")
    set_auth(token)
    project_id = str(get_project_id(session, os.getenv("PROJECT")))
    set_auth(token, project_id)
    return session

def logout(session):
    response = session.post(f"{API_BASE_URL}/api/logout", headers=get_headers())
    handle_logout_responses(response)
    clear_auth()