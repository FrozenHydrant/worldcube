import random
import collections

class World:
    def __init__(self):
        self.chunk_images = {}
        self.chunks = {}
        self.count = 0

        # Generation settings
        self.CHUNK_SIZE = 33
        self.WATER_LEVEL = 120
        self.VARIABILITY = 0.05

    def _generate_chunk(self, x, y):
        chunk = {}
        temp = random.random()
        
        #chunk[(0, 0)] = random.random()
        #chunk[(0, self.CHUNK_SIZE-1)] = random.random()
        #chunk[(self.CHUNK_SIZE-1, 0)] = random.random()
        #chunk[(self.CHUNK_SIZE-1, self.CHUNK_SIZE-1)] = random.random()
        # To generate a world...
        #for i in range(self.CHUNK_SIZE):
        #    for j in range(self.CHUNK_SIZE):
        #        chunk[(i,j)] = temp
        #self.chunks[(x,y)] = chunk

        points = collections.deque([(0, 0, self.CHUNK_SIZE-1), (0, self.CHUNK_SIZE-1, self.CHUNK_SIZE-1), (self.CHUNK_SIZE-1, 0, self.CHUNK_SIZE-1), (self.CHUNK_SIZE-1, self.CHUNK_SIZE-1, self.CHUNK_SIZE-1)])
        while len(points) > 0:
            point_x, point_y, strength = points.popleft()
            if (point_x, point_y) not in chunk:
                if strength != self.CHUNK_SIZE-1:
                    chunk[(point_x, point_y)] = self._get_height(x, y, point_x, point_y, strength, chunk)
                else:
                    chunk[(point_x, point_y)] = self._get_neighbouring_height(x, y, point_x, point_y)
                strength = int(strength/2)
                points.append((max(point_x - strength, 0), max(point_y - strength, 0), strength))
                points.append((max(point_x - strength, 0), min(point_y + strength, self.CHUNK_SIZE-1), strength))
                points.append((min(point_x + strength, self.CHUNK_SIZE-1), max(point_y - strength, 0), strength))
                points.append((min(point_x + strength, self.CHUNK_SIZE-1), min(point_y + strength, self.CHUNK_SIZE-1), strength))
                points.append((max(point_x - strength, 0), point_y, strength))
                points.append((min(point_x + strength, self.CHUNK_SIZE-1), point_y, strength))
                points.append((point_x, max(point_y - strength, 0), strength))
                points.append((point_x, min(point_y + strength, self.CHUNK_SIZE-1), strength))

        #print((len(chunk), " CHUNK LEN"))
        self.count += 1
        self.chunks[(x,y)] = chunk

    def query(self, x, y):
        if (x,y) not in self.chunks:
            self._generate_chunk(x,y)
            
        return self.chunks[(x,y)]

    def _get_height(self, cx, cy, x, y, s, chunk):
        points = [(x-s, y-s), (x-s, y+s), (x+s, y-s), (x+s, y+s), (x, y+s), (x, y-s), (x+s, y), (x-s, y)]
        accumulation = 0
        amount_accumulated = 0
        for point in points:
            if point in chunk:
                accumulation += chunk[point]
                amount_accumulated += 1
            else:
                #print(self._obtain_across_chunk(cx, cy, point[0], point[1]))
                temp = self._obtain_across_chunk(cx, cy, point[0], point[1])
                if temp != -1:
                     accumulation += temp
                     amount_accumulated += 1
        
        average = accumulation / amount_accumulated
        extra_salt = 1 + (1-2*random.random()) * self.VARIABILITY
        return average*extra_salt
    
    def _obtain_across_chunk(self, c, d, x, y):
        #print("WAIT")
        while x < 0:
            x += self.CHUNK_SIZE-1
            c -= 1
        while x > self.CHUNK_SIZE-1:
            x -= self.CHUNK_SIZE-1
            c += 1
        while y < 0:
            y += self.CHUNK_SIZE-1
            d -= 1
        while y > self.CHUNK_SIZE-1:
            y -= self.CHUNK_SIZE-1
            d += 1
        #print("DPONE")
        if (c, d) in self.chunks:
            return self.chunks[(c, d)][(x, y)]
        return -1
    
    def _get_neighbouring_height(self, chunk_x, chunk_y, point_x, point_y):
        cases = {(0, 0): [(0, -1, 0, self.CHUNK_SIZE-1), (-1, -1, self.CHUNK_SIZE-1, self.CHUNK_SIZE-1), (-1, 0, self.CHUNK_SIZE-1, 0)], (0, self.CHUNK_SIZE-1): [(-1, 0, self.CHUNK_SIZE-1, self.CHUNK_SIZE-1), (-1, 1, self.CHUNK_SIZE-1, 0), (0, 1, 0, 0)], (self.CHUNK_SIZE-1, self.CHUNK_SIZE-1): [(0, 1, self.CHUNK_SIZE-1, 0), (1, 1, 0, 0), (1, 0, 0, self.CHUNK_SIZE-1)], (self.CHUNK_SIZE-1, 0): [(0, -1, self.CHUNK_SIZE-1, self.CHUNK_SIZE-1), (1, -1, 0, self.CHUNK_SIZE-1), (1, 0, 0, 0)]}

        accumulation = 0
        amount_accumulated = 0
        for point_set in cases[(point_x, point_y)]:
            temp_chunk_x = chunk_x + point_set[0]
            temp_chunk_y = chunk_y + point_set[1]
            if (temp_chunk_x, temp_chunk_y) in self.chunks:
                chunk = self.chunks[temp_chunk_x, temp_chunk_y]
                accumulation += chunk[(point_set[2], point_set[3])]
                amount_accumulated += 1

        if amount_accumulated == 0:
            return random.random()
        average = accumulation / amount_accumulated
        extra_salt = 1 + (1-2*random.random()) * self.VARIABILITY
        return average*extra_salt


            
