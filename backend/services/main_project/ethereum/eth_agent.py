
from langchain.llms import OpenAI
from langchain.agents import  Tool
from core.config import Config
MODEL_NAME = Config.MODEL_NAME
LLM = OpenAI(model_name=MODEL_NAME, temperature=0)  

from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain import OpenAI,  LLMChain
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish, OutputParserException
import re


from services.main_project.ethereum.airstack_and_quicknode import fetch_token_balance
from services.main_project.ethereum.airstack_and_quicknode import fetch_transfers_history
from services.main_project.ethereum.airstack_and_quicknode import fetch_identity
from services.main_project.ethereum.airstack_and_quicknode import query_contract
from services.main_project.ethereum.airstack_and_quicknode import query_ensname

# question = "Could you please assist me in looking up the account with the domain name 'vitalik.eth'?"
# question = "Can you help me examine the details of this contract: 0xf2A22B900dde3ba18Ec2AeF67D4c8C1a0DAB6aAC?"
# question = "Please check what is the ENS associated with the account 0xEf1c6E67703c7BD7107eed8303Fbe6EC2554BF6B"
# question = "Check the recent transfer records of this account 0xEf1c6E67703c7BD7107eed8303Fbe6EC2554BF6B."
# question = "Can you check how many kinds of tokens the address 0xEf1c6E67703c7BD7107eed8303Fbe6EC2554BF6B has?"

# onchain_info_agent(question)


# Set up the base template
SUB_AGENT_PROMPT_V1 = """Assume you're a master of on-chain information indexing. 
Your task now is to interpret user queries to understand what information they are seeking. 
Once you've clarified their requirements, you must choose the appropriate tools to retrieve the data. 
If there are no corresponding tools for the type of data the user wishes to query, you should respond, 
'I'm sorry, I can't answer this question at the moment,' and suggest where they can find the required information.s

You can use the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: you should input {input} as param of tool
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin! Remember to speak as a pirate when giving your final answer. Use lots of "Arg"s

Question: {input}
{agent_scratchpad}"""


# Set up the base template
SUB_AGENT_PROMPT_V2 = """Assume you're an investment research analyst with in-depth expertise in the areas of blockchain, web3, and artificial intelligence.
Now, your task is to use this knowledge to answer the upcoming questions in the most professional way. Before responding, carefully consider the purpose of each tool and whether it matches the question you need to answer.
You can use the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Action: the action to take, should be one of [{tool_names}]
Action Input: you should input {input} as the parameter of the selected tool

Begin! Choose the appropriate tool to obtain the answer and provide the observed result as your final response.

Question: {input}
{agent_scratchpad}"""

# Set up a prompt template
class CustomPromptTemplate(StringPromptTemplate):
    # The template to use
    template: str
    # The list of tools available
    tools: List[Tool]

    def format(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        # Set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts
        # Create a tools variable from the list of tools provided
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        # Create a list of tool names for the tools provided
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        return self.template.format(**kwargs)

class CustomOutputParser(AgentOutputParser):

    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Check if agent should finish
        if "Final Answer:" in llm_output:
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment :)
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output,
            )
        # Parse out the action and action input
        regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            raise OutputParserException(f"Could not parse LLM output: `{llm_output}`")
        action = match.group(1).strip()
        action_input = match.group(2)
        # Return the action and action input
        return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)

def eth_agent(question: str):

    llm = LLM

    # Define which tools the agent can use to answer user queries
    tools = [
        Tool(
            name="token balance info",
            func=fetch_token_balance,
            description="Useful for when you need to check the token balance of a specific address."
        ),
        Tool(
            name="transfers history info",
            func=fetch_transfers_history,
            description="Useful for when you need to examine the transfer records of a specific address.for example:'Check the recent transfer records of this account 0xEf1c6E67703c7BD7107eed8303Fbe6EC2554BF6B'"
        ),
        Tool(
            name="ens' address info",
            func=fetch_identity,
            description="Useful for when you need to obtain the identity information associated with a specific ENS name."
        ),
        Tool(
            name="contract info",
            func=query_contract, 
            description="Useful for when you need to examine the details of a contract using its address."
        ),
        Tool(
            name="address' ensname info ",
            func=query_ensname, 
            description="Useful when you want to query the ENS domain name via a specific wallet address.for example:'Please check what is the ENS associated with the account 0xEf1c6E67703c7BD7107eed8303Fbe6EC2554BF6B'"
        ),
    ]

    prompt = CustomPromptTemplate(
        template=SUB_AGENT_PROMPT_V2,
        tools=tools,
        # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
        # This includes the `intermediate_steps` variable because that is needed
        input_variables=["input", "intermediate_steps"]
    ) 

    output_parser = CustomOutputParser()

    # LLM chain consisting of the LLM and a prompt
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    tool_names = [tool.name for tool in tools]
    agent = LLMSingleActionAgent(
        llm_chain=llm_chain,
        output_parser=output_parser,
        stop=["\nObservation:"],
        allowed_tools=tool_names
    )

    agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)

    result = agent_executor.run(question)

    print("INFO:     Sub Agent Result:", result)

    return result