import openai as openai
import os
import sys

from core.config import Config

from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

current_directory = os.path.dirname(os.path.realpath(__file__))
backend_directory = os.path.abspath(os.path.join(current_directory,"..",".."))
sys.path.insert(0, backend_directory)

# os.environ["OPENAI_API_KEY"] = Config.OPENAI_API_KEY
MODEL_NAME = Config.MODEL_NAME
LLM = OpenAI(temperature=0,model_name=MODEL_NAME)  


# question decomposition

TASK_DECOMPOSITION_PROMPT = """
Assume you are a product manager, 
your task now is to break down the user's questions into different needs to come up with various answering schemes. 
Each user's question can be decomposed into up to 5 needs.

For example, the user's question 'List the recent valuable project airdrops and the specific steps to participate in them' can be broken down into two needs. 
The first need is 'What are the recent valuable airdrops?', and the second one is 'How to participate in these airdrops?'.

However, the question 'Provide me with the most active DApps on the Ethereum blockchain in the past month, along with a summary analysis of their activity' should be decomposed into one question, 
'Can you provide me with a list of the most active DApps on the Ethereum blockchain in the past month?'. 
Even though there is an analysis need, it is based on the result of the first question, 
which will be solved in the next step, so it does not need to be extracted.

Another example,'What is the market share about different stable coins?',it's no need to break down.

Therefore, the core logic is to extract independent questions. 
Whenever there is a dependency relationship between questions, only the first question needs to be extracted.

Additionally, when you determine that the problem only has one requirement, there is no need to unpack it, just keep the problem as is.

"""

DISCRIPTION_PROMPT = """
'task_id_1' is the identifier for the first requirement derived from the given question. 
For example, if the question is 'List the recent valuable project airdrops and the specific steps to participate in them', 
it implies that there are two requirements associated with this question. 
The first requirement is to determine 'What are the recent valuable airdrop projects?' 
Thus, 'task_id_1' corresponds to 'What are the recent valuable airdrop projects?' 
The second requirement pertains to 'How to participate in airdrop projects?' 
Consequently, 'task_id_2' corresponds to 'How to participate in airdrop projects?' and so on for subsequent requirements. 
If no further questions can be extracted, 'task_id_x' corresponds to 'none'. 
For example, in the given question, if only two questions can be extracted, then 'task_id_3', 'task_id_4', 'task_id_5', and so on, 
would all correspond to 'none'
"""

def decompose_question(question):

    print("-----question need to decompose:", question)

    response_schemas = [
        ResponseSchema(name="task_id_1", description=DISCRIPTION_PROMPT),
        ResponseSchema(name="task_id_2", description=DISCRIPTION_PROMPT),
        ResponseSchema(name="task_id_3", description=DISCRIPTION_PROMPT),
        ResponseSchema(name="task_id_4", description=DISCRIPTION_PROMPT),
        ResponseSchema(name="task_id_5", description=DISCRIPTION_PROMPT),
    ]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

    format_instructions = output_parser.get_format_instructions()

    prompt = PromptTemplate(
        template=TASK_DECOMPOSITION_PROMPT+"\n{format_instructions}\n{question}",
        input_variables=["question"],
        partial_variables={"format_instructions": format_instructions}
    )

    model = LLM

    _input = prompt.format_prompt(question=question)
    output = model(_input.to_string())
    result = output_parser.parse(output)

    # print("-----question decompose result:", type(result))
    print("-----question decompose result:", result)

    return result

# decompose_question("Can you help me check the market share of stablecoin?")