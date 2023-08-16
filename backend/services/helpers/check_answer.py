
import openai as openai
import json
import os
import sys

from core.config import Config

from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

current_directory = os.path.dirname(os.path.realpath(__file__))
backend_directory = os.path.abspath(os.path.join(current_directory,"..",".."))
sys.path.insert(0, backend_directory)

os.environ["OPENAI_API_KEY"] = Config.OPENAI_API_KEY
MODEL_NAME = Config.MODEL_NAME
LLM = OpenAI(temperature=0,model_name=MODEL_NAME)  

ANSWER_JUDGEMENT_PROMPT = "As a language expert, it is your task to assess whether a given response is valid or an exception. A response is deemed invalid if its meaning aligns closely with 'Agent stopped due to iteration limit or time limit.' However, if it deviates from this scenario, the response is classified as valid."

def check_answer(x):
    response_schemas = [
        ResponseSchema(name="validity", description="'validity' represents the validity of the answer. When the answer is invalid, the value is 'no'. When the answer is valid, the value is 'yes'."),
        ResponseSchema(name="question", description="question is the problem itself.")
    ]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

    format_instructions = output_parser.get_format_instructions()

    prompt = PromptTemplate(
        template=ANSWER_JUDGEMENT_PROMPT+"\n{format_instructions}\n{question}",
        input_variables=["question"],
        partial_variables={"format_instructions": format_instructions}
    )

    model = LLM 

    _input = prompt.format_prompt(question=x)
    output = model(_input.to_string())
    result = output_parser.parse(output)

    print("INFO:   Answer Validity Judge Result:", result)

    return result