import pygame
import sys

from level import Level
from settings import *
from debug import debug
from math import *

#kiilimi

class Game:
    def __init__(self):
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption('Outlands')
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("outlands")
        self.level = Level(3)

    def run(self):
        while True:
            keys = pygame.key.get_pressed()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT :
                    pygame.quit()
                    sys.exit()
            self.screen.fill('black')
            self.clock.tick(FPS)
            self.level.run()
            self.playerx = self.level.player.rect.centerx
            self.playery = self.level.player.rect.centery
            #if self.playerx >= 164*TILESIZE and self.level.scene == 1:
             #   if self.playery <= 241*TILESIZE :
              #     self.level = Level(1,2)
            #if self.level.scene == 2 and self.playery <= 16 :
             #   if self.playerx >= 15*TILESIZE and self.playerx <= 21*TILESIZE :
              #      self.level = Level(3) #just testing
            #Here comes the modification based on the position of the player        
            #if self.level == 2:
             #   if self.playerx >= 15*TILESIZE and self.playerx <= 21*TILESIZE :
              #      self.level = Level(3)
        


           
    def wave_value(self,f,a,boolean,phase):
        if boolean:
            return a*abs(sin(2*pi*f*pygame.time.get_ticks()+phase))
        else:
            return a*(sin(2*pi*f*pygame.time.get_ticks()+phase))


game = Game()
game.run()
