import json
from Ex4.src.graph_implementation.GraphAlgo import GraphAlgo
import agent
import client
epsilon = 0.0000001

class game:
    def __init__(self):
        self.agents = {}
        self.pokemon_dist = {}
        self.graph_algo = GraphAlgo()

    # def  load_game_data(self, pokemons: str, agents: str):
    #     agents_dict: dict = json.loads(agents)
    #     for agent in agents_dict.get()


