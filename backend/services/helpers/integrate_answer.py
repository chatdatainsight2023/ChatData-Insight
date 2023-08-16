import openai as openai
import json
import os
import sys
from core.config import Config

from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage,
)
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI

from langchain.schema import (
    HumanMessage,
    SystemMessage
)

current_directory = os.path.dirname(os.path.realpath(__file__))
backend_directory = os.path.abspath(os.path.join(current_directory,"..",".."))
sys.path.insert(0, backend_directory)

os.environ["OPENAI_API_KEY"] = Config.OPENAI_API_KEY
MODEL_NAME = Config.MODEL_NAME
LLM = OpenAI(temperature=0,model_name=MODEL_NAME)  

# from backend.services.primary_agent_v1 import primary_agent
from services.primary_agent_v2 import primary_agent

# result integration

RESULT_INTEGRATION_PROMPT = '''Assume you're a master at summarizing complex information. 
In response to the question "{origin_question}", we've broken it down into multiple sub-questions, and received the following answers: {ans_dict}. 
Your task now is to synthesize this information into a concise, user-friendly summary that addresses the original question.
Please note that the summary should be coherent and directly related to the original question. It should provide the user with a clear and complete response based on the answers we've obtained from the sub-questions.
Furthermore, if you come across image links, it means that the image links are part of the answer. Please make sure to include the image links in the final response.
'''

def integrate_answer(origin_question,answer_dict):

    if not isinstance(answer_dict, dict):
        print("ERROR:     answer_dict must be a dictionary")
        return None

    if not isinstance(origin_question, str):
        print("ERROR:     origin_question must be a string")
        return None

    ans_dict = {}

    try:
        for _key, value in answer_dict.items():
            if value == 'none':
                break
            else:
                
                new_key = value
                
                try:
                    print(f'--------------INFO:     Key: {new_key}')
                   
                    # new_value = primary_agent(value)
                    new_value = primary_agent(new_key)
                    print(f'--------------INFO:     Value: {new_value}')
                   
                except Exception as e:
                    print(f"ERROR:     Error occurred while executing solution_selection: {e}")
                    continue
                ans_dict[new_key] = new_value
    except Exception as e:
        print(f"ERROR:     Error occurred during processing answer_dict: {e}")
        return None

    print("------ q&a dic:",ans_dict)

    try:
        multiple_input_prompt = PromptTemplate(
        input_variables=["origin_question", "ans_dict"], 
        template=RESULT_INTEGRATION_PROMPT
        )
    except Exception as e:
        print(f"ERROR:     Error occurred during the creation of PromptTemplate: {e}")
        return None

    try:
        _input=multiple_input_prompt.format(origin_question=origin_question, ans_dict=ans_dict)
    except Exception as e:
        print(f"ERROR:     Error occurred during the formatting of PromptTemplate: {e}")
        return None

    # print("INFO:     MULTIPLE INPUT:", _input)

    # try:
    #     model = LLM 
    # except Exception as e:
    #     print(f"ERROR:     Error occurred while creating OpenAI model: {e}")
    #     return None

    # try:
    #     res = model(_input)
    # except Exception as e:
    #     print(f"ERROR:     Error occurred while processing input with the OpenAI model: {e}")
    #     return None

    res = stream_output(origin_question,ans_dict)
    
    print("------ intergrate ans:",res)

    return res

PROMPT = f'''Assume you're a master at summarizing complex information. 
    In response to the question, we've broken it down into multiple sub-questions, and received a series of answers. 
    Your task now is to synthesize this information into a concise, user-friendly summary that addresses the original question.
    Please note that the summary should be coherent and directly related to the original question. It should provide the user with a clear and complete response based on the answers we've obtained from the sub-questions.
    Furthermore, if you come across image links, it means that the image links are part of the answer. Please make sure to include the image links in the final response.
    '''

def stream_output(origin_question,ans_dict):

    prompt = f'''Assume you're a master at summarizing complex information. 
    In response to the question '{origin_question}', we've broken it down into multiple sub-questions, and received the following answers: '{ans_dict}'. 
    Your task now is to synthesize this information into a concise, user-friendly summary that addresses the original question.
    Please note that the summary should be coherent and directly related to the original question. It should provide the user with a clear and complete response based on the answers we've obtained from the sub-questions.
    Furthermore, if you come across image links, it means that the image links are part of the answer. Please make sure to include the image links in the final response.
    '''

    messages = [
    SystemMessage(content=PROMPT),
    HumanMessage(content=prompt)
    ]
         
    chat = ChatOpenAI(streaming=True, callbacks=[StreamingStdOutCallbackHandler()], temperature=0,model_name=MODEL_NAME)
    return chat(messages)