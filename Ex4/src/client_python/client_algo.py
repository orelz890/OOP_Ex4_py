import json
from Ex4.src.graph_implementation.GraphAlgo import GraphAlgo
from Ex4.src.graph_implementation.DiGraph import DiGraph
from Ex4.src.client_python.agent import Agent
from Ex4.src.client_python.pokemon import Pokemon
from Ex4.src.client_python.client import Client
import time

epsilon = 0.0000001


class Game:
    def __init__(self, graph_str: str):
        self.agents = {}
        self.pokemons = {}
        self.graph_algo: GraphAlgo = GraphAlgo()
        self.graph_algo.load_from_str(graph_str)
        self.sleep_time = []

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
        for agent in self.agents.values():
            if agent.dest == -1:
                pokemon_id = self.priority_cal(agent, client)
                pass

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
    def priority_cal(self, agent: Agent, client: Client) -> int:
        if agent.dest == -1:
            best_priority = 0
            pokemon_id = -1
            for pokemon in self.pokemons.values():
                if pokemon.time < client.time_to_end():
                    self.pokemons.pop(pokemon.id)
                    continue
                if pokemon.id != best_priority:
                    i = 0
                    while i < len(agent.path) - 2:
                        if pokemon.src == agent.path[i] and pokemon.dest == agent.path[i + 1]:
                            return 0
                    dist = self.graph_algo.shortest_path_dist(agent.src, pokemon.src)
                    edge_dist = self.graph_algo.graph.out_edges.get(str(pokemon.src)).get(str(pokemon.dest)).weight
                    priority = (dist + edge_dist) / pokemon.value
                    if priority < best_priority:
                        best_priority = priority
                        pokemon_id = pokemon.id
            return pokemon_id

    # Reduce the number of moves!
    def sleep(self, client: Client):
        best = float('inf')
        for pokemon in self.pokemons.values():
            if pokemon.time < best:
                best = pokemon.time
        if best != float('inf'):
            time_sec = best - client.time_to_end() - epsilon
            time.sleep(time_sec)
