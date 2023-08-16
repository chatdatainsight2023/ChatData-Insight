import requests
import os
import sys
import json

from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain import OpenAI,  LLMChain
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish, OutputParserException
import re

current_directory = os.path.dirname(os.path.realpath(__file__))
backend_directory = os.path.abspath(os.path.join(current_directory,"..",".."))
sys.path.insert(0, backend_directory)

API_KEY = '1070b58dcadf4b6eabd668dab22cfdca'
URL = "https://api.airstack.xyz/gql"

from core.config import Config
os.environ["OPENAI_API_KEY"] = Config.OPENAI_API_KEY
MODEL_NAME = Config.MODEL_NAME
LLM = OpenAI(model_name=MODEL_NAME, temperature=0)  

import logging
# Create a custom logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

import json
import requests
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


# extract params from question

JUDGEMENT_PROMPT = '''
Assuming you are an expert in keyword extraction, 
your task is to extract key terms from user inquiries that will be used to retrieve blockchain-related information.
These keywords are often wallet addresses, ENS domain names, and the like. 
For example, in the question 'can you check the balance of this address 0x60e4d786628fea6478f785a6d7e704777c86a7c6?', 
the extracted parameter would be '0x60e4d786628fea6478f785a6d7e704777c86a7c6'.
Another question:'Check the recent transfer records of this account 0xEf1c6E67703c7BD7107eed8303Fbe6EC2554BF6B',
the extracted parameter would be '0xEf1c6E67703c7BD7107eed8303Fbe6EC2554BF6B'
'''

def get_query_params(x):
    response_schemas = [
      ResponseSchema(name="question", description="question is the problem itself.for example,'Check the recent transfer records of this account 0xEf1c6E67703c7BD7107eed8303Fbe6EC2554BF6B.',would be 'Check the recent transfer records of this account 0xEf1c6E67703c7BD7107eed8303Fbe6EC2554BF6B.'"),
      ResponseSchema(name="params", description="The parameter extracted from the question, for instance 'can you check the balance of this address 0x60e4d786628fea6478f785a6d7e704777c86a7c6?', would be '0x60e4d786628fea6478f785a6d7e704777c86a7c6'.")
    ]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

    format_instructions = output_parser.get_format_instructions()

    prompt = PromptTemplate(
        template=JUDGEMENT_PROMPT+"\n{format_instructions}\n{question}",
        input_variables=["question"],
        partial_variables={"format_instructions": format_instructions}
    )

    model = LLM

    _input = prompt.format_prompt(question=x)
    output = model(_input.to_string())
    result = output_parser.parse(output)

    print("INFO:     Judge Result:", result)

    return result


# Headers
HEADERS = {
     "Content-Type": "application/json",
     "authorization": API_KEY
}


# query token balance

def fetch_token_balance(question):

    data = get_query_params(question)
    owner_address = data['params']

    TOKEN_BALANCE = f''' 
    query QB5 {{
      TokenBalances(input: {{filter: {{ owner: {{_eq: "{owner_address}"}}}}, limit: 3, blockchain: ethereum}}) {{
        TokenBalance {{
          amount
          chainId
          id
          lastUpdatedBlock
          lastUpdatedTimestamp
          owner {{
            addresses
          }}
          tokenAddress
          tokenId
          tokenType
          token {{
            name
            symbol
          }}
        }}
      }}
    }}
    '''

    # Make the request
    response = requests.post(URL, headers=HEADERS, json={'query': TOKEN_BALANCE})

    # Parse the response
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=4))  # print the data
        return data
    else:
        return {"error": "Query failed", "status_code": response.status_code}



# fetch_token_balance(question)

# query token transfer

def fetch_transfers_history(question):

    data = get_query_params(question)
    token_address = data['params']

    TOKEN_TRANSFERS = f''' 
    query MyQuery {{
      TokenTransfers(
        input: {{filter: {{tokenAddress: {{_eq: "{token_address}"}}}}, blockchain: ethereum}}
      ) {{
        TokenTransfer {{
          amount
          amounts
          blockNumber
          blockTimestamp
          blockchain
          chainId
          from {{
            addresses
          }}
          to {{
            addresses
          }}
          tokenType
        }}
      }}
    }}
    '''

    # Make the request
    response = requests.post(URL, headers=HEADERS, json={'query': TOKEN_TRANSFERS})

    # Parse the response
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=4))  # print the data
        return data
    else:
        return {"error": "Query failed", "status_code": response.status_code}



# fetch_transfers_history(question)



# query identity

def fetch_identity(identity: str):

    data = get_query_params(identity)
    domain_name = data['params']


    IDENTITY_QUERY = f''' 
    query identity {{
      Wallet(input: {{identity: "{domain_name}", blockchain: ethereum}}) {{
        socials {{
          dappName
          profileName
          profileCreatedAtBlockTimestamp
          userAssociatedAddresses
        }}
        tokenBalances {{
          tokenAddress
          amount
          tokenId
          tokenType
          tokenNfts {{
            contentValue {{
              image {{
                original
              }}
            }}
            token {{
              name
            }}
          }}
        }}
      }}
    }}
    '''

    # Make the request
    response = requests.post(URL, headers=HEADERS, json={'query': IDENTITY_QUERY})

    # Parse the response
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=4))  # print the data
        return data
    else:
        return {"error": "Query failed", "status_code": response.status_code}



# fetch_identity(question)



# Define the GraphQL endpoint and API key
quicknode_endpoint = "https://api.quicknode.com/graphql"
api_key = "QN_0ebeb3e022f541b086412061a6640159"

# Set up the GraphQL client
transport = RequestsHTTPTransport(url=quicknode_endpoint, headers={'x-api-key': api_key}, use_json=True)
client = Client(transport=transport, fetch_schema_from_transport=True)


# query ensname via wallet address
def query_ensname(question):
   
    data = get_query_params(question)
    wallet_address = data['params']

    # Define the GraphQL query to get wallet address
    query = gql("""
    query Query($address: String!) {
        ethereum {
            walletByAddress(address: $address) {
                ensName
            }
        }
    }
    """)

    # Set the address
    variables = {
        "address": wallet_address,
    }

    # Execute the query and print the result
    result = client.execute(query, variable_values=variables)

    print("ensname:", type(result))

    return str(result)



# query_ensname(question)

# query contract detials via contract address

def query_contract(question):

    data = get_query_params(question)
    contract_address = data['params']

    # Define the GraphQL query to get wallet address
    query = gql("""
    query Query($contractAddress: String!) {
        ethereum {
            contract(contractAddress: $contractAddress) {
                address
                isVerified
                name
                symbol
                supportedErcInterfaces
            }
        }
    }
    """)

    # Set the address
    variables = {
        "contractAddress": contract_address,
    }

    # Execute the query and print the result
    result = client.execute(query, variable_values=variables)

    print("contract details:", type(result))

    return str(result)