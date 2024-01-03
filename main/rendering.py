import pygame
import math

class Rendering:
    def __init__(self, screen, world):
        self.count = 0
        self.size = 8
        self.y_size = math.ceil((screen.get_width() * math.sqrt(2)) / (16*self.size))
        self.x_size_min = -math.ceil((screen.get_width() / math.sqrt(2)) / (16*self.size))
        self.x_size_max = math.ceil((screen.get_height() / math.sqrt(2)) / (16*self.size))
        print((self.y_size, self.x_size_min, self.x_size_max))
        self.screen = screen
        self.world = world
        self.STONE = (60, 60, 60)
        self.DIRT = (128, 42, 0)
        self.GRASS = (0, 179, 60)
        self.OCEAN = (77, 166, 255)
        
    def draw(self, x, y):
        self.count = 0
        #print(world, screen)

        chunk_x = math.floor(x / 16)
        chunk_y = math.floor(y / 16)
        draw_chunk_x = chunk_x
        draw_chunk_y = chunk_y
        
        for a in range(0, self.y_size):
            a = 7
            draw_chunk_y = chunk_y + a
            for b in range(self.x_size_min, self.x_size_max):
                b = 0
                draw_chunk_x = chunk_x + b

                delta_chunk_x = draw_chunk_x - chunk_x
                delta_chunk_y = draw_chunk_y - chunk_y
                column_x = (-delta_chunk_x + delta_chunk_y) * (16*self.size/math.sqrt(2)) - x % (16*self.size)
                column_y = (delta_chunk_x + delta_chunk_y) * (16*self.size/math.sqrt(2)) - y % (16*self.size)
                if not (column_x + 16*self.size/math.sqrt(2) < 0 or column_x - 16*self.size/math.sqrt(2) > self.screen.get_width() or column_y + 32*self.size/math.sqrt(2) < 0 or column_y - 100 > self.screen.get_height()):
                    chunk = self.world.query(draw_chunk_x, draw_chunk_y)
                    for i in range(16):
                        for j in range(16):
                            height = chunk[(i, j)]
                            self._draw_column(column_x, column_y, i, j, height)

                
        
    def _draw_column(self, x, y, i, j, height):
        #height = max(height,0.5)
        draw_x = x + (-i + j) * (self.size/math.sqrt(2))
        draw_y = y + (i + j) * (self.size/math.sqrt(2)) - height*100
        if not (draw_x < 0 or draw_x > self.screen.get_width() or draw_y < 0 or draw_y - height > self.screen.get_height()): 
            self.count += 1
            if height*100 < self.world.WATER_LEVEL:
                self.screen.fill(self.OCEAN, (draw_x, math.floor(draw_y + height*100 - self.world.WATER_LEVEL), self.size, math.ceil(self.world.WATER_LEVEL - height*100)))
            grass, dirt, stone = draw_y, draw_y + 6, draw_y + 21
            grass_height, dirt_height, stone_height = math.floor(min(height*100, 6)), math.floor(min(height*100-6, 15)), height*100-21
            self.screen.fill(self.GRASS, (draw_x, grass, self.size, grass_height))
            h = 0
            while h < grass_height:
                self.screen.fill(self._color_lerp(self.GRASS, self.DIRT, h/grass_height), (draw_x, grass+h, self.size, 3))
                h += 3
            h = 0
            while h < dirt_height:
                self.screen.fill(self._color_lerp(self.DIRT, self.STONE, h/dirt_height), (draw_x, dirt+h, self.size, 3))
                h += 3
            self.screen.fill(self.STONE, (draw_x, stone, self.size, stone_height))

    def _color_lerp(self, tuple_one, tuple_two, percentage):
        return (tuple_one[0] * (1-percentage) + tuple_two[0] * percentage, tuple_one[1] * (1-percentage) + tuple_two[1] * percentage, tuple_one[2] * (1-percentage) + tuple_two[2] * percentage)
