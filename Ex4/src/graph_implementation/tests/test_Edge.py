from unittest import TestCase
from Ex4.src.graph_implementation.Edge import Edge

class TestEdge(TestCase):

    def setUp(self) -> None:

        self.edge1 = Edge(0, 1, 435)
        self.edge2 = Edge(1, 2, 34)
        self.edge3 = Edge(2, 3, 45)
        self.edge4 = Edge(3, 4, 23)
        self.edge5 = Edge(4, 5, 134)
        self.edge6 = Edge(5, 0, 21)


    def tests_node_creation(self):
        self.assertEqual(0, self.edge1.src)
        self.assertEqual(1, self.edge1.dest)
        self.assertEqual(435, self.edge1.weight)

    def test_compering(self):
        self.assertTrue(self.edge1 > self.edge2)
        self.assertFalse(self.edge1 < self.edge2)
        self.assertTrue(self.edge1 >= self.edge2)
        self.assertFalse(self.edge1 <= self.edge2)
        self.assertFalse(self.edge1 == self.edge2)
        self.assertTrue(self.edge1 != self.edge2)

    def test_to_string(self):
        self.assertEqual("(0, 1, 435)", self.edge1.__str__())
