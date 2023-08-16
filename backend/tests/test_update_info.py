import base64
import requests
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import pytest
from datetime import datetime


# Replace with your actual app URL
base_url = "http://localhost:3006/api/v1"

# Replace with the actual email and password
test_email = "test@outlook.com"
test_password = "test_20230806"

# Fetching public key
url_public_key = "http://localhost:3006/api/public_key"
response = requests.get(url_public_key)
pem = response.json()['public_key']
public_key = serialization.load_pem_public_key(pem.encode())

# Encrypting email and password
encrypted_email = public_key.encrypt(test_email.encode(), padding.OAEP(padding.MGF1(hashes.SHA256()), hashes.SHA256(), None))
encrypted_password = public_key.encrypt(test_password.encode(), padding.OAEP(padding.MGF1(hashes.SHA256()), hashes.SHA256(), None))

# Base64 encoding the encrypted email and password
login_request = {
    "email": base64.b64encode(encrypted_email).decode(),
    "password": base64.b64encode(encrypted_password).decode()
}

# Logging in to get the token
response = requests.post(f'{base_url}/login', json=login_request)
token = response.json()["access_token"]

headers = {'Authorization': f'Bearer {token}'}

BASE_URL = "http://localhost:3006/api/v1/update_info"

def test_update_wallet_address():
    wallet_address = "0xd17F3D593009756938B0B3041F98AC6233f42080"  

    response = requests.post(BASE_URL, json={"wallet_address": wallet_address}, headers=headers)
    assert response.status_code == 200
    assert response.json()["update_result"] == "success"

def test_update_username():

    response = requests.post(BASE_URL, json={"username": "chatdata-insight"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["update_result"] == "success"

def test_update_password():

    response = requests.post(BASE_URL, json={"password": "test_20230808"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["update_result"] == "success"

if __name__ == "__main__":
    pytest.main()
