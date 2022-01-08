from unittest import TestCase

from Ex4.src.graph_implementation.Node import Node


class TestNode(TestCase):

    def setUp(self) -> None:
        self.node1 = Node(0, (32.1232346, 35.3456645, 0.0))
        self.node2 = Node(0)
        self.node3 = Node(0, (32.1232346, 35.3456645, 0.0))
        self.node3.w = 2346

    def tests_node_creation(self):
        self.assertEqual((32.1232346, 35.3456645, 0.0), self.node1.location)
        self.assertEqual(0, self.node1.key)
        self.assertEqual(0, self.node1.tag)
        self.assertEqual(0, self.node1.w)
        self.assertEqual(0, self.node1.weight)
        self.assertEqual(False, self.node1.flag)

        self.assertTrue(self.node2.location is not None)
        self.assertEqual(0, self.node1.key)
        self.assertEqual(0, self.node1.tag)
        self.assertEqual(0, self.node1.w)
        self.assertEqual(0, self.node1.weight)
        self.assertEqual(False, self.node1.flag)

    def test_compering(self):
        self.assertTrue(self.node3 > self.node1)
        self.assertFalse(self.node3 < self.node1)
        self.assertTrue(self.node3 >= self.node1)
        self.assertFalse(self.node3 <= self.node1)
        self.assertFalse(self.node3 == self.node1)
        self.assertTrue(self.node3 != self.node1)

    def test_to_string(self):
        self.assertEqual("id: 0, position: (32.1232346, 35.3456645, 0.0)", self.node1.__str__())

    def test_pos_to_string(self):
        self.assertEqual("32.1232346,35.3456645,0.0", self.node1.pos_to_string())
