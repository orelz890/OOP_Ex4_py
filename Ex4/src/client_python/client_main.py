import json
import subprocess
import sys
from Ex4.src.client_python.client_algo import Game
from Ex4.src.client_python.agent import Agent
from client import Client

# default port
PORT = 6666
HOST = '127.0.0.1'

if __name__ == '__main__':
    client = Client()
    client.start_connection(HOST, PORT)

    game = Game()
    size = int(json.loads(client.get_info())["GameServer"]["agents"])
    for i in range(size):
        client.add_agent("{\"id\":" + str(i) + "}")
        game.agents[str(i)] = Agent(id=i)
    game.load_game_data(agents_str=client.get_agents(), pokemons_str=client.get_pokemons(), graph_str=client.get_graph())
    client.start()

    while client.is_running() == 'true':
        game.load_game_data(pokemons_str=client.get_pokemons(), agents_str=client.get_agents())
        # Finding the fastest agent available.
        for agent in game.agents.values():
            game.allocate_agent_to_pokemon(client, agent.id)
        game.update_all_tasks(client)
            # print(client.get_info())
        game.sleep(client)
        client.move()
        print(client.get_info())