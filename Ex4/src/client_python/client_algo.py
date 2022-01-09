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

    def load_game_data(self, pokemons_str: str, agents_str: str, graph_str):

        if agents_str is not None:
            agents_dict: dict = json.loads(agents_str)
            for agent_d in agents_dict.get("Agents"):
                data: dict = agent_d.get("Agent")
                self.agents[str(data.get("id"))] = Agent().load_agent(data)

        if pokemons_str is not None:
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
        # For the gui
        if graph_str is not None:
            self.graph_algo.load_from_str(graph_str)

    # update all the agent mission list, need to think how frequently
    def update_all_tasks(self, client: Client):
        for agent_id in self.agents.keys():
            self.update_agent_task(client, agent_id)

    # Updates the agent next step
    def update_agent_task(self, client: Client, agent_id: int):
        agent: Agent = self.agents.get(str(agent_id))
        if agent is not None and agent.dest != -1:
            if agent.path:
                client.choose_next_edge(
                    '{"agent_id":' + str(agent_id) + ', "next_node_id":' + str(agent.path[0]) + '}')
                agent.path.pop(0)
                # node_id = agent.path.pop(0)
                # agent.pos = self.graph_algo.graph.nodes_dict.get(str(node_id)).pos

            else:
                agent.dest = -1

    # Figure out who will take our beloved pokemons
    def allocate_agent_to_pokemon(self, client: Client) -> None:
        agent_id, pokemon_id, job_time = self.priority_cal(client)
        if agent_id == -1 or pokemon_id == -1:
            return
        agent: Agent = self.agents.get(str(agent_id))
        pokemon: Pokemon = self.pokemons.get(str(pokemon_id))
        shortest_path = self.graph_algo.shortest_path(agent.src, pokemon.src)
        pokemon.agent_id = agent_id
        pokemon.time = client.time_to_end() - job_time
        # If not already on his way
        if job_time != 0:
            agent.path.append(shortest_path[1])
            agent.path.append(pokemon.dest)

    """
        Finds the fastest agent available & allocate the pokemon with the highest priority to him 
        (time/value == priority).
        When allocated, he will not change course for any one!
        Last, returns tuple(agent id, pokemon id , time in which he will be peaked)
    """

    def priority_cal(self, client: Client) -> (int, int, int):
        if not self.pokemons:
            return -1, -1, -1
        # Finding the fastest agent available.
        agent_id = -1
        for agent in self.agents.values():
            if agent.dest == -1:
                if agent_id == -1 or agent.speed > self.agents.get(str(agent_id)).speed:
                    agent_id = agent.id
        # If True all agents are busy
        if agent_id == -1:
            return -1, -1, -1
        # Finding the the best pokemon to catch for this agent.
        agent: Agent = self.agents.get(str(agent_id))
        best_priority = float('inf')
        pokemon_id = -1
        distance = float('inf')
        for pokemon in self.pokemons.values():
            if pokemon.time > client.time_to_end():
                self.pokemons.pop(pokemon.id)
                continue
            # Check if the pokemon already been assigned.
            if pokemon.agent_id == -1:
                i = 0
                # Checking if the pokemon on the way.
                while i < len(agent.path) - 2:
                    if pokemon.src == agent.path[i] and pokemon.dest == agent.path[i + 1]:
                        return agent_id, pokemon_id, 0
                    i += 1
                # Not on the way
                dist = self.graph_algo.shortest_path_dist(agent.src, pokemon.src)
                # edge_dist = self.graph_algo.graph.out_edges.get(str(pokemon.src)).get(str(pokemon.dest)).weight
                priority = dist / pokemon.value
                if priority < best_priority:
                    best_priority = priority
                    pokemon_id = pokemon.id
                    distance = dist
        job_time = distance / agent.speed
        # If, we got a valid answer return it. Else, return error flag.
        if pokemon_id == -1 and distance != float('inf'):
            return agent_id, pokemon_id, job_time
        return -1, -1, -1

    def add_pokemon(self, pokemon: Pokemon, client: Client) -> None:
        # Checking if the pokemon on some agent way.
        for agent in self.agents.values():
            i = 0
            while i < len(agent.path) - 2:
                # If do:
                if pokemon.src == agent.path[i] and pokemon.dest == agent.path[i + 1]:
                    shortest_path = self.graph_algo.shortest_path(agent.src, pokemon.src)
                    pokemon.time = client.time_to_end() - shortest_path[0]
                    agent.path.append(shortest_path[1])
                    agent.path.append(pokemon.dest)
                    break
                i += 1
        self.pokemons[str(pokemon.id)] = pokemon

    # Reduce the number of moves!
    def sleep(self, client: Client):
        # Finding the closest pokemon peak up (time wise).
        closest_time = float('inf')
        for pokemon in self.pokemons.values():
            if pokemon.time > closest_time:
                closest_time = pokemon.time
        # If we got a valid value, sleep till we get there.
        if closest_time != float('inf'):
            time_sec = client.time_to_end() - closest_time - 0.02
            time.sleep(time_sec)


if __name__ == '__main__':
    print(0)
