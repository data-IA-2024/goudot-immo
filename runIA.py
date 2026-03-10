from dotenv import load_dotenv  # pip install python-dotenv

from langchain_deepseek import ChatDeepSeek
#from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain.tools import tool
#from langgraph.checkpoint.memory import InMemorySaver
#from langchain.chains import ConversationChain
#from langchain.memory import ConversationBufferMemory  # This import is correct
#from langgraph.checkpoint.postgres import PostgresSaver

import os, json
from dataclasses import dataclass

load_dotenv()

model = ChatDeepSeek(
    model="deepseek-chat",
    max_tokens=1000,
)

from langchain.agents import create_agent

@dataclass
class Bien:
    type : str
    address : str
    surface : int

@tool
def estimate(bien: Bien):
    """
    Estimate price of real estate
    :param bien: description of real estate with address, type (house/appartment), surface
    :return: estimated price
    """
    return (f"estimation de votre {bien.type} : 100000€")


agent = create_agent(
    model=model,
    tools=[estimate],
    system_prompt="You are a helpful assistant",
)

response = agent.invoke(
    {"messages": [{"role": "user",
                   "content": "estime le prix de ma maison située au centre de Blois, elle fait 100m2"}]}
)

#print(response)
#print('')

for message in response["messages"]:
    print(message)

