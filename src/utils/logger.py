import os
import requests
from src.config.settings import API_BASE_URL
from dotenv import load_dotenv

def login():
    session = requests.Session()
    response = session.ppost(f"{API_BASE_URL}/api/login", json={
        "username": os.getenv("USERNAME"),
        "password": os.getenv("PASSWORD")
    })
    return response