
class Pokemon:
    def __init__(self, value: float = 1.0, type: int = -1,
                 pos: tuple = (35.197656770719604, 32.10191878639921, 0.0)) -> None:
        self.id = None
        self.value = value
        self.type = type
        self.pos = pos
        self.src = None
        self.dest = None
        self.agent_id = None
        self.time = float('inf')

    def __repr__(self) -> str:
        return str((self.src, self.dest))

    def load_pokemon(self, pokemon1: dict):
        self.value = pokemon1.get("value")
        self.type = pokemon1.get("type")
        self.pos = tuple(pokemon1.get("pos").split(","))
