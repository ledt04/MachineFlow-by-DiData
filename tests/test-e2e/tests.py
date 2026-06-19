import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Setze hier manuell das Alias ein, das du testen möchtest
BASE_URL = "https://pilot.swissdidata.com/jupiter"  # oder "http://immvmdidata02.d.immlan.unizh.ch"
URL = f"{BASE_URL}/api/login"

payload = {
    "username": os.getenv("DIDATA_USERNAME"),
    "password": os.getenv("DIDATA_PASSWORD")
}

print(f"Teste Route: {URL}...\n")

try:
    response = requests.post(URL, json=payload, timeout=5)
    
    print(f"Status Code: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type', 'Nicht angegeben')}")
    print("-" * 50)
    
    if "application/json" in response.headers.get("Content-Type", ""):
        print("🎯 BINGO! Der Server hat JSON geantwortet:")
        print(response.json())
    else:
        print("❌ Falsches Format. Der Server hat HTML oder Text zurückgegeben.")
        print(response.text[:300]) # Zeigt die ersten 300 Zeichen der Antwort

except Exception as e:
    print(f"💥 Fehler beim Request: {e}")