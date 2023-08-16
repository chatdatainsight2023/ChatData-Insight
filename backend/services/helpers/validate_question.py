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


QUESTION_VALIDATE_PROMPT = """
As an AI investment research expert focusing on web3 and blockchain, your key responsibility is to evaluate the relevance of user inquiries to these professional fields.

Your skills include:
- Answering professional questions related to web3 and blockchain.
- Retrieving on-chain data, such as balances, Ethereum ENS, transaction histories, contracts, etc.
- Extracting information from third-party graph platforms, including data on token prices, Dex transaction data, stablecoin data, and staking/locking data of specific tokens.
- Providing detailed information about most crypto projects.

Take note that:
- Consultative questions directly related to these professional domains are considered valid.
- Non-professional or unrelated questions are considered invalid.

For instance:
- Valid questions include 'What's today's price trend of Bitcoin?' or 'What's the trading volume of stablecoins in the last 24 hours?'.
- Invalid inquiries include 'Hello', 'Do I look handsome today?', empty question '', or 'How's the weather today?' and so on.

Simply put, you should respond with 'True' if the question is professionally relevant, and 'False' if it's not.
"""

def validate_question(x):
    
    response_schemas = [
        ResponseSchema(name='validity', description="'validity' represents the validity of the question. When the answer is invalid, the value is 'False'. When the answer is valid, the value is 'True'."),
        ResponseSchema(name='problem', description="problem is the question itself.")
    ]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

    format_instructions = output_parser.get_format_instructions()

    prompt = PromptTemplate(
        template=QUESTION_VALIDATE_PROMPT+"\n{format_instructions}\n{question}",
        input_variables=["question"],
        partial_variables={"format_instructions": format_instructions}
    )

    model = LLM 
    _input = prompt.format_prompt(question=x)
    output = model(_input.to_string())
    
    # 检查 output 是否嵌入在 Markdown 代码块中的 JSON
    if not output.startswith('```json') or not output.endswith('```'):
        # 进行转换
        json_str = output.strip('```').strip()
        json_obj = json.loads(json_str)
        formatted_json = json.dumps(json_obj, indent=4)
        output = '```json\n' + formatted_json + '\n```'


    result = output_parser.parse(output)

    print("question validity:", result)

    return result