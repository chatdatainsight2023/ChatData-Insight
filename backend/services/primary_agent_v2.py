import json
import openai 
import os
import sys
import traceback

current_directory = os.path.dirname(os.path.realpath(__file__))
backend_directory = os.path.abspath(os.path.join(current_directory,"..",".."))
sys.path.insert(0, backend_directory)

from core.config import Config
os.environ["OPENAI_API_KEY"] = Config.OPENAI_API_KEY

from services.third_platform.dune import stablecoin_supply_and_growth
from services.third_platform.dune import dune_dex_exchange_volume as dex_exchange_volume_or_market_share
from services.third_platform.dune import dune_weekly_dex_exchange_volume_by_chain as dex_exchange_volume_by_chain
from services.third_platform.dune import dune_daily_dex_exchange_volume as daily_dex_exchange_volume
from services.third_platform.binance import get_token_price_trend as token_price_info
from services.main_project.moonbeam.moonbeam import moonbeam_query_engine as moonbeam_details
from services.main_project.ethereum.airstack_and_quicknode import fetch_token_balance as token_balances_on_the_ethereum_platform
from services.main_project.ethereum.airstack_and_quicknode import fetch_transfers_history as token_transfer_records_on_the_ethereum
# from services.main_project.ethereum.airstack_and_quicknode import fetch_identity as eth_address_information_for_ethereum_ens
from services.main_project.ethereum.airstack_and_quicknode import query_contract as contract_info_on_the_ethereum
# from services.main_project.ethereum.airstack_and_quicknode import query_ensname as eth_ens_information_for_ethereum_address
from services.third_platform.coin_glass import get_liquidation_top as get_liquidation_data

