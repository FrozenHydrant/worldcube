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
        pass

    def draw(self, x, y):
        self.count = 0
        #print(world, screen)

        chunk_x = math.floor(x / 16)
        chunk_y = math.floor(y / 16)
        draw_chunk_x = chunk_x
        draw_chunk_y = chunk_y
        
        for a in range(0, self.y_size):
            draw_chunk_y = chunk_y + a
            for b in range(self.x_size_min, self.x_size_max):
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
        draw_x = x + (-i + j) * (self.size/math.sqrt(2))
        draw_y = y + (i + j) * (self.size/math.sqrt(2)) - height*100
        if not (draw_x < 0 or draw_x > self.screen.get_width() or draw_y < 0 or draw_y - height > self.screen.get_height()): 
            self.count += 1
            self.screen.fill(((1-height)*255,(1-height)*255,(1-height)*255), (draw_x, draw_y, self.size, height*100))
