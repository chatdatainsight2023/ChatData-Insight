import pytest
import requests

# 请将"your_api_base_url"替换为实际的API基本URL
BASE_URL = "http://localhost:3006/api/v1/insight"

def test_get_insight_valid_input_case1():
    prompt = "what it the price of btc today?"  
    response = requests.get(BASE_URL, params={"prompt": prompt})

    assert response.status_code == 200
    assert "content" in response.json()

def test_get_insight_valid_input_case2():
    prompt = "Which stablecoins are available on Moonbeam?"  
    response = requests.get(BASE_URL, params={"prompt": prompt})

    assert response.status_code == 200
    assert "content" in response.json()

def test_get_insight_valid_input_case3():
    prompt = "Can you help me check the market share of stablecoin?"  
    response = requests.get(BASE_URL, params={"prompt": prompt})

    assert response.status_code == 200
    assert "content" in response.json()

def test_get_insight_valid_input_case4():
    prompt = "What is the daily trading volume of dex?"  
    response = requests.get(BASE_URL, params={"prompt": prompt})

    assert response.status_code == 200
    assert "content" in response.json()

def test_get_insight_valid_input_case5():
    prompt = "Can you help me examine the details of this contract: 0xf2A22B900dde3ba18Ec2AeF67D4c8C1a0DAB6aAC?"  
    response = requests.get(BASE_URL, params={"prompt": prompt})

    assert response.status_code == 200
    assert "content" in response.json()

def test_get_insight_invalid_input_case1():
    prompt = "what's the weather today?" 
    response = requests.get(BASE_URL, params={"prompt": prompt})

    assert response.status_code == 200
    assert "content" in response.json()

def test_get_insight_invalid_input_case2():
    prompt = "how are you?" 
    response = requests.get(BASE_URL, params={"prompt": prompt})

    assert response.status_code == 200
    assert "content" in response.json()

def test_get_insight_invalid_input_case3():
    prompt = "hello" 
    response = requests.get(BASE_URL, params={"prompt": prompt})

    assert response.status_code == 200
    assert "content" in response.json()

def test_get_insight_empty_prompt():
    prompt = ""  
    response = requests.get(BASE_URL, params={"prompt": prompt})

    assert response.status_code == 200
    assert "content" in response.json()

def test_get_insight_no_prompt():
    response = requests.get(BASE_URL)

    assert response.status_code == 422  # no prompt，return 422 Unprocessable Entity

def test_get_insight_server_error():
    prompt = "Test prompt"  
    # 模拟服务器内部错误（例如500错误）
    with pytest.raises(requests.exceptions.RequestException):
        requests.get(BASE_URL, params={"prompt": prompt}, timeout=0.001)


if __name__ == "__main__":
    pytest.main()
