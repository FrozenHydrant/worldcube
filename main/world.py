import random

class World:
    def __init__(self):
        self.chunk_images = {}
        self.chunks = {}
        self.count = 0

        # Generation settings
        self.CHUNK_SIZE = 32
        self.WATER_LEVEL = 35

    def _generate_chunk(self, x, y):
        chunk = {}
        # To generate a world...
        for i in range(self.CHUNK_SIZE):
            for j in range(self.CHUNK_SIZE):
                chunk[(i,j)] = random.random()
        self.chunks[(x,y)] = chunk
        self.count += 1

    def query(self, x, y):
        if (x,y) not in self.chunks.keys():
            self._generate_chunk(x,y)
            
        return self.chunks[(x,y)] 
