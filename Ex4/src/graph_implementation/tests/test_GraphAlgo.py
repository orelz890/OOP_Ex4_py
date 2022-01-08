import unittest

from Ex4.src.graph_implementation.Edge import Edge
from Ex4.src.graph_implementation.Node import Node
from Ex4.src.graph_implementation.api import GraphInterface
from Ex4.src.graph_implementation.GraphAlgo import GraphAlgo


class test_GraphAlgo(unittest.TestCase):
    g: GraphAlgo = GraphAlgo()
    empty: GraphAlgo = GraphAlgo()

    p1 = (35.19589389346247, 32.10152879327731, 0.0)
    p2 = (35.20319591121872, 32.10318254621849, 0.0)
    p3 = (35.20752617756255, 32.1025646605042, 0.0)
    p4 = (35.21007339305892, 32.10107446554622, 0.0)
    p5 = (35.21310882485876, 32.104636394957986, 0.0)

    a = Node(0, p1)
    b = Node(1, p2)
    c = Node(2, p3)
    d = Node(3, p4)
    e = Node(4, p5)
    nodes = [a, b, c, d, e]

    e1 = Edge(0, 4, 1.3)
    e2 = Edge(1, 0, 1.2)
    e3 = Edge(1, 4, 1.8)
    e4 = Edge(2, 1, 1.7)
    e5 = Edge(3, 2, 1.5)
    e6 = Edge(3, 0, 1)
    e7 = Edge(4, 2, 4)
    e8 = Edge(4, 3, 1.4)
    edge = [e1, e2, e3, e4, e5, e6, e7, e8]

    def setUp(self) -> None:
        self.empty = GraphAlgo()

        self.empty.graph.add_node(self.a.key, self.a.location)
        self.empty.graph.add_node(self.b.key, self.b.location)
        self.empty.graph.add_node(self.c.key, self.c.location)
        self.empty.graph.add_node(self.d.key, self.d.location)
        self.empty.graph.add_node(self.e.key, self.e.location)

        self.empty.graph.add_edge(self.e1.src, self.e1.dest, self.e1.weight)
        self.empty.graph.add_edge(self.e2.src, self.e2.dest, self.e2.weight)
        self.empty.graph.add_edge(self.e3.src, self.e3.dest, self.e3.weight)
        self.empty.graph.add_edge(self.e4.src, self.e4.dest, self.e4.weight)
        self.empty.graph.add_edge(self.e5.src, self.e5.dest, self.e5.weight)
        self.empty.graph.add_edge(self.e6.src, self.e6.dest, self.e6.weight)
        self.empty.graph.add_edge(self.e7.src, self.e7.dest, self.e7.weight)
        self.empty.graph.add_edge(self.e8.src, self.e8.dest, self.e8.weight)

        self.g.load_from_json("../graph_data/A0.json")

    def test_get_graph(self):
        dg = self.g.get_graph()
        self.assertTrue(self.isTheSame(dg))

    def test_load_from_json(self):
        self.assertEqual(11, self.g.graph.node_size)
        self.assertEqual(22, self.g.graph.edge_size)
        self.g.save_to_json("file")
        ga = GraphAlgo()
        ga.load_from_json("file")
        self.assertTrue(self.isTheSame(ga.graph))

    def test_save_to_json(self):
        try:
            ans = self.g.save_to_json("file.json")
            self.assertTrue(ans)

        except Exception:
            print(Exception)

    def test_is_connected(self):
        self.g.load_from_json("../graph_data/CompleteG.json")
        self.assertTrue(self.g.is_connected())
        self.g.load_from_json("../graph_data/MyG.json")
        self.assertTrue(self.g.is_connected())
        self.g.load_from_json("../graph_data/G1.json")
        self.assertTrue(self.g.is_connected())
        self.g.load_from_json("../graph_data/G2.json")
        self.assertTrue(self.g.is_connected())
        self.g.load_from_json("../graph_data/G3.json")
        self.assertTrue(self.g.is_connected())
        self.g.load_from_json("../graph_data/1000Nodes.json")
        self.assertTrue(self.g.is_connected())
        # 1 is not connected
        self.g.load_from_json("../graph_data/NotConnectedG.json")
        self.assertFalse(self.g.is_connected())
        # 47 is not connected
        self.g.load_from_json("../graph_data/NotConnectedG2.json")
        self.assertFalse(self.g.is_connected())

    def test_shortest_path(self):
        self.g.load_from_json("../graph_data/NotConnectedG.json")
        ans = [3, 0]
        self.assertEqual(1, self.g.shortest_path(3, 0)[0])
        self.assertEqual(ans, self.g.shortest_path(3, 0)[1])
        # Not a Direct connection:
        # 2->0->4
        ans = [2, 0, 4]
        self.assertEqual(3.0, self.g.shortest_path(2, 4)[0])
        self.assertEqual(ans, self.g.shortest_path(2, 4)[1])
        # 2->0->4->3
        ans.append(3)
        self.assertEqual(4.4, self.g.shortest_path(2, 3)[0])
        self.assertEqual(ans, self.g.shortest_path(2, 3)[1])
        # 0->4->3->2
        ans = [0, 4, 3, 2]
        self.assertEqual(4.2, self.g.shortest_path(0, 2)[0])
        self.assertEqual(ans, self.g.shortest_path(0, 2)[1])
        # Path not exist
        self.assertEqual(float('inf'), self.g.shortest_path(2, 1)[0])
        self.assertEqual([], self.g.shortest_path(2, 1)[1])
        # Input node do not exist
        self.assertEqual(float('inf'), self.g.shortest_path(2, -1)[0])
        self.assertEqual([], self.g.shortest_path(2, -1)[1])

    def test_tsp(self):
        global i
        self.g.load_from_json("../graph_data/G1.json")
        cities = [0, 1, 2, 3]
        i = 0
        ans = self.g.TSP(cities)[0]
        while i < len(ans):
            self.assertEqual(cities[i], ans[i])
            i += 1
        self.assertEqual(4.096793421922225, self.g.TSP(cities)[1])

        # One node case
        cities1 = [0]
        i = 0
        ans = self.g.TSP(cities1)[0]
        while i < len(ans):
            self.assertEqual(cities1[i], ans[i])
            i += 1
        self.assertEqual(0, self.g.TSP(cities1)[1])

        cities2 = []
        for n in self.g.graph.nodes_dict.values():
            cities2.append(n.key)
        i = 0
        ans = self.g.TSP(cities2)[0]
        while i < len(ans):
            self.assertEqual(cities2[i], ans[i])
            i += 1
        self.assertEqual(22.63446693792369, self.g.TSP(cities2)[1])

        cities3 = []
        self.g.load_from_json("../graph_data/MyG.json")
        for n in self.g.graph.nodes_dict.values():
            cities3.append(n.key)
        expected = [0, 4, 3, 2, 1]
        actual = self.g.TSP(cities3)[0]
        i = 0
        while i < len(actual):
            self.assertEqual(expected[i], actual[i])
            i += 1
        self.assertEqual(5.9, self.g.TSP(cities3)[1])

    def test_center_point(self):
        self.g.load_from_json("../graph_data/G1.json")
        self.assertEqual(self.g.graph.nodes_dict.get(str(8)).key, self.g.centerPoint()[0])
        self.assertEqual(9.925289024973141, self.g.centerPoint()[1])

        self.g.load_from_json("../graph_data/G2.json")
        self.assertEqual(self.g.graph.nodes_dict.get(str(0)).key, self.g.centerPoint()[0])
        self.assertEqual(7.819910602212574, self.g.centerPoint()[1])

        self.g.load_from_json("../graph_data/G3.json")
        self.assertEqual(self.g.graph.nodes_dict.get(str(40)).key, self.g.centerPoint()[0])
        self.assertEqual(9.291743173960954, self.g.centerPoint()[1])

        self.g.load_from_json("../graph_data/MyG.json")
        self.assertEqual(self.g.graph.nodes_dict.get(str(3)).key, self.g.centerPoint()[0])
        self.assertEqual(3.2, self.g.centerPoint()[1])

        # self.g.load_from_json("../data/1000Nodes.json")
        # self.assertEquals(self.g.graph.nodes_dict.get(str(362)).key, self.g.centerPoint()[0])
        # self.assertEquals(0, self.g.centerPoint()[1])

    def test_plot_graph(self):
        try:
            self.assertTrue(self.g.plot_graph())
        except:
            assert False

    def isTheSame(self, dg: GraphInterface) -> bool:

        if self.g.graph.node_size != dg.node_size or self.g.graph.edge_size != dg.edge_size:
            return False
        n1 = None
        n2 = None
        i = 0
        for key in self.g.graph.nodes_dict.keys():
            n1 = self.g.graph.nodes_dict.get(key)
            n2 = dg.nodes_dict.get(key)
            self.assertEqual(n1.key, n2.key)
            self.assertEqual(n1.weight, n2.weight)
            self.assertEqual(n1.location, n2.location)
        e1 = None
        e2 = None
        for key1 in self.g.graph.out_edges.keys():
            for key2 in self.g.graph.out_edges.get(key1):
                e1 = self.g.graph.out_edges.get(key1).get(key2)
                e2 = dg.out_edges.get(key1).get(key2)
                self.assertEqual(e1.src, e2.src)
                self.assertEqual(e1.dest, e2.dest)
                self.assertEqual(e1.weight, e2.weight)
        return True
