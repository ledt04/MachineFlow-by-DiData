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

r = s.get(f"{BASE}/api/workflows/8", headers=headers)

print(r.json())