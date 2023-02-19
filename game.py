import pygame
import sys

from level import Level
from settings import *
from debug import debug



class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("outlands")
        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.fill('black')
            self.clock.tick(FPS)
            self.level.run()
            self.level.rock_sprites.update()
            pygame.display.update()


game = Game()
game.run()
