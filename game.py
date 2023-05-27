import pygame
import sys

from level import Level
from settings import *
from debug import debug
from math import *
#import pyglet
#import pygame.movie

#kiilimi

class Game:
    def __init__(self):
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption('Outlands')
        self.clock = pygame.time.Clock()
        self.game_active=True
        self.player_stand = pygame.image.load('player/gameover_right_6.png').convert_alpha()
        self.player_stand_rect = self.player_stand.get_rect(center = (WIDTH/2,HEIGHT*5/8))
        self.test_font = pygame.font.Font('font/Pixeltype.ttf', 250)
        self.game_name = self.test_font.render('GAME OVER',False,(0, 9, 94))

        self.game_name_rect = self.game_name.get_rect(center = (WIDTH/2,HEIGHT*2/8))

        self.test_font_message = pygame.font.Font('font/Pixeltype.ttf', 150)
        self.game_message = self.test_font_message.render('You Looser',False,(0, 9, 94))
        self.game_message_rect = self.game_message.get_rect(center = (WIDTH/2,HEIGHT*4/8))

        self.test_font_message_0 = pygame.font.Font('font/Pixeltype.ttf', 250)
        self.game_message_0 = self.test_font_message_0.render('press enter to restart',False,(148, 201, 255))
        self.game_message_rect_0 = self.game_message_0.get_rect(center = (WIDTH/2,HEIGHT*7/8))
        #waiting screen
        self.test_font_message_0 = pygame.font.Font('font/Pixeltype.ttf', 150)
        self.game_message_0 = self.test_font_message_0.render('waiting the player to get trough',False,(0, 9, 94))
        self.game_message_rect_0 = self.game_message_0.get_rect(center = (WIDTH/2,HEIGHT*7/8))

        self.player_wait = pygame.image.load('wait.png').convert_alpha()
        self.player_wait_rect = self.player_stand.get_rect(center = (WIDTH/2,HEIGHT*1/2))

        #health
        self.health=100


        self.number_gameover=0

        self.level = Level(self,1,(0,0),1)
    def run(self):
        while True:
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT :
                    pygame.quit()
                    sys.exit()
            if keys[pygame.K_l]:
                pygame.quit()
                sys.exit()
            if self.game_active:

                self.screen.fill('black')

                self.level.run(self,self.number_gameover)
                #changement de maps
                self.playerx = self.level.player.rect.centerx
                self.playery = self.level.player.rect.centery

                if self.level.number == 1 and self.level.scene == 1 :
                    if self.playerx >= 5276 and self.playerx <= 5590 and self.playery == 7803 :
                       self.level = Level(self,1,(0,0),2)
                if self.level.number == 1 and self.level.scene == 2 :
                    if self.playerx >= 1100 and self.playerx <= 1200 and self.playery >= 120 and self.playery <= 140 :
                        self.level = Level(self,1,(0,0),3)
                if self.level.number == 1 and self.level.scene == 3 :

                    if not self.level.attackable_sprites :
                        if self.playerx >= 2100 and self.playerx <= 2256 and self.playery <= 374 :
                            self.level = Level(self,2,(0,0),1)
                if self.level.number == 2:
                   if (self.playerx >= 3500 and self.playerx <= 4500) and (self.playery >= 4450 and self.playery <= 4700):
                        self.level = Level(self,3,(0,0))
                if (self.playery<=12 and self.level.scene ==1  and self.level.number==3):
                    self.level = Level(self,3,(0,0),2)
                elif (self.playery<=25 and self.level.scene ==2  and self.level.number==3):
                   self.level = Level(self,4,(0,0),1)
                if (self.playerx>=2610 and self.playerx<=2748 ) and self.level.scene == 1 and self.level.number==4:
                    if self.playery >= 5500 and self.playery <= 5550 :
                        self.level = Level(self,4,(0,0),2)
                        self.playerx = 1336
                        self.playery = 2954
                if self.level.scene == 2 and self.level.number==4:
                    if   self.playery >= 3100 :
                        self.screen.fill((69,174,116))
                        self.screen.blit(self.game_message_0,self.game_message_rect_0)
                        self.screen.blit(self.player_wait,self.player_wait_rect)
                        self.playery+=60
                    if self.playery >=3200:
                        self.level = Level(self,4,(2690,5650))
                if (self.playerx>=22600 and self.playerx<=22808 ) and self.level.scene == 1 and self.level.number==4:
                    if self.playery >= 4900 and self.playery <= 5190 :
                        self.level = Level(self,4,(0,0),3)
                        self.playerx = 1624
                        self.playery = 2046
                if (self.playerx>=2100 and self.playerx<=2200 ) and self.level.scene == 3 and self.level.number==4:
                    if  self.playery <= 1450 :
                        self.level = Level(self,4,(0,0),4)
                        self.playerx = 1016
                        self.playery = 1438
                if (self.playerx>=1900 and self.playerx<=2200 ) and self.level.scene == 4 and self.level.number==4:
                    if  self.playery >= 3110 :
                        self.level = Level(self,4,(2150,1510),3)
                if (self.playerx>=1900 and self.playerx<=2200 ) and self.level.scene == 4 and self.level.number==4:
                    if  self.playery <= 1780 :
                        self.level = Level(self,4,(0,0),5)
                if (self.playerx>=1900 and self.playerx<=2200 ) and self.level.scene == 5 and self.level.number==4:
                    if  self.playery >= 3050 :
                        self.level = Level(self,4,(2000,1840),4)
                if (self.playerx>=1900 and self.playerx<=2200 ) and self.level.scene == 5 and self.level.number==4:
                    if  self.playery <= 1760 :
                        self.level = Level(self,4,(0,0),6)
                if (self.playerx>=2800 and self.playerx<=2990 ) and self.level.scene == 6 and self.level.number==4:
                    if  self.playery >= 4190 :
                        self.level = Level(self,4,(2000,1840),5)
                if (self.playerx>=2800 and self.playerx<=2950 ) and self.level.scene == 6 and self.level.number==4:
                    if  self.playery <= 1380 :
                        self.level = Level(self,4,(0,0),7)
                if (self.playerx>=1500 and self.playerx<=1700 ) and self.level.scene == 7 and self.level.number==4:
                    if  self.playery >= 2070 :
                        self.level = Level(self,4,(2820,1450),6)

                if self.number_gameover:
                    self.number_gameover=0
                pygame.display.update()
                self.clock.tick(FPS)
            else:
                if keys[pygame.K_RETURN]:
                    self.game_active=True
                self.screen.fill((69,174,116))
                self.screen.blit(self.player_stand,self.player_stand_rect)
                self.screen.blit(self.game_name,self.game_name_rect)
                self.screen.blit(self.game_message,self.game_message_rect)
                if not keys[pygame.K_RETURN]:
                    alpha = self.wave_value(1/800,255,1,0)

                    self.game_message_0.set_alpha(alpha)
                    self.screen.blit(self.game_message_0,self.game_message_rect_0)
                    self.game_name_rect = self.game_name.get_rect(center = (WIDTH/2+self.wave_value(1/1600,255,0,0),HEIGHT*2/8))
                    self.game_message_rect = self.game_message.get_rect(center = (WIDTH/2+self.wave_value(1/2000,100,0,0),HEIGHT*4/8+self.wave_value(1/2000,100,0,pi/2)))
                self.number_gameover=1
                pygame.display.update()
                self.clock.tick(FPS)




    def wave_value(self,f,a,boolean,phase):
        if boolean:
            return a*abs(sin(2*pi*f*pygame.time.get_ticks()+phase))
        else:
            return a*(sin(2*pi*f*pygame.time.get_ticks()+phase))


game = Game()
game.run()
