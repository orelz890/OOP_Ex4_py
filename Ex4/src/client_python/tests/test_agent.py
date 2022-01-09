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

    def test_load_agent(self):
        agent: Agent = Agent()
        agent.load_agent(self.json_dict)
        self.assertEqual(-1, agent.id)
        self.assertEqual(0.0, agent.value)
        self.assertEqual(0, agent.src)
        self.assertEqual(1, agent.dest)
        self.assertEqual(1.0, agent.speed)
        self.assertEqual((35.18753053591606, 32.10378225882353, 0.0), agent.pos)
