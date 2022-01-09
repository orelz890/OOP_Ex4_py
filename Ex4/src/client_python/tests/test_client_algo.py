# import subprocess
# from unittest import TestCase
# import sys
# import json
# from Ex4.src.client_python.client_algo import Game
# from Ex4.src.client_python.agent import Agent
# from Ex4.src.client_python.client import Client
#
# # default port
# PORT = 6666
# HOST = '127.0.0.1'
# """sys.argv[1]"""
# subprocess.Popen(['powershell.exe', f'java -jar ../../../Ex4_Server_v0.0.jar {0}'])
# client = Client()
# client.start_connection(HOST, PORT)
#
# game = Game()
# size = int(json.loads(client.get_info())["GameServer"]["agents"])
# for i in range(size):
#     client.add_agent("{\"id\":" + str(i) + "}")
#     game.agents[str(i)] = Agent(id=i)
# game.load_game_data(agents_str=client.get_agents(), pokemons_str=client.get_pokemons(),
#                     graph_str=client.get_graph())
# client.start()
#
# class TestGame(TestCase):
#
#     def test_load_game_data(self):
#         agents_str = client.get_agents()
#         agents_dict: dict = json.loads(agents_str)
#         pokemons_str = client.get_pokemons()
#         pokemons_dict: dict = json.loads(agents_str)
#         graph_str = client.get_graph()
#         graph_dict: dict = json.loads(agents_str)
#         game.load_game_data(agents_str=agents_str, pokemons_str=pokemons_str, graph_str=graph_str)
#         for node in graph_dict.get('Nodes'):
#             self.assertEqual(node.get('id'), game.graph_algo.graph.nodes_dict.get(str(node.get('id'))))
#
#     def test_update_all_tasks(self):
#         self.fail()
#
#     def test_update_agent_task(self):
#         self.fail()
#
#     def test_allocate_agent_to_pokemon(self):
#         self.fail()
#
#     def test_priority_cal(self):
#         self.fail()
#
#     def test_add_pokemon(self):
#         self.fail()
#
#     def test_sleep(self):
#         self.fail()
