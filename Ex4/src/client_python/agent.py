class Agent:

    def __init__(self, id: int, value: float, src: int, dest: int, speed: float, pos: str):
        self.id = id
        self.value = value
        self.src = src
        self.dest = dest
        self.speed = speed
        self.pos = pos

        self.path = []
        self.free_time = -1

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

    # def creat_pos(self, pos):
    #     temp_pos = pos.split(',')
    #     self.pos = (float(temp_pos[0]), float(temp_pos[1]), float(temp_pos[2]))

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
