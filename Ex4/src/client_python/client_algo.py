import json
from Ex4.src.graph_implementation.GraphAlgo import GraphAlgo
from Ex4.src.graph_implementation.Node import Node
from Ex4.src.client_python.agent import Agent
from Ex4.src.client_python.pokemon import Pokemon
from Ex4.src.client_python.client import Client
import time

epsilon = 0.0000001


class Game:
    def __init__(self):
        self.agents = {}
        self.pokemons = {}
        self.graph_algo: GraphAlgo = GraphAlgo()
        self.sleep_time = []

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
                            if pokemon.type < 0:
                                pokemon.src = mini
                                pokemon.dest = maxi
                            if pokemon.type > 0:
                                pokemon.src = maxi
                                pokemon.dest = mini
                self.pokemons[str(pokemon_id)] = pokemon
                pokemon_id += 1

    # update all the agent mission list, need to think how frequently
    def update_all_tasks(self, client: Client):
        for agent_id in self.agents.keys():
            self.update_agent_task(client, agent_id)

    # Updates the agent next step
    def update_agent_task(self, client: Client, agent_id: int):
        agent: Agent = self.agents.get(str(agent_id))
        if agent is not None and agent.dest != -1:
            if agent.path:
                # print(agent.path)
                poped = agent.path.pop(0)
                # print(agent.path)
                # print(poped)
                client.choose_next_edge(
                    '{"agent_id":' + str(agent_id) + ', "next_node_id":' + str(poped) + '}')
                # node_id = agent.path.pop(0)
                # agent.pos = self.graph_algo.graph.nodes_dict.get(str(node_id)).pos
            else:
                agent.dest = -1

    # Figure out who will take our beloved pokemons
    def allocate_agent_to_pokemon(self, client: Client, agent_id) -> None:
        agent, pokemon, job_time = self.priority_cal(agent_id)
        if agent is None or pokemon is None:
            return
        shortest_path = self.graph_algo.shortest_path(agent.src, pokemon.src)
        pokemon.time = float(client.time_to_end()) / 1000 - job_time
        # If not already on his way
        if job_time > 0 and agent.dest == -1:
            for node in shortest_path[1]:
                agent.path.append(node)
            agent.path.append(pokemon.dest)
            agent.dest = pokemon.dest

    """
        Finds the fastest agent available & allocate the pokemon with the highest priority to him 
        (time/value == priority).
        When allocated, he will not change course for any one!
        Last, returns tuple(agent id, pokemon id , time in which he will be peaked)
    """

    def priority_cal(self, agent_id) -> (int, int, int):
        if not self.pokemons:
            return None, None, -1
        # Finding the the best pokemon to catch for this agent.
        agent: Agent = self.agents.get(str(agent_id))
        best_priority = float('inf')
        pokemon_ans = None
        distance = float('inf')
        for pokemon in self.pokemons.values():
            # if pokemon.time > client.time_to_end():
            #     self.pokemons.pop(pokemon.id)
            #     continue

            # Check if the pokemon already been assigned.
            if pokemon.agent_id == -1:
                i = 0
                # Checking if the pokemon on the way.
                while i < len(agent.path) - 2:
                    if pokemon.src == agent.path[i] and pokemon.dest == agent.path[i + 1]:
                        return agent, pokemon, 0
                    i += 1
                # Not on the way
                dist = self.graph_algo.shortest_path_dist(agent.src, pokemon.src)
                # edge_dist = self.graph_algo.graph.out_edges.get(str(pokemon.src)).get(str(pokemon.dest)).weight
                priority = dist / pokemon.value
                if priority < best_priority:
                    best_priority = priority
                    pokemon_ans = pokemon
                    distance = dist
        job_time = distance / agent.speed
        # If, we got a valid answer return it. Else, return error flag.
        if pokemon_ans is not None and distance != float('inf'):
            return agent, pokemon_ans, job_time
        return None, None, -1

    # def add_pokemon(self, pokemon: Pokemon, client: Client) -> None:
    #     # Checking if the pokemon on some agent way.
    #     for agent in self.agents.values():
    #         i = 0
    #         while i < len(agent.path) - 2:
    #             # If do:
    #             if pokemon.src == agent.path[i] and pokemon.dest == agent.path[i + 1]:
    #                 shortest_path = self.graph_algo.shortest_path(agent.src, pokemon.src)
    #                 pokemon.time = client.time_to_end() - shortest_path[0]
    #                 agent.path.append(shortest_path[1])
    #                 agent.path.append(pokemon.dest)
    #                 break
    #             i += 1
    #     self.pokemons[str(pokemon.id)] = pokemon

    # Reduce the number of moves!
    def sleep(self, client: Client):
        # Finding the closest pokemon peak up (time wise).
        closest_time = float('inf')
        for pokemon in self.pokemons.values():
            if pokemon.time > closest_time:
                closest_time = pokemon.time
        # If we got a valid value, sleep till we get there.
        if closest_time != float('inf'):
            time_sec = float(client.time_to_end()) / 1000 - closest_time - 0.02
            time.sleep(time_sec)

