class Pokemon:
    def __init__(self, value=-1, type=-1, pos=(35.197656770719604, 32.10191878639921, 0.0)) -> None:
        self.id = -1
        self.value = value
        self.type = type
        self.pos = pos
        self.src = -1
        self.dest = -1
        self.agent_id = -1
        self.time = -1

    def __repr__(self) -> str:
        return str(self.value)

    def load_pokemon(self, pokemon1: dict):
        self.value = pokemon1.get("value")
        self.type = pokemon1.get("type")
        values: list = pokemon1.get("pos").split(",")
        temp = []
        for item in values:
            temp.append(float(item))
        self.pos = tuple(temp)

    # def creat_pos(self, pos):
    #     temp_pos = pos.split(",")
    #     self.pos = (float(temp_pos[0]), float(temp_pos[1]), float(temp_pos[2]))
