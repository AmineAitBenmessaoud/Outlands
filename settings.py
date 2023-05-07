FPS = 60
import pygame 
pygame.init()
from math import *
# game setup
info = pygame.display.Info()
WIDTH    = info.current_w
HEIGHT   = info.current_h
TILESIZE = 32

weapon_data = {
    'gem_blue' : {'cooldown':100,'damage':15,'graphic':'gems/gem_blue'},
    'gem_blue2' : {'cooldown':250,'damage':30,'graphic':'gems/gem_blue2'},
    'gem_green' : {'cooldown':100,'damage':15,'graphic':'gems/gem_green'},
    'gem_green2' : {'cooldown':250,'damage':30,'graphic':'gems/gem_green2'},
    'gem_pink' : {'cooldown':100,'damage':15,'graphic':'gems/gem_pink'},
    'gem_purpel' : {'cooldown':250,'damage':30,'graphic':'gems/gem_purpel'},
    'gem_red' : {'cooldown':100,'damage':15,'graphic':'gems/gem_red'},
    'gem_redorange' : {'cooldown':250,'damage':30,'graphic':'gems/gem_redorange'},
    'gem_orange' : {'cooldown':100,'damage':15,'graphic':'gems/gem_orange'},
    
}

lvl1_obj = {
    'coin' : {'type':'auto_collect', 'graphic':'Graphics/coin.jpg' },
    'weapon' : {'type':'weapon','graphic':'NinjaAdventure/Items/Weapons/Lance2/Sprite.png'}

}

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = 'public-pixel-font/PublicPixel-z84yD.ttf'
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# magic
magic_data = {
	'flame': {'strength': 5,'cost': 20,'graphic':'Graphics/flame/fire.png'},
	'heal' : {'strength': 20,'cost': 10,'graphic':'Graphics/heal/heal.png'}}

# enemy
monster_data = {
	'squid': {'health': 100,'exp':100,'damage':20,'attack_type': 'slash', 'attack_sound':'../audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360,'animation_speed':0.8,'near_distance':200},
	'raccoon': {'health': 300,'exp':250,'damage':40,'attack_type': 'claw',  'attack_sound':'../audio/attack/claw.wav','speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400,'animation_speed':0.8,'near_distance':200},
	'spirit': {'health': 100,'exp':110,'damage':8,'attack_type': 'thunder', 'attack_sound':'../audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350,'animation_speed':0.8,'near_distance':200},
	'squeleton': {'health': 100,'exp':120,'damage':10,'attack_type': 'slash', 'attack_sound':'../audio/attack/slash.wav', 'speed': 2, 'resistance': 3, 'attack_radius': 0, 'notice_radius': 300,'animation_speed':0.5,'near_distance':200},
	'flying_rock': {'health': 150,'exp':0,'damage':0,'attack_type': 'none', 'attack_sound':'../audio/attack/slash.wav', 'speed': 0, 'resistance': 3, 'attack_radius': 0, 'notice_radius' : 0,'animation_speed':0.8,'near_distance':200},
	'Tower': {'health': 150,'exp':0,'damage':0,'attack_type': 'none', 'attack_sound':'../audio/attack/slash.wav', 'speed': 0, 'resistance': 3, 'attack_radius': 0, 'notice_radius' : 0,'animation_speed':0.8,'near_distance':200},
	'dragon': {'health' : 300 , 'exp': 100, 'damage': 10, 'attack_type': 'firebreath', 'attack_sound': '../audio/attack/slash.wav','speed': 0.05, 'resistance': 3, 'attack_radius': 180, 'notice_radius': 500,'animation_speed':0.8,'near_distance':200},
	'ghost': {'health': 60,'exp':1,'damage':15,'attack_type': 'slash', 'attack_sound':'../audio/attack/slash.wav',
                           'speed': 11, 'resistance':100 , 'attack_radius': 25, 'notice_radius': 600,'animation_speed':0.7,'near_distance':30},
    'dark_fairy': {'health': 30,'exp':0,'damage':2,'attack_type': 'claw',  'attack_sound':'../audio/attack/claw.wav',
                            'speed': 6, 'resistance': 30, 'attack_radius': 10, 'notice_radius': 250,'animation_speed':0.2,'near_distance':60},
    'bat': {'health': 120,'exp':2,'damage':20,'attack_type': 'thunder', 'attack_sound':'../audio/attack/fireball.wav',
                            'speed': 9, 'resistance': 3, 'attack_radius': 90, 'notice_radius': 1000,'animation_speed':0.8,'near_distance':200},
    'boss': {'health': 300,'exp':10,'damage':30,'attack_type': 'leaf_attack', 'attack_sound':'../audio/attack/slash.wav', 
                           'speed': 12, 'resistance': 60, 'attack_radius': 140,'notice_radius': 1000,'animation_speed':0.5,'near_distance':80},
    'lv1_boss' : {'health': 300,'exp':10,'damage':30,'attack_type': 'leaf_attack', 'attack_sound':'../audio/attack/slash.wav', 
                           'speed': 12, 'resistance': 60, 'attack_radius': 140,'notice_radius': 1000,'animation_speed':0.5,'near_distance':80}
}