def primary_agent(question):

    try:

        print("-----primary agent get question:",question)

        if question == None:
            return "I'm sorry, I couldn't find any relevant info at the moment. You may try asking other questions."


        # Step 1: send the conversation and available functions to GPT
        prompt = f'''As an investment research analyst, you will often call a specific function to answer the question "{question}". If the question is related to a specific function, please call it directly. The output from this function may exist in one of two forms: text with an image link or text without an image link.
        Your role is to provide investment advice based on the returned results of the function and then deliver it to the user.
        If the function returns an image link along with text, please remember to include an exclamation mark '!' immediately before the image link. This is crucial for the frontend to correctly render the chart and display it to the user, rather than just showing a plain image link.
        For example, your answer should be formatted like this:
        ![image](https://demo.chatdatainsight.com/api/static/image/dex_daily_trading_volume_chart_2023-07-14_04_SFxD9gwK.png)
        By following this format, the frontend will be able to directly display the chart to the user.
        If the function only provides text without an image link, your final answer should consist of text only. Remember! There is no need to mention the absence of an image link or any graphical data in such cases.
        These guidelines are essential to ensure clarity and proper rendering of the output. Please adhere to them while formulating your answers. If you have any further questions, feel free to ask.'''


        messages = [{"role": "user", "content": prompt}]

        functions = [
            {
                "name": "stablecoin_supply_and_growth",
                "description": "Useful for answering questions about stablecoin, such as 'What is the market share about different stable coin?'",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "a question about stablecoin, e.g. 'What is the market share about different stablecoin?' ",
                        },
                    },
                    "required": ["question"],
                },
            },
            {
                "name": "dex_exchange_volume_or_market_share",
                "description": "Useful for answering questions about daily trading volumes or market shares of a specific decentralized exchange.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "a question about daily dex exchange volume or dex market share, e.g.'Can you help me check the daily exchange volume of dex?' ",
                        },
                    },
                    "required": ["question"],
                },
            },
            {
                "name": "dex_exchange_volume_by_chain",
                "description": "Useful for answering questions about trading volumes of decentralized exchanges across different blockchains",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "a question about dex exchange volume by different chain, e.g. 'Can you help me check the trading volumes of exchanges on various blockchains?' ",
                        },
                    },
                    "required": ["question"],
                },
            },
            {
                "name": "daily_dex_exchange_volume",
                "description": "Useful for answering questions about the overall daily trading volumes of all decentralized exchanges",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "a question about the daily trading volume of dex, e.g. 'What is the daily trading volume of dex?'",
                        },
                    },
                    "required": ["question"],
                },
            },
            {
                "name": "token_price_info",
                "description": "Useful for addressing queries about the token price of a specific project, including price trends, highs and lows, etc.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "a question about token price, e.g. 'What's the recent price trend of BTC over the last few hours?'",
                        },
                    },
                    "required": ["question"],
                },
            },
            {
                "name": "moonbeam_details",
                "description": "Useful for answering questions about the details of moonbeam, such as 'How many DApps are there on Moonbeam?' or 'How many stablecoins are available on Moonbeam?'",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "a question about moonbeam info, e.g. 'What are the recent major technical updates on Moonbeam?' ",
                        },
                    },
                    "required": ["question"],
                },
            },
            {
                "name": "token_balances_on_the_ethereum_platform",
                "description": "Useful for when you need to check the token balance of a specific eth address on ethereum.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "a question about token balance on ethereum blockchain, e.g. 'Can you help me check the token balance for the Ethereum address: '0xEf1c6E67703c7BD7107eed8303Fbe6EC2554BF6B?'",
                        },
                    },
                    "required": ["question"],
                },
            },
            {
                "name": "token_transfer_records_on_the_ethereum",
                "description": "Useful for when you need to examine the transfer records of a specific address on ethereum.For example:'Check the recent transfer records of this eth account 0xEf1c6E67703c7BD7107eed8303Fbe6EC2554BF6B'",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "a question about the transfer records of a specific address on Ethereum, e.g. 'Check the recent transfer records of this account 0xEf1c6E67703c7BD7107eed8303Fbe6EC2554BF6B' ",
                        },
                    },
                    "required": ["question"],
                },
            },
            {
                "name": "contract_info_on_the_ethereum",
                "description": "Useful for when you need to examine the details of a contract using its address",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "a question about a contract, e.g. 'Can you help me examine the details of this contract: 0xf2A22B900dde3ba18Ec2AeF67D4c8C1a0DAB6aAC?'",
                        },
                    },
                    "required": ["question"],
                },
            },
            {
                "name": "get_liquidation_data",
                "description": "Useful for when you need to answer question related to crypto currency liquidation data",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "a question about crypto currency liquidation info, e.g. 'Please help me check the recent cryptocurrency liquidation data'",
                        },
                    },
                    "required": ["question"],
                },
            },
        ]

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=messages,
                functions=functions,
                function_call="auto",
            )

            print("*** step1:",response['choices'][0]['message'])
            response_message = response["choices"][0]["message"]

            # Step 2: check if GPT wanted to call a function
            if response_message.get("function_call"):
                # Step 3: call the function
                available_functions = {
                    "stablecoin_supply_and_growth":stablecoin_supply_and_growth,
                    "dex_exchange_volume_or_market_share":dex_exchange_volume_or_market_share,
                    "dex_exchange_volume_by_chain":dex_exchange_volume_by_chain,
                    "daily_dex_exchange_volume":daily_dex_exchange_volume,
                    "token_price_info":token_price_info,
                    "moonbeam_details":moonbeam_details,
                    "token_balances_on_the_ethereum_platform":token_balances_on_the_ethereum_platform,
                    "token_transfer_records_on_the_ethereum":token_transfer_records_on_the_ethereum,
                    # "eth_address_information_for_ethereum_ens":eth_address_information_for_ethereum_ens,
                    "contract_info_on_the_ethereum":contract_info_on_the_ethereum,
                    # "eth_ens_information_for_ethereum_address":eth_ens_information_for_ethereum_address,
                    "get_liquidation_data":get_liquidation_data,
                }
                function_name = response_message["function_call"]["name"]
                function_to_call = available_functions[function_name]
                function_args = json.loads(response_message["function_call"]["arguments"])

                try:
                    # Call the function with its respective arguments
                    if function_name == "stablecoin_supply_and_growth":
                        function_response = function_to_call(
                            question=function_args.get("question"),
                        )
                    elif function_name == "dex_exchange_volume_or_market_share":
                        function_response = function_to_call(
                            question=function_args.get("question"),
                        )
                    elif function_name == "dex_exchange_volume_by_chain":
                        function_response = function_to_call(
                            question=function_args.get("question"),
                        )
                    elif function_name == "daily_dex_exchange_volume":
                        function_response = function_to_call(
                            question=function_args.get("question"),
                        )
                    elif function_name == "token_price_info":
                        function_response = function_to_call(
                            question=function_args.get("question"),
                        )
                    elif function_name == "moonbeam_details":
                        function_response = function_to_call(
                            question=function_args.get("question"),
                        )
                    elif function_name == "token_balances_on_the_ethereum_platform":
                        function_response = function_to_call(
                            question=function_args.get("question"),
                        )
                    elif function_name == "token_transfer_records_on_the_ethereum":
                        function_response = function_to_call(
                            question=function_args.get("question"),
                        )
                    elif function_name == "contract_info_on_the_ethereum":
                        function_response = function_to_call(
                            question=function_args.get("question"),
                        )
                    elif function_name == "get_liquidation_data":
                        function_response = function_to_call(
                            question=function_args.get("question"),
                        )
                    else:
                        raise ValueError(f"Unsupported function: {function_name}")

                except Exception as err:
                    print(f"An error occurred while calling function: {function_name}")
                    print(f"Error: {err}")
                    traceback.print_exc()  
                    return "I'm sorry, I couldn't find any relevant info at the moment. You may try asking other questions."

                # Step 4: send the info on the function call and function response to GPT
                messages.append(response_message)  
                messages.append(
                    {
                        "role": "function",
                        "name": function_name,
                        "content": function_response,
                    }
                )  
                second_response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-0613",
                    messages=messages,
                )

                final_response = second_response['choices'][0]['message']['content']
                print("*** step2:",final_response)

                if final_response:
                    return final_response
                else:
                    raise ValueError("Response content is empty.")  

            else:

                return "I'm sorry, I couldn't find any relevant info at the moment. You may try asking other questions."

        except Exception as e:
            print(f"An error occurred during the conversation: {e}")
            return "I'm sorry, I couldn't find any relevant info at the moment. You may try asking other questions."

    except Exception as unexpected_error:
        print(f"An unexpected error occurred: {unexpected_error}")
        return "I'm sorry, I couldn't find any relevant info at the moment. You may try asking other questions."

