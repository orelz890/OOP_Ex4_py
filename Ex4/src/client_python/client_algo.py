import json
import math

from Ex4.src.graph_implementation.GraphAlgo import GraphAlgo
from Ex4.src.graph_implementation.DiGraph import DiGraph
from Ex4.src.client_python.agent import Agent
from Ex4.src.client_python.pokemon import Pokemon
from Ex4.src.client_python.client import Client

import agent
import client

epsilon = 0.0000001


class Game:
    def __init__(self, graph_str: str):
        self.agents = {}
        self.pokemons = {}
        self.graph_algo: GraphAlgo = GraphAlgo()
        self.graph_algo.load_from_str(graph_str)

    def load_game_data(self, pokemons_str: str, agents_str: str):

        if agents_str is None or pokemons_str is None:
            return None
        agents_dict: dict = json.loads(agents_str)
        for agent_d in agents_dict.get("Agents"):
            data: dict = agent_d.get("Agent")
            self.agents[str(data.get("id"))] = Agent().load_agent(data)

        pokemons_dict: dict = json.loads(pokemons_str)
        # Add the pokemons:
        graph: DiGraph = self.graph_algo.graph
        for pokemon_d in pokemons_dict.get("Pokemons"):
            data: dict = pokemon_d.get("Pokemon")
            pokemon: Pokemon = Pokemon().load_pokemon(data)
            # Finds on which edge the pokemon stands:
            for edge in graph.out_edges:
                src = graph.nodes_dict.get(str(edge.src))
                dst = graph.nodes_dict.get(str(edge.dest))
                edge_dist = src.distance(dst)
                pokemon_dist = src.distance(pokemon.pos) + dst.distance(pokemon.pos)
                # If True it means the pokemon is on the current edge or the opposite edge:
                # note: The pokemon type cant be zero (assumption).
                if abs(edge_dist - pokemon_dist) < epsilon:
                    maxi = max(edge.src, edge.dest)
                    mini = min(edge.src, edge.dest)
                    if pokemon.type < 0:
                        pokemon.src = mini
                        pokemon.dest = maxi
                    if pokemon.type > 0:
                        pokemon.src = maxi
                        pokemon.dest = mini
            self.agents[str(data.get("id"))] = pokemon

    # Figure out who will take our beloved pokemons
    def allocate_agents_to_pokemons(self):
        for pokemon in self.pokemons:
            if pokemon.agent is None:
                pass

    # update all the agent mission list, need to think how frequently
    def update_agents_tasks(self, client: Client):
        pass

    # By dist & value!!!
    def priority_cal(self):
        pass

    # Reduce the number of moves!
    def sleep(self):
        pass