
# We used this graph_implementation from https://www.geeksforgeeks.org/priority-queue-in-python/
class PriorityQueue:
    def __init__(self):
        self.queue = []

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    def isEmpty(self):
        return len(self.queue) == 0

    def insert(self, data):
        self.queue.append(data)

    def size(self):
        return len(self.queue)

    def delete(self):
        try:
            minim = len(self.queue) - 1
            for i in range(len(self.queue)):
                if self.queue[i].w < self.queue[minim].w:
                    minim = i
            item = self.queue[minim]
            del self.queue[minim]
            return item
        except IndexError:
            print()
            exit()
