import json
from Ex4.src.graph_implementation.GraphAlgo import GraphAlgo
from Ex4.src.graph_implementation.Node import Node
from Ex4.src.client_python.agent import Agent
from Ex4.src.client_python.pokemon import Pokemon
from Ex4.src.client_python.client import Client
import time

epsilon = 0.0000001


class Game:
    def __init__(self, client: Client):
        self.client = client
        self.agents = {}
        self.pokemons = {}
        self.graph_algo: GraphAlgo = GraphAlgo()

    def load_game_data(self, agents_str=None, pokemons_str=None, graph_str=None):
        # For the gui
        if graph_str is not None:
            self.graph_algo.load_from_str(graph_str)

        if agents_str is not None:
            agents_dict = json.loads(agents_str)
            for agent_d in agents_dict.get('Agents'):
                data: dict = agent_d.get('Agent')
                agent = self.agents.get(str(data.get('id')))
                agent.load_agent(data)
                self.agents[str(agent.id)] = agent

        if pokemons_str is not None:
            pokemons_dict: dict = json.loads(pokemons_str)
            # Add the pokemons:
            pokemon_id = 0
            for pokemon_d in pokemons_dict.get("Pokemons"):
                data: dict = pokemon_d.get("Pokemon")
                pokemon: Pokemon = Pokemon()
                pokemon.load_pokemon(data)
                # Finds on which edge the pokemon stands:
                for val in self.graph_algo.graph.out_edges.values():
                    for edge in val.values():
                        src: Node = self.graph_algo.graph.nodes_dict.get(str(edge.src))
                        dst: Node = self.graph_algo.graph.nodes_dict.get(str(edge.dest))
                        edge_dist = src.distance(dst.location)
                        pokemon_dist = src.distance(pokemon.pos) + dst.distance(pokemon.pos)
                        # If True it means the pokemon is on the current edge or the opposite edge:
                        # note: The pokemon type cant be zero (assumption).
                        if abs(edge_dist - pokemon_dist) < epsilon:
                            maxi = max(edge.src, edge.dest)
                            mini = min(edge.src, edge.dest)
                            # if pokemon.type < 0:
                            #     pokemon.src = mini
                            #     pokemon.dest = maxi
                            # if pokemon.type > 0:
                            #     pokemon.src = maxi
                            #     pokemon.dest = mini
                            if pokemon.type < 0:
                                pokemon.src = maxi
                                pokemon.dest = mini
                            if pokemon.type > 0:
                                pokemon.src = mini
                                pokemon.dest = maxi
                            if pokemon.type == 0:
                                pokemon.src = mini
                                pokemon.dest = mini
                self.pokemons[str(pokemon_id)] = pokemon
                pokemon_id += 1

    # Updates the agent next step
    def update_agent_task(self, agent: Agent, dest):
        if agent is not None:
            self.client.choose_next_edge('{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(dest) + '}')

    # update all the agent mission list, need to think how frequently
    def allocate_all(self):
        for agent in self.agents.values():
            if agent.dest == -1:
                self.priority_allocation(agent)

    """
        Given an agent, allocate the pokemon with the highest priority to him 
        (dist/value == priority).
        When allocated, he will not change course for any one!
        Last, returns tuple(agent id, pokemon id , time in which he will be peaked)
    """

    def priority_allocation(self, agent: Agent) -> None:
        prioritized = float("inf")
        next_move: int = -1
        pokemon_ans = None
        for pokemon in self.pokemons.values():
            if pokemon.agent_id == -1:
                shortest_path = self.graph_algo.shortest_path(agent.src, pokemon.src)
                priority = shortest_path[0] / agent.speed
                if priority < prioritized:
                    pokemon_ans = pokemon
                    prioritized = priority
                    if prioritized != 0:
                        next_move = shortest_path[1][1]
                    else:
                        next_move = pokemon.dest
        if pokemon_ans != None:
            # if agent.src == pokemon_ans.src:
            #     self.client.move()
            if pokemon_ans.agent_id == -1:
                pokemon_ans.agent_id = agent.id
            self.update_agent_task(agent, next_move)
