import openai

import sys
import os
import json
import threading
import queue

from langchain.llms import OpenAI
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

current_directory = os.path.dirname(os.path.realpath(__file__))
backend_directory = os.path.abspath(os.path.join(current_directory))
sys.path.insert(0, backend_directory)

# sys.path.insert(0, '/Users/qinjianquan/Career/redstone-network/chatdata-insight/backend')

from core.config import Config
openai.api_key = Config.OPENAI_API_KEY
MODEL_NAME = Config.MODEL_NAME
LLM = OpenAI(model_name=MODEL_NAME, temperature=0)  


def conversation(prompt):
     
     message = chat_with_gpt(prompt)

     return message

def chat_with_gpt(input):

    prom = """You are an omniscient artificial intelligence, please assist users in solving various problems"""

    conv = Conversation(prom, 20)
    return conv.ask(input) 

# upgrade
class Conversation:
    def __init__(self, prompt, num_of_round):
        self.prompt = prompt
        self.num_of_round = num_of_round
        self.messages = []
        self.messages.append({"role": "system", "content": self.prompt})

    def ask(self, question):
        try:
            self.messages.append({"role": "user", "content": question})
            response = openai.ChatCompletion.create(
                model="gpt-4-0613",
                messages=self.messages,
                # stream=True,
                temperature=0.5,
                max_tokens=2048,  
                top_p=1,
            )
        except Exception as e:
            print(e)
            return e

        message = response["choices"][0]["message"]["content"]
        self.messages.append({"role": "assistant", "content": message})

        if len(self.messages) > self.num_of_round*2 + 1:
            del self.messages[1:21] # Remove the first round conversation left.
        return message



# prompt = "假设你是一个家庭服务聊天机器人，你需要回答一些关于家庭生活的日常问题"
# num_of_round = 5  # 对话轮数
# conversation = Conversation(prompt, num_of_round)

# question = "我烧伤了，应该怎么办？"
# print(conversation.ask(question))



from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage,
)

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain

from langchain.schema import (
    HumanMessage,
    SystemMessage
)


ANSWER_PROMPT = '''
Suppose you are an information organization expert. Your goal is to integrate and compile resources including text and image links, and then present them in a smooth, professional way to end users, and the content you output is directly facing users.

Please note that sometimes the source material may not contain image links. In this case, the project output only contains textual content. However, when image links are included in the source material, we will incorporate them into the final output.

Let's illustrate with an example:

Suppose we receive the following input:

'Over the past 24 hours, Bitcoin opened at 25647.69, reached a high of 25792.3, dropped to a low of 25571.37, and finally closed at 25727.3. This suggests that Bitcoin has been relatively stable in the past few hours. https://demo.chatdatainsight.com/api/static/image/chart.png'

The output will be:

'Over the past 24 hours, Bitcoin opened at 25647.69, reached a high of 25792.3, dropped to a low of 25571.37, and finally closed at 25727.3. This suggests that Bitcoin has been relatively stable in the past few hours. ![Bitcoin Price Chart](https://demo.chatdatainsight.com/api/static/image/chart.png) If you are considering making an investment, we recommend that you visit an exchange to view price trends over a longer period. If the current price is relatively low, the investment risk may be significantly lower compared to when the price is at a high point.'

Remember, your aim is to provide users with detailed, accurate and easy-to-understand information to assist them in making decisions."

'''

class ThreadedGenerator:
    def __init__(self):
        self.queue = queue.Queue()

    def __iter__(self):
        return self

    def __next__(self):
        item = self.queue.get()
        if item is StopIteration: raise item
        return item

    def send(self, data):
        self.queue.put(data)

    def close(self):
        self.queue.put(StopIteration)

class ChainStreamHandler(StreamingStdOutCallbackHandler):
    def __init__(self, gen):
        super().__init__()
        self.gen = gen

    def on_llm_new_token(self, token: str, **kwargs):
        self.gen.send(token)


def llm_thread(g, prompt):
    messages = [
    SystemMessage(content=ANSWER_PROMPT),
    HumanMessage(content=prompt)
    ]
    try:
        chat = ChatOpenAI(
            verbose=True,
            streaming=True,
            callbacks=[ChainStreamHandler(g)],
            temperature=0,
            model_name=MODEL_NAME
        )
        chat(messages)

    finally:
        g.close()


def stream_output(prompt):
    g = ThreadedGenerator()
    threading.Thread(target=llm_thread, args=(g, prompt)).start()
    return g


# def stream_output(prompt):

#     messages = [
#     SystemMessage(content=ANSWER_PROMPT),
#     HumanMessage(content=prompt)
#     ]
         
#     chat = ChatOpenAI(streaming=True, callbacks=[StreamingStdOutCallbackHandler()], temperature=0,model_name=MODEL_NAME)
#     return chat(messages)

DATA_SUMMARY_PROMPT = """
As an information organization expert, your task is to gather, organize, and present resources in a user-friendly and professional manner. This includes both textual data and image links.

For instance, your output could be something like:

'Over the last 24 hours, Bitcoin's performance has been stable. It opened at 25647.69, hit a high of 25792.3, dropped to a low of 25571.37, and closed at 25727.3. An illustrative chart is available at this link: https://demo.chatdatainsight.com/api/static/image/chart_2023-07-08_08_X1MW5rzr.png. 

Investors are encouraged to study long-term price trends at their preferred exchange. Notably, investing when prices are relatively low can significantly reduce investment risk.'

Keep in mind, the information you provide should help users make decisions. Ensure that the image link is a full URL.

Your main task is to generate a data summary rather than providing detailed information. When working with a large data set, try to extract and convey key features. For example, identify the top performers and highlight any outliers. Images can be used to present detailed data, but the accompanying text should be simple and clear. Avoid presenting extensive details, such as daily or weekly figures. Focus instead on summarizing data features like top performers, and unusual data points.
such as following content are not allow, presenting data is too detailed and contains the '-' symbol, please avoid answering questions in this way.:

'1. Arbitrum:
   - June 5, 2023: $2,048,245,073.64
   - June 12, 2023: $1,548,245,576.23
   - June 19, 2023: $2,149,053,537.14
   - June 26, 2023: $2,460,170,085.52
   - July 3, 2023: $1,540,155,370.60

2. Avalanche (C-Chain):
   - June 5, 2023: $48,793,789.70
   - June 12, 2023: $35,961,584.88
   - June 19, 2023: $47,643,463.10
   - June 26, 2023: $35,013,218.63
   - July 3, 2023: $30,868,496.16'

"""

def data_summary_v2(prompt):

    messages = [
    SystemMessage(content=DATA_SUMMARY_PROMPT),
    HumanMessage(content=prompt)
    ]
         
    chat = ChatOpenAI(streaming=True, callbacks=[StreamingStdOutCallbackHandler()], temperature=0,model_name=MODEL_NAME)

    print("------",dir(chat(messages)))
    
    return chat(messages)