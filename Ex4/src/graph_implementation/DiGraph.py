from Ex4.src.graph_implementation.Node import Node
from Ex4.src.graph_implementation.Edge import Edge
from Ex4.src.graph_implementation.api.GraphInterface import GraphInterface
from Ex4.src.graph_implementation.PQ import PriorityQueue

no_path = -1
valid_path = 1


class DiGraph(GraphInterface):
    nodes_dict = {}
    into_edges = {}
    out_edges = {}
    node_size = 0
    edge_size = 0
    MC = 0

    def __init__(self):
        self.nodes_dict = {}
        self.into_edges = {}
        self.out_edges = {}
        self.node_size = 0
        self.edge_size = 0
        self.MC = 0

    def v_size(self) -> int:
        return self.node_size

    def e_size(self) -> int:
        return self.edge_size

    def get_all_v(self) -> dict:
        """return a dictionary of all the nodes in the Graph, each node is represented using a pair
         (node_id, node_data)
        """
        return self.nodes_dict

    def all_in_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected to (into) node_id ,
        each node is represented using a pair (other_node_id, weight)
         """
        ans = {}
        node = self.nodes_dict.get(str(id1))
        if node is not None:
            for key in self.into_edges.get(str(id1)):
                node_edges = self.into_edges.get(str(key))
                if ans.get(str(key)) is None:
                    ans[str(key)] = {}
                if node_edges is not None:
                    for key2 in node_edges:
                        edge = self.into_edges.get(str(key)).get(str(key2))
                        ans[str(key)] = (edge.src, edge.weight)
        return ans

    def all_out_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected from node_id , each node is represented using a pair
        (other_node_id, weight)
        """
        ans = {}
        node = self.nodes_dict.get(str(id1))
        if node is not None:
            for key in self.out_edges.get(str(id1)).keys():
                node_edges = self.out_edges.get(str(key))
                if ans.get(str(key)) is None:
                    ans[str(key)] = {}
                if node_edges is not None:
                    for key2 in node_edges:
                        edge = self.out_edges.get(str(key)).get(str(key2))
                        ans[str(key)] = (edge.src, edge.weight)
        return ans

    def get_mc(self) -> int:
        return self.MC

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        src = self.nodes_dict.get(str(id1))
        dest = self.nodes_dict.get(str(id2))
        if src is None or dest is None:
            return False
        new_edge = Edge(id1, id2, weight)
        edges_into = self.into_edges.get(str(id2))
        edges_out = self.out_edges.get(str(id1))
        if edges_out is not None and edges_into is not None:
            if edges_out.get(str(id2)) is not None:
                return False
        else:
            if edges_into is None:
                self.into_edges[str(id2)] = {}
            if edges_out is None:
                self.out_edges[str(id1)] = {}
        self.into_edges[str(id2)][str(id1)] = new_edge
        self.out_edges[str(id1)][str(id2)] = new_edge
        self.nodes_dict.get(str(id1)).weight += 1
        self.edge_size += 1
        src.weight += 1
        self.MC += 1
        return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        node = self.nodes_dict.get(str(node_id))
        if node is not None:
            return False
        self.nodes_dict[str(node_id)] = Node(node_id, pos)
        self.node_size += 1
        self.MC += 1
        return True

    def remove_node(self, node_id: int) -> bool:
        node = self.nodes_dict.get(str(node_id))
        if node is None:
            return False
        s = str(node_id)
        self.nodes_dict.pop(s)
        self.node_size -= 1

        edge1 = self.out_edges.get(s)
        if edge1 is not None:
            e = self.out_edges.pop(s)
            self.edge_size -= len(e)
        edge2 = self.into_edges.get(s)
        if edge2 is not None:
            e = self.into_edges.pop(s)
            self.edge_size -= len(e)
        for key in self.out_edges:
            self.remove_edge(key, node_id)

        self.MC += 1
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:

        s1 = str(node_id1)
        s2 = str(node_id2)
        node1 = self.nodes_dict.get(s1)
        node2 = self.nodes_dict.get(s2)
        edge = self.out_edges.get(s1).get(s2)
        if node1 is None or node2 is None or edge is None:
            return False
        self.out_edges[s1].pop(s2)
        self.into_edges[s2].pop(s1)
        self.edge_size -= 1
        node1.weight -= 1
        self.MC += 1
        return True

    """
        Site which explains about Dijkstra's algorithm: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm .
        Mission -> set all tags and w of all the nodes. The tag will store this node father id, in the shortest path
                    from src to dest. And w will store the shortest path distance(weight).
        Implementation:
        Step 1: Set all weight to infinity, tags to -1, and the src node weight to 0.
        Step 2: Creat a priority queue and add the src node to it.
        Step 3: While the queue is not empty pull an element.
        Step 4: Go throw all its edges to its neighbors, and check if the current neighbor weight >
                new val (element weight + the edge between them).
                If do, update it to the new val, the tag to element key(his father), and add the neighbor to the queue.
    """

    def dijkstra(self, src: int):
        if self.nodes_dict.get(str(src)) is None:
            return no_path
        priority_q = PriorityQueue()
        for node in self.nodes_dict.values():
            if node.key == src:
                node.w = 0
                node.tag = src
            else:
                node.w = float('inf')
                node.tag = -1
            priority_q.insert(node)
        while not priority_q.isEmpty():
            temp_node = priority_q.delete()
            if self.out_edges.get(str(temp_node.key)) is not None:
                for edge in self.out_edges.get(str(temp_node.key)).values():
                    new_weight = temp_node.w + edge.weight
                    if new_weight < self.nodes_dict.get(str(edge.dest)).w:
                        self.nodes_dict.get(str(edge.dest)).w = new_weight
                        self.nodes_dict.get(str(edge.dest)).tag = temp_node.key
        return valid_path

    def set_all_tags(self, w_val: float, tag_val: int):
        for node in self.nodes_dict.values():
            node.w = w_val
            node.tag = tag_val
            node.info = "White"

    def __str__(self):
        s = "Graph: |V|=" + str(self.v_size()) + ", |E|=" + str(self.e_size())
        return s
