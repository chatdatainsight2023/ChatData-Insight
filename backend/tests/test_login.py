import base64
import requests
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def test_login():
    # Retrieve public key
    url_public_key = "http://localhost:3006/api/public_key"
    response = requests.get(url_public_key)
    pem = response.json()['public_key']
    public_key = serialization.load_pem_public_key(pem.encode())

    url_login = "http://localhost:3006/api/v1/login"

    # Test unregistered user
    unregistered_email = "unregistered@example.com"
    unregistered_password = "new_password"
    encrypted_email = public_key.encrypt(unregistered_email.encode(), padding.OAEP(padding.MGF1(hashes.SHA256()), hashes.SHA256(), None))
    encrypted_password = public_key.encrypt(unregistered_password.encode(), padding.OAEP(padding.MGF1(hashes.SHA256()), hashes.SHA256(), None))
    encoded_email = base64.b64encode(encrypted_email).decode()
    encoded_password = base64.b64encode(encrypted_password).decode()

    json_data = {
            "email": encoded_email,
            "password": encoded_password
    }
    response_login = requests.post(url_login, json=json_data)
    assert response_login.status_code == 200  # Successful
    assert "access_token" in response_login.json()

    # Test login with a registered user and correct password
    correct_password = "new_password"  # Replace with your actual password
    encrypted_password = public_key.encrypt(correct_password.encode(), padding.OAEP(padding.MGF1(hashes.SHA256()), hashes.SHA256(), None))
    encoded_password = base64.b64encode(encrypted_password).decode()

    response_login = requests.post(url_login, json={"email": encoded_email, "password": encoded_password})
    assert response_login.status_code == 200  # Successful
    assert "token_type" in response_login.json()
    assert "access_token" in response_login.json()

    # Test login with a registered user but incorrect password
    email = "unregistered@example.com"  # Replace with your actual registered email
    wrong_password = "wrong_password"
    encrypted_email = public_key.encrypt(email.encode(), padding.OAEP(padding.MGF1(hashes.SHA256()), hashes.SHA256(), None))
    encrypted_password = public_key.encrypt(wrong_password.encode(), padding.OAEP(padding.MGF1(hashes.SHA256()), hashes.SHA256(), None))
    encoded_email = base64.b64encode(encrypted_email).decode()
    encoded_password = base64.b64encode(encrypted_password).decode()

    response_login = requests.post(url_login, json={"email": encoded_email, "password": encoded_password})
    assert response_login.status_code == 401  # Unauthorized
