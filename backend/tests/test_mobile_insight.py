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
test_email = "test_mobile_insight@example.com"
test_password = "testpassword"

# Fetching public key
url_public_key = "http://localhost:3006/public_key"
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

BASE_URL = "http://localhost:3006/api/v1/mobile_insight"

def test_get_insight_valid_input_case1():
    prompt = "what it the price of btc today?"  
    response = requests.get(BASE_URL, params={"prompt": prompt}, headers=headers)
    assert response.status_code == 200
    assert "content" in response.json()

def test_get_insight_valid_input_case2():
    prompt = "Which stablecoins are available on Moonbeam?"  
    response = requests.get(BASE_URL, params={"prompt": prompt}, headers=headers)
    assert response.status_code == 200
    assert "content" in response.json()

def test_get_insight_valid_input_case3():
    prompt = "Can you help me check the market share of stablecoin?"  
    response = requests.get(BASE_URL, params={"prompt": prompt}, headers=headers)
    assert response.status_code == 200
    assert "content" in response.json()

def test_get_insight_valid_input_case4():
    prompt = "What is the daily trading volume of dex?"  
    response = requests.get(BASE_URL, params={"prompt": prompt}, headers=headers)
    assert response.status_code == 200
    assert "content" in response.json()

def test_get_insight_valid_input_case5():
    prompt = "Can you help me examine the details of this contract: 0xf2A22B900dde3ba18Ec2AeF67D4c8C1a0DAB6aAC?"  
    response = requests.get(BASE_URL, params={"prompt": prompt}, headers=headers)
    assert response.status_code == 200
    assert "content" in response.json()

def test_get_insight_invalid_input_case1():
    prompt = "what's the weather today?" 
    response = requests.get(BASE_URL, params={"prompt": prompt}, headers=headers)
    assert response.status_code == 200
    assert "content" in response.json()

def test_get_insight_invalid_input_case2():
    prompt = "how are you?" 
    response = requests.get(BASE_URL, params={"prompt": prompt}, headers=headers)
    assert response.status_code == 200
    assert "content" in response.json()

def test_get_insight_invalid_input_case3():
    prompt = "hello" 
    response = requests.get(BASE_URL, params={"prompt": prompt}, headers=headers)
    assert response.status_code == 200
    assert "content" in response.json()

def test_get_insight_empty_prompt():
    prompt = ""  
    response = requests.get(BASE_URL, params={"prompt": prompt}, headers=headers)
    assert response.status_code == 200
    assert "content" in response.json()

def test_get_insight_no_prompt():
    response = requests.get(BASE_URL, headers=headers)
    assert response.status_code == 422  # no prompt, return 422 Unprocessable Entity

def test_get_insight_server_error():
    prompt = "Test prompt causing server error"  
    # 模拟服务器内部错误（例如500错误）。你可能需要使用其他方法来模拟或触发特定的服务器错误。
    with pytest.raises(requests.exceptions.RequestException):
        requests.get(BASE_URL, params={"prompt": prompt}, headers=headers, timeout=0.001)

if __name__ == "__main__":
    pytest.main()

