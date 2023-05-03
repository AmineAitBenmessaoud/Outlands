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
        self.level = Level(2)
        global TILESIZE

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.fill('black')
            self.clock.tick(FPS)
            self.level.run()
            self.playerx = self.level.player.rect.centerx
            self.playery = self.level.player.rect.centery
            if self.playerx >= 164*TILESIZE and self.level.scene == 1 and self.level.number == 1:
                if self.playery <= 241*TILESIZE :
                   self.level = Level(1,2)
            if self.level.scene == 2 and self.playery <= 16 :
                if self.playerx >= 15*TILESIZE and self.playerx <= 21*TILESIZE :
                    self.level = Level(3)
                     #just testing
            #Here comes the modification based on the position of the player        
            #if self.level == 2:
             #   if self.playerx >= 15*TILESIZE and self.playerx <= 21*TILESIZE :
              #      self.level = Level(3)
        



            pygame.display.update()
            self.level.rock_sprites.update()
            pygame.display.update()


game = Game()
game.run()
