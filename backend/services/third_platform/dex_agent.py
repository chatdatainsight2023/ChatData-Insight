import os
import sys
import re

from services.third_platform.dune import dune_dex_exchange_volume
from services.third_platform.dune import dune_weekly_dex_exchange_volume_by_chain
from services.third_platform.dune import dune_daily_dex_exchange_volume

from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain import OpenAI,  LLMChain
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish
from core.config import Config

current_directory = os.path.dirname(os.path.realpath(__file__))
backend_directory = os.path.abspath(os.path.join(current_directory,"..",".."))
sys.path.insert(0, backend_directory)

os.environ["OPENAI_API_KEY"] = Config.SECONDARY_AGNET_OPENAI_API_KEY
MODEL_NAME = Config.MODEL_NAME
LLM = OpenAI(temperature=0,model_name=MODEL_NAME)  


# Set up the base template
DEX_AGENT_PROMPT_V1 = """ Assume you're a master of on-chain data analysis. 
Your task is to understand the type and scope of data the user is seeking, based on their input. 
Choose the most suitable tools to retrieve this data from the blockchain. Upon obtaining the data, 
you're required to synthesize it in response to the user's original question.if you find one or more image links, the answer must contains them,they are come from data

Here is the flow you should follow:
1. Interpretation: Understand the user's query and identify what type of data and which aspects they are interested in.
2. Selection: Choose the best tools from your repertoire to retrieve the desired data.
3. Execution: Use these tools to obtain the necessary data from the blockchain.
4. Response: Analyze the obtained data and formulate a comprehensive and understandable answer that directly addresses the user's original query.

You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the {input} to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times), 
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin! Remember to speak as a pirate when giving your final answer. Use lots of "Arg"s

Question: {input}
{agent_scratchpad}"""


# Set up the base template
DEX_AGENT_PROMPT_V2 = """
As an investment analysis expert, please answer the following questions using language and perspectives that align with the field. 
Your responses should include summary text and image links where applicable. If you encounter an image link, remember that the valid format should resemble '[Chart Name](https://demo.chatdatainsight.com/api/static/image/chart_2023-07-11_16_Za3qvS3H.png)'. 
However, please note that the provided example is not a valid image link, and you must extract a valid link from the answer generated by the tool. If no images are available, there is no need to include an image link in your response. 
Please avoid using special characters such as '-'. 
Ensure that your answers are based on the content observed without improvisation. 
Remember not to overlook the image link and do not modify it; it must be a valid image link that you have observed. This is crucial for the user experience.
You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the {input} to the action, {input} is the question itself. Please do not modify it.
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin! Remember to speak as a pirate when giving your final answer. Use lots of "Arg"s

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
            raise ValueError(f"dex agent could not parse LLM output: `{llm_output}`")
        
        action = match.group(1).strip()
        action_input = match.group(2)
        # Return the action and action input
        return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)


def dex_agent(question):

    llm = LLM

    tools = [
        Tool(
            name="DEX Daily Volume or Market Share",
            func=dune_dex_exchange_volume,
            description="Useful for answering questions about daily trading volumes or market shares of a specific decentralized exchange."
        ),
        Tool(
            name="DEX Weekly Volume by Blockchain",
            func=dune_weekly_dex_exchange_volume_by_chain,
            description="Useful for answering questions about weekly trading volumes of decentralized exchanges across different blockchains."
        ),
        Tool(
            name="DEX Daily Overall Trading Volume",
            func=dune_daily_dex_exchange_volume,
            description="Useful for answering questions about the overall daily trading volumes of all decentralized exchanges."
        )
    ]

    prompt = CustomPromptTemplate(
        template=DEX_AGENT_PROMPT_V2,
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
        allowed_tools=tool_names,
        max_iterations = 2
    )


    # agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
    # result = agent.run(question)

    agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)
    result = agent_executor.run(question)
    

    print("**** dex agent result:", result)

    return result
