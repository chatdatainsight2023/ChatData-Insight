import os
import sys
import logging
import openai as openai

from core.config import Config
from services.helpers.validate_question import validate_question
from services.helpers.decompose_question import decompose_question
from services.helpers.integrate_answer import integrate_answer
from services.primary_agent_v2 import primary_agent

from langchain.llms import OpenAI

current_directory = os.path.dirname(os.path.realpath(__file__))
backend_directory = os.path.abspath(os.path.join(current_directory,"..",".."))
sys.path.insert(0, backend_directory)

os.environ["OPENAI_API_KEY"] = Config.OPENAI_API_KEY
MODEL_NAME = Config.MODEL_NAME
LLM = OpenAI(temperature=0,model_name=MODEL_NAME)  

# Create a custom logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# decompose questions and compile answers

RETURN_MODEL = '''
I'm sorry, but I'm currently unable to answer your question. 
My expertise lies in the fields of blockchain and web3. 
Feel free to ask me any questions related to these domains.
'''

def chatdata_insight_v1(origin_question):

    validity_result = validate_question(origin_question)
    validity = True if validity_result['validity'] == 'True' else False
    if validity:
        try:
            answer_dict = decompose_question(origin_question)
        except Exception as e:
            print(f"ERROR:     Error occurred during task decomposition: {e}")
            return None

        try:
            result = integrate_answer(origin_question, answer_dict)
        except Exception as e:
            print(f"ERROR:     Error occurred during result integration: {e}")
            return None

        # print("integration result:", result)
        return validity, result

    else:
        return validity, RETURN_MODEL

RESPONSE_MODEL = '''
I'm sorry, but I'm currently unable to answer your question. 
My expertise lies in the fields of blockchain and web3. 
Feel free to ask me any questions related to these domains.
'''

def chatdata_insight_v2(origin_question):

    try:
        validity_result = validate_question(origin_question)
    except Exception as e:
        print(f"ERROR:     Error occurred during validatquing question: {e}")
        return RESPONSE_MODEL  

    
    print("-------validity:",validity_result['validity'])

   
    if validity_result['validity'] == True or validity_result['validity'] == "True" :
        try:
            response = primary_agent(origin_question)
        except Exception as e:
            print(f"ERROR:     Error occurred during executing primary agent: {e}")
            return RESPONSE_MODEL

        # print("integration result:", result)
        return response

    else:
        return RESPONSE_MODEL
