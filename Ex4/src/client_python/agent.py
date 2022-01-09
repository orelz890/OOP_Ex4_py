
class Agent:
    def __init__(self, id: int = -1):
        self.id = id
        self.value = 0.0
        self.src = -1
        self.dest = -1
        self.speed = 1.0
        self.pos = pos = (35.18753053591606, 32.10378225882353, 0.0)
        self.path = []

    def load_agent(self, agent: dict):
        self.value = agent.get("value")
        self.src = agent.get("src")
        self.dest = agent.get("dest")
        self.speed = agent.get("speed")
        values: list = agent.get("pos").split(",")
        temp = []
        for item in values:
            temp.append(float(item))
        self.pos = tuple(temp)


# if __name__ == '__main__':
#     agent = Agent()
#     agent.load_agent(
#
#                     {
#                         "id": 0,
#                         "value": 0.0,
#                         "src": 0,
#                         "dest": 1,
#                         "speed": 1.0,
#                         "pos": "35.18753053591606,32.10378225882353,0.0"
#                     })
#     print(agent.value)
#     print(agent.id)
#     print(agent.pos)