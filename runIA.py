from dotenv import load_dotenv  # pip install python-dotenv

from langchain_deepseek import ChatDeepSeek
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from langchain.tools import tool, ToolRuntime
from typing import Callable

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

@dataclass
class UserContext:
    name: str


@tool
def estimate(bien: Bien,
             runtime: ToolRuntime[UserContext]):
    """
    Estimate price of real estate
    :param bien: description of real estate with :
        address, type (house/appartment), surface
    :return: estimated price
    """
    print(f">estimate {bien=}, {runtime.context}")
    return f"estimation de votre {bien.type} : 100000€"

@tool
def geocode(bien:Bien,
            runtime: ToolRuntime[UserContext]):
    """
    geocode address of real estate
    :param bien:
    :return: array of [lat, lon]
    """
    URL="https://data.geopf.fr/geocodage/search/"
    print(f">geocode {bien=}, {runtime.context}")
    res = requests.get(URL, params={'q': bien.address, 'limit':2, 'autocomplete':1})
    #print(json.dumps(res.json(), indent=2))
    return res.json().get('features')[0].get('geometry').get('coordinates')

'''
bien = Bien(address="Rue Matabiau, Toulouse", type='house', surface=100)
pos = geocode(bien)
print(f"{pos=}")
'''

@wrap_model_call
def context_based_tools(
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    '''
    Middleware qui intercepte les appel LLM ou outils
    '''
    print(f">context_based_tools, {request.runtime.context}")
    #print(f"tools {request}, {request.tools}")

    # Si User autre que 'Goudot', remplace la liste des outils par liste réduite (1 outil)
    if request.runtime.context.name != "Goudot":
        print('  MaJ liste outils')
        request = request.override(tools=request.tools[:1])

    # Affichage des outils
    for tool in request.tools:
        print(f"  >{tool.name}")

    # Invocation de la séquence
    res = handler(request)
    return res

agent = create_agent(
    model=model,
    tools=[estimate, geocode],
    system_prompt="You are a helpful assistant",
    context_schema= UserContext,
    middleware=[context_based_tools],
)

context = UserContext(name='xxxx')

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
    },
    context = context
)

for message in response["messages"]:
    print(message)
