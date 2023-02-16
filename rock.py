import pygame
from entity import Entity
from support import *
from settings import *
class Rock(Entity):
    def __init__(self,pos, groups,sprite_type ,surface = pygame.Surface((TILESIZE,TILESIZE))):
        super().__init__(groups)
        self.sprites = []
        self.animating = True
        self.sprites.append(pygame.image.load('Graphics/rocks/08_0.png'))
        self.sprites.append(pygame.image.load('Graphics/rocks/08_1.png'))
        self.sprites.append(pygame.image.load('Graphics/rocks/08_2.png'))
        self.sprites.append(pygame.image.load('Graphics/rocks/08_3.png'))
        self.sprites.append(pygame.image.load('Graphics/rocks/08.png'))

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = pos


    def update(self):
        if self.animating == True :
            self.current_sprite += 1
            if self.current_sprite >= len(self.sprites) :
                self.current_sprite = 0
            self.image = self.sprites[self.current_sprite]

