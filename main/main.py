import pygame

from world import *
from rendering import *

# pygame setup
pygame.init()

MAIN_SCREEN = pygame.display.set_mode()

class MainClass:
    def __init__(self, screen):
        self.running = True
        self.x = 0
        self.y = 0
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.world = World()
        self.rendering = Rendering(screen, self.world)

    def begin_loop(self):

        pygame.display.flip()
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            #Rendering
            self.screen.fill("white")
            self.rendering.draw(self.x, self.y)
            pygame.display.flip()
        
            self.clock.tick(60)
            print(self.clock.get_fps())
            print(str(self.rendering.count) + " " + str(self.world.count) + " \n " + str(len(self.world.chunk_images)))
        pygame.quit()

def main():
    #test = {}
    #print((0,1) in test.keys())
    #test[(0,1)] = "hello"
    #print(test[(0,1)])
    #test[(0,1)] = "a"
    #print(test)
    main_instance = MainClass(MAIN_SCREEN)
    main_instance.begin_loop()

if __name__ == "__main__":
    main()
