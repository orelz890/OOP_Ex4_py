import unittest

from Ex4.src.graph_implementation.GraphAlgo import GraphAlgo
from Ex4.src.graph_implementation.DiGraph import DiGraph
from Ex4.src.graph_implementation.Node import Node
from Ex4.src.graph_implementation.Edge import Edge


class test_DiGraph(unittest.TestCase):
    g = DiGraph()
    n1 = Node(0, (0, 0, 0))
    n2 = Node(1, (1, 1, 1))
    n3 = Node(2, (2, 2, 2))
    e1 = Edge(0, 1, 1.5)
    e2 = Edge(0, 2, 2.0)
    e3 = Edge(1, 0, 3.5)

    def setUp(self) -> None:
        self.g = DiGraph()

    def test_v_size(self):
        self.assertEqual(0, self.g.node_size)
        self.g.add_node(self.n1.key, self.n1.location)
        self.assertEqual(1, self.g.node_size)
        self.g.remove_node(self.n1.key)
        self.assertEqual(0, self.g.node_size)

    def test_e_size(self):
        self.g.add_node(self.n1.key, self.n1.location)
        self.g.add_node(self.n2.key, self.n2.location)
        self.g.add_node(self.n3.key, self.n3.location)
        self.assertEqual(0, self.g.edge_size)
        self.g.add_edge(self.n1.key, self.n2.key, 22.5)
        self.assertEqual(1, self.g.edge_size)
        self.g.remove_edge(self.n1.key, self.n2.key)
        self.assertEqual(0, self.g.edge_size)

    def test_get_all_v(self):
        self.g.add_node(self.n1.key, self.n1.location)
        self.g.add_node(self.n2.key, self.n2.location)
        self.g.add_node(self.n3.key, self.n3.location)
        expected = {'0': (0, (0, 0, 0)), '1': (1, (1, 1, 1)), '2': (2, (2, 2, 2))}
        self.assertEqual(str(expected), str(self.g.get_all_v()))

    def test_all_in_edges_of_node(self):
        self.g.add_node(self.n1.key, self.n1.location)
        self.g.add_node(self.n2.key, self.n2.location)
        self.g.add_node(self.n3.key, self.n3.location)
        self.g.add_edge(0, 1, 22.5)
        self.g.add_edge(0, 2, 2.5)
        self.g.add_edge(1, 0, 13.5)
        self.g.add_edge(2, 0, 17.5)
        expected = {'1': (0, 22.5), '2': (0, 2.5)}
        self.assertEqual(str(expected), str(self.g.all_in_edges_of_node(self.n1.key)))

    def test_all_out_edges_of_node(self):
        self.g.add_node(self.n1.key, self.n1.location)
        self.g.add_node(self.n2.key, self.n2.location)
        self.g.add_node(self.n3.key, self.n3.location)
        self.g.add_edge(0, 1, 22.5)
        self.g.add_edge(0, 2, 2.5)
        self.g.add_edge(1, 0, 13.5)
        self.g.add_edge(2, 0, 17.5)
        expected = {'1': (1, 13.5), '2': (2, 17.5)}
        self.assertEqual(str(expected), str(self.g.all_out_edges_of_node(self.n1.key)))

    def test_get_mc(self):
        self.assertEqual(0, self.g.MC)
        self.g.add_node(self.n1.key, self.n1.location)
        self.g.add_node(self.n2.key, self.n2.location)
        self.g.add_edge(self.n1.key, self.n2.key, 21.3)
        self.g.remove_edge(self.n1.key, self.n2.key)
        self.g.remove_node(self.n1.key)
        self.g.remove_node(self.n2.key)
        self.assertEqual(6, self.g.MC)

    def test_add_edge(self):
        self.g.add_node(self.n1.key, self.n1.location)
        self.g.add_node(self.n2.key, self.n2.location)
        self.g.add_edge(self.n1.key, self.n2.key, 21.3)
        self.g.add_edge(self.n2.key, self.n1.key, 14.7)
        self.assertEqual(2, self.g.edge_size)
        edge1 = self.g.out_edges.get(str(0)).get(str(1))
        self.assertEqual(self.n1.key, edge1.src)
        self.assertEqual(self.n2.key, edge1.dest)
        self.assertEqual(21.3, edge1.weight)
        edge2 = self.g.out_edges.get(str(1)).get(str(0))
        self.assertEqual(self.n2.key, edge2.src)
        self.assertEqual(self.n1.key, edge2.dest)
        self.assertEqual(14.7, edge2.weight)
        self.assertEqual(self.g.out_edges[str(self.n1.key)][str(self.n2.key)],
                         self.g.into_edges[str(self.n2.key)][str(self.n1.key)])

    def test_add_node(self):
        self.g.add_node(self.n1.key, self.n1.location)
        self.g.add_node(self.n2.key, self.n2.location)
        self.assertEqual(2, self.g.node_size)
        node1 = self.g.nodes_dict.get(str(self.n1.key))
        self.assertEqual(self.n1.key, node1.key)
        self.assertEqual(self.n1.location, node1.location)
        self.assertEqual(self.n1.weight, node1.weight)
        node2 = self.g.nodes_dict.get(str(self.n2.key))
        self.assertEqual(self.n2.key, node2.key)
        self.assertEqual(self.n2.location, node2.location)
        self.assertEqual(self.n2.weight, node2.weight)

    def test_remove_node(self):
        self.g.add_node(self.n1.key, self.n1.location)
        self.g.add_node(self.n2.key, self.n2.location)
        self.g.add_node(self.n3.key, self.n3.location)
        self.assertEqual(3, self.g.node_size)
        self.g.add_edge(self.n1.key, self.n2.key, 21.3)
        self.g.add_edge(self.n2.key, self.n1.key, 14.7)
        self.g.add_edge(self.n2.key, self.n3.key, 12.5)
        self.g.add_edge(self.n3.key, self.n1.key, 12.5)
        self.assertEqual(4, self.g.edge_size)
        self.g.remove_node(self.n1.key)
        self.assertEqual(2, self.g.node_size)
        self.assertEqual(1, self.g.edge_size)
        edge_left = self.g.out_edges.get(str(self.n2.key)).get(str(self.n3.key))
        self.assertEqual(self.n2.key, edge_left.src)
        self.assertEqual(self.n3.key, edge_left.dest)
        self.assertEqual(12.5, edge_left.weight)

    def test_remove_edge(self):
        self.g.add_node(self.n1.key, self.n1.location)
        self.g.add_node(self.n2.key, self.n2.location)
        self.g.add_node(self.n3.key, self.n3.location)
        self.assertEqual(3, self.g.node_size)
        self.g.add_edge(self.n1.key, self.n2.key, 21.3)
        self.g.add_edge(self.n2.key, self.n1.key, 14.7)
        self.g.add_edge(self.n2.key, self.n3.key, 12.5)
        self.g.add_edge(self.n3.key, self.n1.key, 12.5)
        self.assertEqual(4, self.g.edge_size)
        edge1 = self.g.out_edges.get(str(self.n1.key)).get(str(self.n2.key))
        self.assertEquals(4, self.g.edge_size)
        self.assertTrue(edge1 is not None)
        self.g.remove_edge(self.n1.key, self.n2.key)
        edge1 = self.g.out_edges.get(str(self.n1.key)).get(str(self.n2.key))
        self.assertTrue(edge1 is None)
        self.assertEquals(3, self.g.edge_size)

    def test_set_all_w(self):
        self.g.set_all_tags(1.2, 890)
        for node in self.g.nodes_dict.values():
            self.assertEqual(1.2, node.w)
            self.assertEqual(890, node.tag)

    def test_dijkstra(self):
        is_valid = self.g.dijkstra(0)
        self.assertEqual(-1, is_valid)
        ga = GraphAlgo()
        ga.load_from_json("../graph_data/A0.json")
        is_valid = ga.graph.dijkstra(0)
        self.assertEqual(1, is_valid)
        for node in ga.graph.nodes_dict.values():
            node.tag >= 0
