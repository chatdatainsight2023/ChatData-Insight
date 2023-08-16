import os
import sys

# Get the absolute path of the current file
current_path = os.path.abspath(os.path.dirname(__file__))

# Navigate up to the 'backend' directory from the current file's location
backend_path = os.path.join(current_path, '..')

# Get the normalized absolute path
backend_path = os.path.abspath(backend_path)

# Add the 'backend' directory to sys.path
sys.path.append(backend_path)


from services.helpers.validate_question import validate_question

def test_validate_question_case1():
    question = "Can you help me examine the details of this contract: 0xf2A22B900dde3ba18Ec2AeF67D4c8C1a0DAB6aAC?"
    result = validate_question(question)
    assert result['validity'] == 'True'
    assert result['problem'] == question

def test_validate_question_case2():
    question = "What's the recent price trend of BTC over the last few hours?"
    result = validate_question(question)
    assert result['validity'] == 'True'
    assert result['problem'] == question

def test_validate_question_case3():
    question = "Could you please check the market share of decentralized exchanges?"
    result = validate_question(question)
    assert result['validity'] == 'True'
    assert result['problem'] == question

def test_validate_question_case4():
    question = "Can you help me check the trading volumes of exchanges on various blockchains?"
    result = validate_question(question)
    assert result['validity'] == 'True'
    assert result['problem'] == question

def test_validate_question_case5():
    question = "What is the daily trading volume of dex?"
    result = validate_question(question)
    assert result['validity'] == 'True'
    assert result['problem'] == question

def test_validate_question_case6():
    question = "Can you help me check the market share of stablecoin?"
    result = validate_question(question)
    assert result['validity'] == 'True'
    assert result['problem'] == question

def test_validate_question_case7():
    question = "Which stablecoins are available on Moonbeam?"
    result = validate_question(question)
    assert result['validity'] == 'True'
    assert result['problem'] == question

def test_validate_question_case8():
    question = "How are you?"
    result = validate_question(question)
    assert result['validity'] == 'False'
    assert result['problem'] == question
def test_validate_question_case9():
    question = "hello"
    result = validate_question(question)
    assert result['validity'] == 'False'
    assert result['problem'] == question
def test_validate_question_case10():
    question = "Can you introduce the Google?"
    result = validate_question(question)
    assert result['validity'] == 'False'
    assert result['problem'] == question
def test_validate_question_case11():
    question = "csadjdskfsdf"
    result = validate_question(question)
    assert result['validity'] == 'False'
    assert result['problem'] == question
