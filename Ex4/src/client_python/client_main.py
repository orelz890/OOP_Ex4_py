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
    game.load_game_data(agents_str=None, pokemons_str=client.get_pokemons(),
                        graph_str=client.get_graph())
    size = int(json.loads(client.get_info())["GameServer"]["agents"])
    pokemon_info = json.loads(client.get_pokemons())
    pokemon_d = pokemon_info.get("Pokemons")
    for i in range(size):
        ag_str = "{}\"id\":{}{}".format('{', game.pokemons.get(str(i)).src, '}')
        client.add_agent(ag_str)
        game.agents[str(i)] = Agent(id=i, value=0.0, src=-1, dest=-1, speed=1.0, pos="0.0,0.0,0.0")
        i += 1
    game.load_game_data(agents_str=client.get_agents(), pokemons_str=client.get_pokemons(),
                        graph_str=client.get_graph())
    gui = GUIT(client)
    client.start()

    while client.is_running() == 'true':
        game.load_game_data(pokemons_str=client.get_pokemons(), agents_str=client.get_agents())
        # Finding the fastest agent available.
        game.allocate_all()
        gui.draw()
        # print(client.get_info())
        time.sleep(0.078)
        client.move()
        time.sleep(0.012)




    client.stop_connection()
    # print(client.get_info())
