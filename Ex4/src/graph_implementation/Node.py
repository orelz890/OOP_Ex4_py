import math
import random


class Node:
    def __init__(self, key: int, pos: tuple = None):
        self.flag = True if pos is None else False
        if pos is None:
            pos = (random.uniform(35.19, 35.22), random.uniform(32.05, 32.22), 0.0)
        self.key = key
        self.location = pos
        self.weight = 0
        self.tag = 0
        self.w = 0
        self.outEdges = {}
        self.inEdges = {}

    def add_out_edge(self, weight: float, dest: int):
        self.outEdges[dest] = weight
        self.outEdges.values()

    # add in edge
    def add_in_edge(self, weight: float, src: int):
        self.inEdges[src] = weight

    def __repr__(self):
        return f"({self.key}, {self.location})"

    def __str__(self):
        s = "id: " + str(self.key) + ", position: " + str(self.location)
        return s

    def __lt__(self, other):
        return self.w < other.w

    def __le__(self, other):
        return self.w <= other.w

    def __eq__(self, other):
        return self.w == other.w

    def __ne__(self, other):
        return self.w != other.w

    def __gt__(self, other):
        return self.w > other.w

    def __ge__(self, other):
        return self.w >= other.w

    def pos_to_string(self):
        string = "{},{},{}".format(self.location[0], self.location[1], self.location[2])
        return string

    def distance(self, loc: (float, float, float)) -> float:
        temp1 = []
        for item in loc:
            temp1.append(float(item))
        position = tuple(temp1)
        temp2 = []
        for item in self.location:
            temp2.append(float(item))
        location = tuple(temp2)
        ans = math.sqrt(math.pow(location[0] - position[0], 2) + math.pow(location[1] - position[1], 2))
        return ans


# if __name__ == '__main__':
#     node1 = Node(0, (1, 2, 3))
#     pos2 = (2, 2, 3)
#     print(node1.distance(pos2))
