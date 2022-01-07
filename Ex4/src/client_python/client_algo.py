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
        pokemon_id = 0
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
            self.agents[str(pokemon_id)] = pokemon
            pokemon_id += 1

    # Figure out who will take our beloved pokemons
    def allocate_agent_to_pokemon(self, client: Client):
        for pokemon in self.pokemons.values():
            if pokemon.agent_id is None:
                time, chosen_agent_id = self.priority_cal(pokemon)
                pokemon.time = time + client.time_to_end()
                pokemon.agent_id = chosen_agent_id
                # Agent job time increased if the pokemon not in his way:
                if pokemon.time > 0:
                    self.agents.get(str(chosen_agent_id)).free_time = pokemon.time
            # If the time of pickup has passed remove the pokemon & update (next mission)
            elif pokemon.time < client.time_to_end():
                agent: Agent = self.agents.get(str(pokemon.agent_id))
                agent.dest = -1
                agent.missions.pop(0)
                self.pokemons.pop(pokemon.id)
                self.update_agent_task(client, pokemon.agent_id)

    # update all the agent mission list, need to think how frequently
    def update_agent_task(self, client: Client, agent_id: int):
        agent: Agent = self.agents.get(str(agent_id))
        if agent is not None and agent.dest == -1:
            if agent.missions:
                client.choose_next_edge(
                    '{"agent_id":' + str(agent_id) + ', "next_node_id":' + str(agent.missions[0]) + '}')

    def update_all_tasks(self, client: Client):
        for agent_id in self.agents.keys():
            self.update_agent_task(client, agent_id)

    # If an agent is free take the highest priority from the list of pokemon (time/value == priority)
    # when allocated he do not change course unless the new pokemon is in his way!
    # returns tuple(time in which he will be peaked, agent allocated for the job)
    def priority_cal(self, pokemon: Pokemon) -> (float, int):
        for agent in self.agents.values():
            i = 0
            while i < len(agent.path) - 2:
                if pokemon.src == agent.path[i] and pokemon.dest == agent.path[i + 1]:
                    return 0, []
                pass
        return 0, 0

    # Reduce the number of moves!
    def sleep(self):
        pass
