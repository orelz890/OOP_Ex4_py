import json
from Ex4.src.graph_implementation.GraphAlgo import GraphAlgo
from Ex4.src.client_python.agent import Agent
from Ex4.src.client_python.pokemon import Pokemon
import agent
import client

epsilon = 0.0000001


class game:
    def __init__(self, graph_str: str):
        self.agents = {}
        self.pokemons = {}
        self.graph_algo = GraphAlgo().load_from_str(graph_str)

    def load_game_data(self, pokemons_str: str, agents_str: str):
        if agents_str is None or pokemons_str is None:
            return None
        agents_dict: dict = json.loads(agents_str)
        for agent_d in agents_dict.get("Agents"):
            data: dict = agent_d.get("Agent")
            self.agents[str(data.get("id"))] = Agent().load_agent(data)

        pokemons_dict: dict = json.loads(pokemons_str)
        for pokemon_d in pokemons_dict.get("Pokemons"):
            data: dict = pokemon_d.get("Pokemon")
            self.agents[str(data.get("id"))] = Pokemon().load_pokemon(data)

