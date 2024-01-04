import pygame
import math

class Rendering:
    def __init__(self, screen, world):
        # Colors
        self.STONE = (60, 60, 60)
        self.DIRT = (128, 42, 0)
        self.GRASS = (0, 179, 60)
        self.OCEAN = (77, 166, 255, 100)

        #Don't touch
        self.CHUNK_SIZE = world.CHUNK_SIZE
        
        # World settings
        self.TILE_SIZE = 4
        self.PIXEL_SIZE = self.TILE_SIZE/math.sqrt(2)
        self.HALF_CHUNK_PIXEL_SIZE = world.CHUNK_SIZE*self.PIXEL_SIZE
        
        self.count = 0
        self.y_size = math.ceil((screen.get_width() * math.sqrt(2)) / (self.CHUNK_SIZE*self.TILE_SIZE))
        self.x_size_min = -math.ceil((screen.get_width() / math.sqrt(2)) / (self.CHUNK_SIZE*self.TILE_SIZE))
        self.x_size_max = math.ceil((screen.get_height() / math.sqrt(2)) / (self.CHUNK_SIZE*self.TILE_SIZE))
        self.screen = screen
        self.world = world

    def draw(self, x, y):
        self.count = 0

        chunk_x = math.floor(x / self.CHUNK_SIZE)
        chunk_y = math.floor(y / self.CHUNK_SIZE)
        
        for a in range(0, self.y_size):
            #a = 3
            draw_chunk_y = chunk_y + a
            for b in range(self.x_size_min, self.x_size_max):
                #b = 2
                draw_chunk_x = chunk_x + b
                if (draw_chunk_x, draw_chunk_y) not in self.world.chunk_images.keys():
                    self.world.chunk_images[(draw_chunk_x, draw_chunk_y)] = self._create_image(draw_chunk_x, draw_chunk_y, chunk_x, chunk_y)

                delta_chunk_x = draw_chunk_x - chunk_x
                delta_chunk_y = draw_chunk_y - chunk_y
            
                start_x = (-delta_chunk_x + delta_chunk_y) * (self.HALF_CHUNK_PIXEL_SIZE) - x % (self.CHUNK_SIZE*self.TILE_SIZE)
                start_y = (delta_chunk_x + delta_chunk_y) * (self.HALF_CHUNK_PIXEL_SIZE) - y % (self.CHUNK_SIZE*self.TILE_SIZE)
                    
                self.screen.blit(self.world.chunk_images[(draw_chunk_x, draw_chunk_y)], (start_x - self.HALF_CHUNK_PIXEL_SIZE, start_y - 100))
                
    def _create_image(self, draw_chunk_x, draw_chunk_y, chunk_x, chunk_y):
            new_surface = pygame.Surface((math.floor(self.HALF_CHUNK_PIXEL_SIZE*2), math.floor(self.HALF_CHUNK_PIXEL_SIZE*2) + 100), pygame.SRCALPHA)
            column_x = self.HALF_CHUNK_PIXEL_SIZE
            column_y = 100
            chunk = self.world.query(draw_chunk_x, draw_chunk_y)
            for i in range(self.CHUNK_SIZE):
                for j in range(self.CHUNK_SIZE):
                    height = chunk[(i, j)]
                    self._draw_column(column_x, column_y, i, j, height, new_surface)

            return new_surface
        
    def _draw_column(self, x, y, i, j, height, new_surface):
        draw_x = x + (-i + j) * (self.PIXEL_SIZE)
        draw_y = y + (i + j) * (self.PIXEL_SIZE) - height*100
        if not (draw_x < 0 or draw_x > self.screen.get_width() or draw_y < -self.TILE_SIZE*self.CHUNK_SIZE or draw_y - height > self.screen.get_height()): 
            self.count += 1
            if height*100 < self.world.WATER_LEVEL:
                pygame.draw.rect(new_surface, self.OCEAN, (draw_x, math.floor(draw_y + height*100 - self.world.WATER_LEVEL), self.TILE_SIZE, math.ceil(self.world.WATER_LEVEL - height*100)))
            grass, dirt, stone = draw_y, draw_y + 6, draw_y + 21
            grass_height, dirt_height, stone_height = math.floor(min(height*100, 6)), math.floor(min(height*100-6, 15)), height*100-21
            new_surface.fill(self.GRASS, (draw_x, grass, self.TILE_SIZE, grass_height))
            h = 0
            while h < grass_height:
                new_surface.fill(self._color_lerp(self.GRASS, self.DIRT, h/grass_height), (draw_x, grass+h, self.TILE_SIZE, 1))
                h += 1
            h = 0
            while h < dirt_height:
                new_surface.fill(self._color_lerp(self.DIRT, self.STONE, h/dirt_height), (draw_x, dirt+h, self.TILE_SIZE, 3))
                h += 3
            new_surface.fill(self.STONE, (draw_x, stone, self.TILE_SIZE, stone_height))

    def _color_lerp(self, tuple_one, tuple_two, percentage):
        return (tuple_one[0] * (1-percentage) + tuple_two[0] * percentage, tuple_one[1] * (1-percentage) + tuple_two[1] * percentage, tuple_one[2] * (1-percentage) + tuple_two[2] * percentage)
