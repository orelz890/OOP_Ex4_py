from unittest import TestCase
from Ex4.src.client_python.agent import Agent


class TestAgent(TestCase):
    json_dict = {
        "id": 0,
        "value": 0.0,
        "src": 0,
        "dest": 1,
        "speed": 1.0,
        "pos": "35.18753053591606,32.10378225882353,0.0"
    }
    json_dict1 = {
        "id": 1,
        "value": 0.0,
        "src": 14,
        "dest": 12,
        "speed": 3.0,
        "pos": "35.18753053591707,32.10378225882220,0.0"
    }
    json_dict2 = {
        "id": 2,
        "value": 0.0,
        "src": 9,
        "dest": 5,
        "speed": 5.0,
        "pos": "35.18753053591616,32.10378225882210,0.0"
    }

    def test_load_agent(self):
        agent: Agent = Agent(0,0,0,0,0,"4")
        agent.load_agent(self.json_dict)
        self.assertEqual(0, agent.id)
        self.assertEqual(0.0, agent.value)
        self.assertEqual(0, agent.src)
        self.assertEqual(1, agent.dest)
        self.assertEqual(1.0, agent.speed)
        self.assertEqual((35.18753053591606, 32.10378225882353, 0.0), agent.pos)

        agent1: Agent = Agent(1, 3, 3, 1,10, "4")
        agent1.load_agent(self.json_dict1)
        self.assertEqual(1, agent1.id)
        self.assertEqual(0.0, agent1.value)
        self.assertEqual(14, agent1.src)
        self.assertEqual(12, agent1.dest)
        self.assertEqual(3.0, agent1.speed)
        self.assertEqual((35.18753053591707, 32.10378225882220, 0.0), agent1.pos)

        agent2: Agent = Agent(2, 3, 3, 1, 10, "4")
        agent2.load_agent(self.json_dict2)
        self.assertEqual(2, agent2.id)
        self.assertEqual(0.0, agent2.value)
        self.assertEqual(9, agent2.src)
        self.assertEqual(5, agent2.dest)
        self.assertEqual(5.0, agent2.speed)
        self.assertEqual((35.18753053591616, 32.10378225882210, 0.0), agent2.pos)



