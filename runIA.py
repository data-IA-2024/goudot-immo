from dotenv import load_dotenv  # pip install python-dotenv

from langchain_deepseek import ChatDeepSeek
from langchain.agents import create_agent

from langchain.tools import tool

from dataclasses import dataclass

import requests, json

load_dotenv()

model = ChatDeepSeek(
    model="deepseek-chat",
    max_tokens=1000,
)


@dataclass
class Bien:
    type: str
    address: str
    surface: int


@tool
def estimate(bien: Bien):
    """
    Estimate price of real estate
    :param bien: description of real estate with :
        address, type (house/appartment), surface
    :return: estimated price
    """
    return f"estimation de votre {bien.type} : 100000€"

@tool
def geocode(bien:Bien):
    """
    geocode address of real estate
    :param bien:
    :return: array of [lat, lon]
    """
    URL="https://data.geopf.fr/geocodage/search/"
    print(f">geocode {bien=}")
    res = requests.get(URL, params={'q': bien.address, 'limit':2, 'autocomplete':1})
    #print(json.dumps(res.json(), indent=2))
    return res.json().get('features')[0].get('geometry').get('coordinates')

'''
bien = Bien(address="Rue Matabiau, Toulouse", type='house', surface=100)
pos = geocode(bien)
print(f"{pos=}")
'''


agent = create_agent(
    model=model,
    tools=[estimate, geocode],
    system_prompt="You are a helpful assistant",
)

response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "estime le prix et la position de ma maison située"
                " 10 rue Matabiau, face à la gare de Toulouse,"
                " elle fait 100m2",
            }
        ]
    }
)

# print(response)
# print('')

for message in response["messages"]:
    print(message)
