import random

class World:
    def __init__(self):
        self.chunks = {}
        self.count = 0

    def _generate_chunk(self, x, y):
        chunk = {}
        # To generate a world...
        for i in range(16):
            for j in range(16):
                chunk[(i,j)] = random.random()
        self.chunks[(x,y)] = chunk
        self.count += 1

    def query(self, x, y):
        if (x,y) not in self.chunks.keys():
            self._generate_chunk(x,y)
            
        return self.chunks[(x,y)] 
