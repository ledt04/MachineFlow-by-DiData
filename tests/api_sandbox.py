import requests
import json
import os

BASE = "http://immvmdidata02.d.immlan.unizh.ch/test"
USERNAME = "res_admin"
PASSWORD = "imm.FoEg.567"

s = requests.Session()
r = s.post(f"{BASE}/api/login", json={
    "username": USERNAME,
    "password": PASSWORD
})

token = r.json()["token"]

headers = {
    "Authorization":        f"Bearer {token}",
    "Content-Type":         "application/json",
    "Accept":               "application/json",
    "Didata-Project-Id":    "1"
}

r = s.get(f"{BASE}/api/entities", headers=headers)

all_entities = r.json()

target_dir = r"C:\Users\dule\Documents\MashineFlow-by-DiData\tests"
file_name = "all_entities.json"
full_path = os.path.join(target_dir, file_name)

os.makedirs(target_dir, exist_ok=True)

with open(full_path, "w", encoding="utf-8") as f:
    json.dump(all_entities, f, indent=4, ensure_ascii=False)

print(f"Stored {len(all_entities)} entities in {full_path}")