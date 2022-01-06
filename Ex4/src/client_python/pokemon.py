class pokemon:
    def __init__(self, pok_data: dict) -> None:
        self.value = pok_data['value']
        self.type = int(pok_data['type'])
        pok_pos = pok_data['pos'].split(',')
        self.pos = []
        for n in pok_pos:
            self.pos.append(float(n))
        self.src = None
        self.dest = None
        self.agent = None

    def __repr__(self) -> str:
        return str((self.src, self.dest))


if __name__ == '__main__':
    p=pokemon(
                {

                        "value": 5.0,
                        "type": -1,
                        "pos": "35.197656770719604,32.10191878639921,0.0"

                }

    )
    print(p.pos)
