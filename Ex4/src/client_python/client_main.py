import json
import subprocess
import sys
# from Ex4.src.client_python.client_algo import Game
import time

from Ex4.src.GUIT import GUIT
from Ex4.src.client_python.client_algo import Game
from Ex4.src.client_python.agent import Agent
from Ex4.src.client_python.client import Client

# default port
PORT = 6666
HOST = '127.0.0.1'

if __name__ == '__main__':
    client = Client()
    client.start_connection(HOST, PORT)

    game = Game(client)
    size = int(json.loads(client.get_info())["GameServer"]["agents"])
    for i in range(size):
        client.add_agent("{\"id\":" + str(i) + "}")
    #
        game.agents[str(i)] = Agent(id=i, value=0.0, src=-1, dest=-1, speed=1.0, pos="0.0,0.0,0.0")
    game.load_game_data(agents_str=client.get_agents(), pokemons_str=client.get_pokemons(),
                        graph_str=client.get_graph())
    gui = GUIT(client)
    client.start()

    while client.is_running() == 'true':
        game.load_game_data(pokemons_str=client.get_pokemons(), agents_str=client.get_agents())
        # Finding the fastest agent available.
        game.allocate_all()
        client.move()
        gui.draw()
        print(client.get_info())
        time.sleep(0.1)
    client.stop_connection()
    # print(client.get_info())
