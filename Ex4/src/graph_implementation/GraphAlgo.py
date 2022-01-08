import json
import random
from typing import List

from matplotlib import pyplot as plt

from Ex4.src.graph_implementation.api.GraphAlgoInterface import GraphAlgoInterface
from Ex4.src.graph_implementation.DiGraph import DiGraph
from Ex4.src.graph_implementation.api.GraphInterface import GraphInterface

valid_path = 1
zero_dist = 0
no_path = -1


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, g: DiGraph = DiGraph()):
        self.graph = g

    def get_graph(self) -> GraphInterface:
        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        try:
            self.file = file_name
            self.graph.__init__()
            with open(file_name, 'r') as file:
                l = json.load(file)
                ListNodes = l['Nodes']
                ListEdges = l['Edges']
            for n in ListNodes:
                try:
                    tmp = n['pos'].split(",")
                    x = float(tmp[0])
                    y = float(tmp[1])
                    pos = (x, y, 0.0)
                except Exception:
                    x = random.uniform(35.19, 35.22)
                    y = random.uniform(32.05, 32.22)
                    pos = (x, y, 0.0)

                self.graph.add_node(n['id'], pos)
            for e in ListEdges:
                self.graph.add_edge(e['src'], e['dest'], e['w'])
            return True
        except:
            return False

    def load_from_str(self, json_str: str) -> bool:
        if json_str is None:
            return False
        self.graph = DiGraph()
        graph_dict: dict = json.loads(json_str)
        for node_dict in graph_dict.get("Nodes"):
            self.graph.add_node(node_dict.get("id"), tuple(node_dict.get("pos").split(",")))
        for edge_dict in graph_dict.get("Edges"):
            self.graph.add_edge(edge_dict.get("src"), edge_dict.get("dest"), edge_dict.get("w"))
        if not self.is_connected():
            raise Exception("The graph is not connected! try again\n")

    def save_to_json(self, file_name: str) -> bool:
        data = {"Nodes": [], "Edges": []}
        for node in self.graph.nodes_dict.values():
            if node.flag is False:
                data["Nodes"].append({"id": node.key, "pos": None})
            else:
                data["Nodes"].append({"id": node.key, "pos": node.location})
        for src in self.graph.out_edges.keys():
            for dst in self.graph.out_edges.get(str(src)).keys():
                weight = self.graph.out_edges.get(str(src)).get(str(dst)).weight
                data["Edges"].append({"src": src, "dest": dst, "w": weight})
        try:
            with open(file_name, 'w') as file:
                json.dump(data, indent=2, fp=file)
        except Exception:
            return False
        return True

    def is_connected(self) -> bool:
        if len(self.graph.nodes_dict) == 0 or len(self.graph.nodes_dict) == 1:
            return True
        some_node = 0
        if not self.is_node_connected(self.graph, some_node):
            return False
        reversed_graph = DiGraph()
        reversed_graph.nodes_dict = self.graph.nodes_dict
        for node_key in self.graph.out_edges.keys():
            if node_key is not None:
                for edge in self.graph.out_edges.get(str(node_key)).values():
                    reversed_graph.add_edge(edge.dest, edge.src, edge.weight)
        return self.is_node_connected(reversed_graph, some_node)

    def is_node_connected(self, DWG: DiGraph, key: int) -> bool:
        DWG.dijkstra(key)
        # If one of the nodes tag still holds -1 as his father it means there is no path to it from the src node.
        for node in DWG.nodes_dict.values():
            if node.tag == no_path:
                return False
        return True

    def shortest_path_dist(self, src: int, dst: int) -> float:
        flag = self.graph.dijkstra(src)
        src_node = self.graph.nodes_dict.get(str(src))
        dst_node = self.graph.nodes_dict.get(str(dst))
        if src_node is None or dst_node is None or flag == no_path or dst_node.tag == -1:
            return float('inf')
        if src == dst:
            return 0
        return dst_node.w

    """
        The Idea for this function is also based on the Dijkstra's algorithm.
        Mission -> Return the list of nodes which represent the shortest path from a given src node to the given dest
                    And the path cost(weight).
        Implementation:
        Step 1: Do dijkstra on the src node.
        Step 2: Check if the returned value shows a valid path(using flag).
        Step 3: Go to the dest node tag and start gathering fathers(tag value stores this node father id) to a list.
        Step 4: The list we made is reversed. therefore, reverse it.
        Last, return the list and the dest node w (after the dijkstra its stores the shortest dist from src to it)
        
    """

    def shortest_path(self, id1: int, id2: int) -> (float, list[int]):
        flag = self.graph.dijkstra(id1)
        src_node = self.graph.nodes_dict.get(str(id1))
        dst_node = self.graph.nodes_dict.get(str(id2))
        if src_node is None or dst_node is None or flag == no_path or dst_node.tag == -1:
            return float('inf'), []
        if id1 == id2:
            return 0, [src_node]
        # If we got to the next line it means we have a valid path between id1 to id2
        # The dijkstra works from src to dest and stores in each node in his way a reference to his father(flag val)
        # Therefore, lets gather the information to a valid answer:
        stack = [dst_node]
        current_tag = dst_node.tag
        while current_tag != id1:
            current_node = self.graph.nodes_dict.get(str(current_tag))
            current_tag = current_node.tag
            stack.append(current_node)
        stack.append(src_node)
        # Now, we have a reversed version of the answer. Because we gathered fathers from dest till we saw the src.
        ans_list = []
        while stack:
            ans_list.append(stack.pop().key)
        return dst_node.w, ans_list

    """
        https://www.sanfoundry.com/java-program-implement-traveling-salesman-problem-using-nearest-neighbour-algorithm/
        The Idea for this function is a Greedy algorithm.
        Mission ->  Given a city nodes the function Returns a list of nodes represents the shortest path throw all.
        Implementation -> Same idea as before:
        Step 1: Chose the first node. Add is to the ans array.
        Step 2: Find the closest node in the given city to this node(lets call it CN).
        Step 3: Get the path between them, and add it to the ans array.
        Step 4: Remove the current node from cities and add CN
        Step 5: Loop till there are no more nodes in cities.
        Last, return the ans list.
    """

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        if len(node_lst) == 0:
            return [], 0
        if len(node_lst) == 1:
            return [self.graph.nodes_dict.get(str(node_lst[0])).key], 0
        temp_list = []
        for id in node_lst:
            temp_list.append(id)
        current_node = self.graph.nodes_dict.get(str(temp_list[0]))
        temp_list.remove(temp_list[0])
        ans = [current_node.key]
        total_dist = 0
        while temp_list:
            src = float('-inf')
            dst = float('-inf')
            shortest_dist = float('inf')
            i = 0
            for node_key in temp_list:
                dist = self.shortest_path_dist(current_node.key, node_key)
                if dist < shortest_dist:
                    src = i
                    dst = node_key
                    shortest_dist = dist
                i += 1
            # Now we know who are the current src and dst that has the shortest path between them
            shortest_path = self.shortest_path(current_node.key, dst)[1]
            shortest_path.remove(shortest_path[0])
            # Filling the ans with the list of nodes we got from the shortestPath function.
            ans.extend(shortest_path)
            current_node = self.graph.nodes_dict.get(str(temp_list[src]))
            temp_list.remove(temp_list[src])
            total_dist += shortest_dist
        return ans, total_dist

    """
        Mission -> Find the NodeData which minimizes the max distance to all the other nodes.
        Implementation:
        Step 1: Check if the graph is connected. If not return null.
        Step 2: ForEach node in the graph call dijkstra, And find the max weight value.
        Step 3: If this value is lower than the last canter update, update the center to this value.
        Last, return the center.
    """

    def centerPoint(self) -> (int, float):
        if not self.is_connected():
            return None, float('inf')
        center = None
        best_dist = float('inf')
        for node in self.graph.nodes_dict.values():
            self.graph.dijkstra(node.key)
            temp = float('-inf')
            for node2 in self.graph.nodes_dict.values():
                if node2.w > temp:
                    temp = node2.w
            if temp < best_dist:
                best_dist = temp
                center = node.key
        return center, best_dist

    def plot_graph(self) -> bool:
        X_locations = []
        Y_locations = []
        for node in self.graph.nodes_dict.values():
            X_locations.append(node.location[0])
            Y_locations.append(node.location[1])
        plt.plot(X_locations, Y_locations, 'ro')
        for i in range(len(X_locations)):
            plt.annotate(i, xy=(X_locations[i] * 0.999992, Y_locations[i] * 1.000005))
        for node_id in self.graph.get_all_v().keys():
            if self.graph.out_edges.get(str(node_id)) is not None:
                edge_list = self.get_graph().all_out_edges_of_node(node_id)
                if edge_list is not None:
                    for edge in edge_list.keys():
                        srcX = self.get_graph().get_all_v().get(node_id).location[0]
                        srcY = self.get_graph().get_all_v().get(node_id).location[1]
                        destX = self.get_graph().get_all_v().get(edge).location[0]
                        destY = self.get_graph().get_all_v().get(edge).location[1]

                        plt.annotate("", xy=(srcX, srcY), xytext=(destX, destY),
                                     arrowprops={'arrowstyle': "<-", 'lw': 2})
        plt.show()
        return True


