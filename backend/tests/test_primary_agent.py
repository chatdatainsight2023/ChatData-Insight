import os
import sys
import json

# Get the absolute path of the current file
current_path = os.path.abspath(os.path.dirname(__file__))

# Navigate up to the 'backend' directory from the current file's location
backend_path = os.path.join(current_path, '..')

# Get the normalized absolute path
backend_path = os.path.abspath(backend_path)

# Add the 'backend' directory to sys.path
sys.path.append(backend_path)

from services.primary_agent_v2 import primary_agent

def test_valid_question_case1():
    question = "Can you help me examine the details of this contract: 0xf2A22B900dde3ba18Ec2AeF67D4c8C1a0DAB6aAC?"
    response = primary_agent(question)
    assert response is not None

def test_valid_question_case2():
    question = "What's the recent price trend of BTC over the last few hours?"
    response = primary_agent(question)
    assert response is not None

def test_valid_question_case3():
    question = "Could you please check the market share of decentralized exchanges?"
    response = primary_agent(question)
    assert response is not None

def test_valid_question_case4():
    question = "Can you help me check the trading volumes of exchanges on various blockchains?"
    response = primary_agent(question)
    assert response is not None

def test_valid_question_case5():
    question = "What is the daily trading volume of dex?"
    response = primary_agent(question)
    assert response is not None

def test_valid_question_case6():
    question = "Can you help me check the market share of stablecoin?"
    response = primary_agent(question)
    assert response is not None

def test_valid_question_case7():
    question = "Which stablecoins are available on Moonbeam?"
    response = primary_agent(question)
    assert response is not None

def test_invalid_question_case8():
    question = "how is the weather?"
    response = primary_agent(question)

    print("------response:",response)
    assert response is not None

def test_invalid_question_case9():
    question = "How are you?"
    response = primary_agent(question)

    print("------response:",response)
    assert response is not None
def test_invalid_question_case10():
    question = "hello"
    response = primary_agent(question)

    print("------response:",response)
    assert response is not None