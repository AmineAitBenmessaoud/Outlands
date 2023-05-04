import pygame
from settings import *
class UI :
    def __init__(self):

        #general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)

        #bar setup
        self.health_bar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH,BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10,34,ENERGY_BAR_WIDTH,BAR_HEIGHT)

        #convert weapon dict
        self.weapon_graphics = []
        for weapon in weapon_data.values() :
            path = weapon['graphic']
            weapon1 = pygame.image.load(path).convert_alpha()
            weapon1 = pygame.transform.scale(weapon1,(40,40))
            self.weapon_graphics.append(weapon1)

        #convert magic dict
        self.magic_graphics = []
        for magic in magic_data.values():
            path = magic['graphic']
            magic1 = pygame.image.load(path).convert_alpha()
            magic1 = pygame.transform.scale(magic1, (40, 40))
            self.magic_graphics.append(magic1)

    def show_bar(self,current,max_amount,bg_rect,color):
        #draw the bg
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)

        #converting stat to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width


        #drawing the bar
        pygame.draw.rect(self.display_surface,color,current_rect)
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3)

    def show_exp(self,exp):
        text_surf = self.font.render('EXP : ' + str(int(exp)),False,TEXT_COLOR)
        x = 10
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomleft = (x,y))

        pygame.draw.rect(self.display_surface,UI_BG_COLOR,text_rect.inflate(20,20))
        self.display_surface.blit(text_surf,text_rect)
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,text_rect.inflate(20,20),3)

    def selection_box(self,left,top):
        bg_rect = pygame.Rect(left,top,ITEM_BOX_SIZE,ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3)
        return bg_rect


    def weapon_overlay(self,weapon_index):
        bg_rect = self.selection_box(self.display_surface.get_size()[0]-100,10) #weapon
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center)
        self.display_surface.blit(weapon_surf,weapon_rect)

    def magic_overlay(self,magic_index):
        bg_rect = self.selection_box(self.display_surface.get_size()[0]-100,10+ITEM_BOX_SIZE) #magic
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center = bg_rect.center)
        self.display_surface.blit(magic_surf,magic_rect)

    def display(self,player):
        self.show_bar(player.health,player.stats['health'],self.health_bar_rect,HEALTH_COLOR)
        self.show_bar(player.energy,player.stats['energy'],self.energy_bar_rect,ENERGY_COLOR)

        self.show_exp(player.exp)

        self.weapon_overlay(player.weapon_index)
        self.magic_overlay(player.magic_index)