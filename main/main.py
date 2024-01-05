import pygame

from world import *
from rendering import *

# pygame setup
pygame.init()

MAIN_SCREEN = pygame.display.set_mode()

class MainClass:
    def __init__(self, screen):
        self.running = True
        self.x = 50
        self.y = 0
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.world = World()
        self.rendering = Rendering(screen, self.world)
        self.font = pygame.font.SysFont("Comic Sans MS", 30)

    def begin_loop(self):

        pygame.display.flip()
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.rendering.THREAD_POOL.shutdown(wait=False)
                    self.running = False
                    break

            #Rendering
            self.screen.fill("white")
            self.rendering.draw(self.x, self.y)

            label = self.font.render(f"{self.clock.get_fps()}", 1, (0,0,0))
            self.screen.blit(label, (100,100))
            
            pygame.display.flip()
            # Speed Change
            #if (self.clock.get_fps() > 59):
            #    self.rendering.draw_delay /= 1.01
            #else:
            #    self.rendering.draw_delay *= 1.01
            #self.rendering.draw_delay = max(min(self.rendering.draw_delay, 1), 0)

            self.clock.tick(60)
            #print(self.clock.get_fps())
            #print(str(self.rendering.count) + " " + str(self.world.count) + " \n " + str(len(self.world.chunk_images)))

            # Movement
            self.x -= 0.5
            self.y -= 0.5
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
