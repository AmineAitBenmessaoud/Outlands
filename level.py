import pygame
from support import *
from tile import Tile
from player import Player
from random import choice
from weapon import Weapon
from ui import UI
from enemy import Enemy
from debug import debug
from rock import Rock
from Object_level import Object_level
from math import *
from settings import *

class Level:

    def __init__(self,main,level_number,init=(0,0),scene_number=1):
        # surface principale
        self.player = None
        self.display_surface = pygame.display.get_surface()
        # types des sprites :
        self.visible_sprites = YSortCameraGroup(level_number,scene_number)
        self.obstacle_sprites = pygame.sprite.Group()
        self.obstacle_sprites_ennemie=pygame.sprite.Group()
        #attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.attacker_sprites =pygame.sprite.Group()
        self.nothing=pygame.sprite.Group()
        #objets à prendre
        self.level_objects = pygame.sprite.Group()
        #roches
        self.rock_sprites = pygame.sprite.Group()
        #boss
        self.boss_sprite = pygame.sprite.Group()
        #level data
        self.number = level_number
        self.scene = scene_number
        self.init=init
        if self.number==4: 
            self.initial_point=(1056,1536)

        self.game=main
        #user interface
        self.ui = UI()
        #shield
        self.shield=None
        self.shield_timer=0
        self.coef=180
        # creation de la map
        if level_number == 1:
            if scene_number == 1:
                self.create_map1_scene1()
            if scene_number == 2:
                self.create_map1_scene2()
            if scene_number == 3 :
                self.create_map1_scene3()
        if level_number == 2:
            self.create_map2()
        if level_number == 3: #This is Amine level (it will have also a slight modification on the size of the tiles)
            if scene_number == 1:
                self.create_map3()
            if scene_number == 2:
                self.create_map3_scene2()
            #if scene_number == 3:
             #   self.create_map3_scene3()
        # creation de la map4
        if level_number==4:
            if scene_number == 1:
                self.create_map4_scene1()
            if scene_number == 2:
                self.create_map4_scene2()
            if scene_number == 3 :
                self.create_map4_scene3()
            if scene_number == 4 :
                self.create_map4_scene4()
            if scene_number == 5 :
                self.create_map4_scene5()
            if scene_number == 6 :
                self.create_map4_scene6()
            if scene_number == 7 :
                self.create_map4_scene7()




    def create_map1_scene1(self):
        TILESIZE = 32
        layouts = {
            'grass' : import_csv_layout('real level/CSV/Level_1 map_grass.csv'),
            'plants': import_csv_layout('real level/CSV/Level_1 map_plants.csv'),
            'house': import_csv_layout('real level/CSV/Level_1 map_House.csv'),

            'boundary': import_csv_layout('real level/CSV/Level_1 map_Trees.csv'),
            'rocks': import_csv_layout('real level/CSV/Level_1 map_Rocks.csv'),
            'water_rocks' : import_csv_layout('real level/CSV/Level_1 map_water rocks.csv'),
            'wood' : import_csv_layout('real level/CSV/Level_1 map_Wood.csv'),
            'player' : import_csv_layout('real level/CSV/Level_1 map_player.csv'),
            'ennemies' : import_csv_layout('real level\CSV\Level_1 map_ennemies.csv')
        }
        i = 0
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        #test
                        if style == 'boundary' or style == 'rocks' or style == 'wood' or style== 'house':
                            Tile((x, y), [self.obstacle_sprites,self.obstacle_sprites_ennemie], 'invisible',pygame.Surface((TILESIZE,TILESIZE)))
                        if style == 'player' and i==0:
                            self.player = Player((60*16,40*16),
                                                 [self.visible_sprites,self.attacker_sprites],
                                                 self.obstacle_sprites,
                                                 self.create_attack,
                                                 self.destroy_attack,
                                                 self.create_magic,self.game.health)
                            i = 1                   
                        if style == 'ennemies' :
                            if col == '4150' :
                                monster_name = 'dragon'
                                group = [self.visible_sprites,self.attackable_sprites]
                            elif col == '3308' :
                                monster_name = 'squeleton'
                                group = [self.visible_sprites,self.attackable_sprites]
                            else :
                                monster_name = 'flying_rock'
                                group = [self.visible_sprites,self.attackable_sprites,self.obstacle_sprites]
                            Enemy(monster_name, (x,y), group, self.obstacle_sprites_ennemie, self.damage_player,1)


                            
                        if style == 'water_rocks' :
                            Tile((x, y), [self.obstacle_sprites,self.obstacle_sprites_ennemie], 'invisible',pygame.Surface((TILESIZE,TILESIZE)))

    def create_map1_scene2(self):
        TILESIZE = 16*4
        layouts = {
            'floor' : import_csv_layout("real level/CSV/First gym/interior_floor.csv"),
            'meubles': import_csv_layout("real level/CSV/First gym/interior_meubles.csv"),
            'tapis': import_csv_layout("real level/CSV/First gym/interior_Tapis.csv"),
            'wall': import_csv_layout("real level/CSV/First gym/interior_wall.csv"),
            'player' : import_csv_layout('real level/CSV/First gym/interior_player.csv')
        }
        i = 0
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        #test
                        if style == 'meubles' or style == 'wall' :
                            Tile((x, y), [self.obstacle_sprites,self.obstacle_sprites_ennemie], 'invisible',pygame.Surface((TILESIZE,TILESIZE)))
                        if style == 'player' and col == '163':
                            
                            self.player = Player((x,y),
                                                 [self.visible_sprites,self.attacker_sprites],
                                                 self.obstacle_sprites,
                                                 self.create_attack,
                                                 self.destroy_attack,
                                                 self.create_magic,self.game.health)

                            i = 1

    def create_map1_scene3(self):
        TILESIZE = 32
        layouts = {
            'grass': import_csv_layout("real level/CSV/boss/mini_boss_grass.csv"),
            'wall': import_csv_layout("real level/CSV/boss/mini_boss_mur.csv"),
            'rocks': import_csv_layout("real level/CSV/boss/mini_boss_rocks.csv"),
            'sol': import_csv_layout('real level/CSV/boss/mini_boss_sol.csv'),
            'player' : import_csv_layout('real level/CSV/boss/mini_boss_player.csv'),
            'boss' : import_csv_layout('real level/CSV/boss/mini_boss_boss.csv')
        }
        i = 0
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'wall' :
                            Tile((x,y),[self.obstacle_sprites,self.obstacle_sprites_ennemie],'wall',pygame.Surface((TILESIZE,TILESIZE)))
                        if style == 'player' and row != 0  :
                            
                            self.player = Player((x, y),
                                                 [self.visible_sprites,self.attacker_sprites],
                                                 self.obstacle_sprites,
                                                 self.create_attack,
                                                 self.destroy_attack,
                                                 self.create_magic,self.game.health)
                        if style == 'boss' :
                            if col == '1' :
                                Enemy('lv1_boss', (x,y), [self.visible_sprites,self.attackable_sprites], self.obstacle_sprites_ennemie, self.damage_player,1)
 
                        
                            
    def create_map2(self):
        TILESIZE = 32
        layouts = {
            'grass' : import_csv_layout('Level 2\BIGMAP_Surface.csv'),
            'ennemi' : import_csv_layout('Level 2\BIGMA_Ennemi.csv'),

            'boundary': import_csv_layout('Level 2\BIGMAP_Trees.csv'),
            'player' : import_csv_layout('real level/CSV/Level_1 map_player.csv'),

        }
        i = 0
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        #test
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites,self.obstacle_sprites_ennemie], 'invisible',pygame.Surface((TILESIZE,TILESIZE)))
                        if style == 'player' and i==0:
                            self.player = Player((60*16,40*16),
                                                 [self.visible_sprites,self.attacker_sprites],
                                                 self.obstacle_sprites,
                                                 self.create_attack,
                                                 self.destroy_attack,
                                                 self.create_magic,self.game.health) 

                            i = 1
                        if style == 'ennemi' and col == '10':
                            Enemy('bamboo', (x, y),
                                  [self.visible_sprites, self.attackable_sprites],
                                  self.obstacle_sprites_ennemie, self.damage_player)
    def create_map3(self):
        TILESIZE = 60
        layouts = {
            "boundary": import_csv_layout("Graphics/passage/files_collision_boundaries.csv"),
            "grass": import_csv_layout("Graphics/passage/files_collision_movable.csv"),
            "object": import_csv_layout("Graphics/passage/files_collision_object.csv"),
            "entities": import_csv_layout("Graphics/passage/files_collision_entities.csv"),
        }
        graphics = {
            "grass": import_folder("Graphics/grass"),
            "objects": import_folder("Graphics/objects"),
        }

        # row gives us y position
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):

                    if col != "-1":
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == "boundary":
                            Tile(
                                (x, y),
                                [self.obstacle_sprites,self.obstacle_sprites_ennemie],
                                "invisible",
                                pygame.Surface((TILESIZE,TILESIZE))
                            )

                        if style == "entities":
                            if col == "68":
                                self.player = Player(
                                    (x,y),
                                    [self.visible_sprites,self.attacker_sprites],
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic,self.game.health
                                )
                            else:
                                if col == "4":
                                    monster_name = "squeleton"
                                #elif col == "391":
                                 #   monster_name = "spirit"
                                #elif col == "31":
                                 #   monster_name = "raccoon"
                                #else:
                                  #  monster_name = "squid"
                                Enemy(
                                    monster_name,
                                    (x, y),
                                    [self.visible_sprites, self.attackable_sprites],
                                    self.obstacle_sprites_ennemie,
                                    self.damage_player,
                                    # self.destroy_attack,
                                    # self.create_magic,
                                    self.number
                                )
    def create_map3_scene2(self):
        TILESIZE = 60
        layouts = {
            "boundary": import_csv_layout("Graphics/boss_map/boss_obstacle.csv"),
            "grass": import_csv_layout("Graphics/boss_map/boss_movable.csv"),
            "entities": import_csv_layout("Graphics/boss_map/boss_entities.csv"),
        }
        graphics = {
            "grass": import_folder("Graphics/grass"),
            "objects": import_folder("Graphics/objects"),
        }

        # row gives us y position
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):

                    if col != "-1":
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == "boundary":
                            Tile(
                                (x, y),
                                [self.obstacle_sprites,self.obstacle_sprites_ennemie],
                                "invisible",
                                pygame.Surface((TILESIZE,TILESIZE))
                            )

                        if style == "entities":
                            if col == "16":
                                self.player = Player(
                                    (x,y),
                                    [self.visible_sprites,self.attacker_sprites],
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic,self.game.health
                                )
                            else:
                                if col == "305":
                                    monster_name = "squeleton"
                                #elif col == "391":
                                 #   monster_name = "spirit"
                                #elif col == "31":
                                 #   monster_name = "raccoon"
                                #else:
                                  #  monster_name = "squid"
                                Enemy(
                                    monster_name,
                                    (x, y),
                                    [self.visible_sprites, self.attackable_sprites],
                                    self.obstacle_sprites_ennemie,
                                    self.damage_player,
                                    # self.destroy_attack,
                                    # self.create_magic,
                                    self.number
                                )
    def create_map4_scene1(self):
        TILESIZE=32
        layouts = {
            'boundary': import_csv_layout('map_csv/scene1/fairy_floor_blocks_bare.csv'),
            'entities': import_csv_layout('map_csv/scene1/fairy_Entity_pos_0.csv')
        }
        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites,self.obstacle_sprites_ennemie],'invisible',pygame.Surface((TILESIZE,TILESIZE)))
                        if style == 'entities':
                            if col == '0':
                                if not(self.init[0] or self.init[1]):
                                    self.player = Player(
                                        (x,y),
                                        [self.visible_sprites,self.attacker_sprites],
                                        self.obstacle_sprites,self.create_attack,
                                    self.destroy_attack,
                                        self.create_magic,self.game.health)
                                else:
                                    self.player = Player(
                                        self.init,
                                        [self.visible_sprites,self.attacker_sprites],
                                        self.obstacle_sprites,self.create_attack,
                                    self.destroy_attack,
                                        self.create_magic,self.game.health)
                            else:
                                if col == '1': monster_name = 'ghost'
                                elif col == '4': monster_name = 'dark_fairy'
                                elif col == '2': monster_name ='bat'
                                
                                else: monster_name = 'boss'
                                Enemy(monster_name,(x,y),[self.visible_sprites,self.attackable_sprites],self.nothing,self.damage_player,self.number)
    def create_map4_scene2(self):
        TILESIZE=32
        layouts = {
            'boundary': import_csv_layout('map_csv/scene2/tree._floor_blocks.csv'),
            'entities': import_csv_layout('map_csv/scene2/tree._pos.csv')
        }
        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites,self.obstacle_sprites_ennemie],'invisible',pygame.Surface((TILESIZE,TILESIZE)))
                        if style == 'entities':
                            if col == '1536':
                                if not (self.init[0] or self.init[1]):
                                    self.player = Player(
                                        (x,y),
                                        [self.visible_sprites,self.attacker_sprites],
                                        self.obstacle_sprites,self.create_attack,
                                    self.destroy_attack,
                                        self.create_magic,self.game.health)
                                else:
                                    self.player = Player(
                                        self.init,
                                        [self.visible_sprites,self.attacker_sprites],
                                        self.obstacle_sprites,self.create_attack,
                                    self.destroy_attack,
                                        self.create_magic,self.game.health)
                            #else:
                                #if col == '1': monster_name = 'ghost'
                                #elif col == '4': monster_name = 'dark_fairy'
                                #elif col == '2': monster_name ='bat'
                                
                                #else: monster_name = 'boss'
                                #Enemy(monster_name,(x,y),[self.visible_sprites,self.attackable_sprites],self.nothing,self.damage_player)
    def create_map4_scene3(self):
        TILESIZE=32
        layouts = {
            'boundary': import_csv_layout('map_csv/scene3/chateaux_floor_blocks.csv'),
            'entities': import_csv_layout('map_csv/scene3/chateaux_perso.csv')
        }
        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites,self.obstacle_sprites_ennemie],'invisible',pygame.Surface((TILESIZE,TILESIZE)))
                        if style == 'entities':
                            if col == '1536':
                                if not(self.init[0] or self.init[1]):
                                    self.player = Player(
                                        (x,y),
                                        [self.visible_sprites,self.attacker_sprites],
                                        self.obstacle_sprites,self.create_attack,
                                    self.destroy_attack,
                                        self.create_magic,self.game.health)
                                else:
                                    self.player = Player(
                                        self.init,
                                        [self.visible_sprites,self.attacker_sprites],
                                        self.obstacle_sprites,self.create_attack,
                                    self.destroy_attack,
                                        self.create_magic,self.game.health)
                            #else:
                                #if col == '1': monster_name = 'ghost'
                                #elif col == '4': monster_name = 'dark_fairy'
                                #elif col == '2': monster_name ='bat'
                                
                                #else: monster_name = 'boss'
                                #Enemy(monster_name,(x,y),[self.visible_sprites,self.attackable_sprites],self.nothing,self.damage_player)
    def create_map4_scene4(self):
        TILESIZE=32
        layouts = {
            'boundary': import_csv_layout('map_csv/scene4/etage1_floor_blocks.csv'),
            'entities': import_csv_layout('map_csv/scene4/etage1_pos.csv')
        }
        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites,self.obstacle_sprites_ennemie],'invisible',pygame.Surface((TILESIZE,TILESIZE)))
                        if style == 'entities':
                            if col == '1536':
                                if not(self.init[0] or self.init[1]):
                                    self.player = Player(
                                        (x,y),
                                        [self.visible_sprites,self.attacker_sprites],
                                        self.obstacle_sprites,self.create_attack,
                                    self.destroy_attack,
                                        self.create_magic,self.game.health)
                                else:
                                    self.player = Player(
                                        self.init,
                                        [self.visible_sprites,self.attacker_sprites],
                                        self.obstacle_sprites,self.create_attack,
                                    self.destroy_attack,
                                        self.create_magic,self.game.health)
                            #else:
                                #if col == '1': monster_name = 'ghost'
                                #elif col == '4': monster_name = 'dark_fairy'
                                #elif col == '2': monster_name ='bat'
                                
                                #else: monster_name = 'boss'
                                #Enemy(monster_name,(x,y),[self.visible_sprites,self.attackable_sprites],self.nothing,self.damage_player)
    def create_map4_scene5(self):
        TILESIZE=32
        layouts = {
            'boundary': import_csv_layout('map_csv/scene5/etage2_floor_blocks.csv'),
            'entities': import_csv_layout('map_csv/scene5/etage2_pos.csv')
        }
        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites,self.obstacle_sprites_ennemie],'invisible',pygame.Surface((TILESIZE,TILESIZE)))
                        if style == 'entities':
                            if col == '1536':
                                
                                if not(self.init[0] or self.init[1]):
                                    
                                    self.player = Player(
                                        (x,y),
                                        [self.visible_sprites,self.attacker_sprites],
                                        self.obstacle_sprites,self.create_attack,
                                    self.destroy_attack,
                                        self.create_magic,self.game.health)
                                else:
                                    
                                    self.player = Player(
                                        self.init,
                                        [self.visible_sprites,self.attacker_sprites],
                                        self.obstacle_sprites,self.create_attack,
                                    self.destroy_attack,
                                        self.create_magic,self.game.health)
                                #else:
                                #if col == '1': monster_name = 'ghost'
                                #elif col == '4': monster_name = 'dark_fairy'
                                #elif col == '2': monster_name ='bat'
                                
                                #else: monster_name = 'boss'
                                #Enemy(monster_name,(x,y),[self.visible_sprites,self.attackable_sprites],self.nothing,self.damage_player)
    def create_map4_scene6(self):
        TILESIZE=32
        layouts = {
            'boundary': import_csv_layout('map_csv/scene6/roof_floor_blocks.csv'),
            'entities': import_csv_layout('map_csv/scene6/roof_pos.csv')
        }
        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites,self.obstacle_sprites_ennemie],'invisible',pygame.Surface((TILESIZE,TILESIZE)))
                        if style == 'entities':
                            if col == '1536':
                                if not(self.init[0] or self.init[1]):
                                    self.player = Player(
                                        (x,y),
                                        [self.visible_sprites,self.attacker_sprites],
                                        self.obstacle_sprites,self.create_attack,
                                    self.destroy_attack,
                                        self.create_magic,self.game.health)
                                else:
                                    self.player = Player(
                                        self.init,
                                        [self.visible_sprites,self.attacker_sprites],
                                        self.obstacle_sprites,self.create_attack,
                                    self.destroy_attack,
                                        self.create_magic,self.game.health)
                            #else:
                                #if col == '1': monster_name = 'ghost'
                                #elif col == '4': monster_name = 'dark_fairy'
                                #elif col == '2': monster_name ='bat'
                                
                                #else: monster_name = 'boss'
                                #Enemy(monster_name,(x,y),[self.visible_sprites,self.attackable_sprites],self.nothing,self.damage_player)
    def create_map4_scene7(self):
        TILESIZE=32
        layouts = {
            'boundary': import_csv_layout('map_csv/scene7/sky_floorblocks.csv'),
            'entities': import_csv_layout('map_csv/scene7/sky_pos.csv')
        }
        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites,self.obstacle_sprites_ennemie],'invisible',pygame.Surface((TILESIZE,TILESIZE)))
                        if style == 'entities':
                            if col == '1536':
                                if not(self.init[0] or self.init[1]):
                                    self.player = Player(
                                        (x,y),
                                        [self.visible_sprites,self.attacker_sprites],
                                        self.obstacle_sprites,self.create_attack,
                                        self.destroy_attack,
                                        self.create_magic,self.game.health)
                                else:
                                    self.player = Player(
                                        self.init,
                                        [self.visible_sprites,self.attacker_sprites],
                                        self.obstacle_sprites,self.create_attack,
                                        self.destroy_attack,
                                        self.create_magic,self.game.health)
                            #else:
                                #if col == '1': monster_name = 'ghost'
                                #elif col == '4': monster_name = 'dark_fairy'
                                #elif col == '2': monster_name ='bat'
                                
                                #else: monster_name = 'boss'
                                #Enemy(monster_name,(x,y),[self.visible_sprites,self.attackable_sprites],self.nothing,self.damage_player)

    


    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visible_sprites,self.attack_sprites])

    def create_magic(self,style,strength,cost):
        print(style)
        print(strength)
        print(cost)

    def destroy_attack(self):
        if self.current_attack != None:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        
        if self.attacker_sprites and self.player.attacking:
            
            for attack_sprite in self.attacker_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
                if collision_sprites :
                    
                    for target_sprite in collision_sprites:
                        target_sprite.get_damage(self.player,self)

    def damage_player(self,amount,attack_type):
        if self.player.vulnerable and not self.player.attacking:
            self.game.health-=amount
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            #spawn particles


    def collect_object(self):
        if self.level_objects:
            keys = pygame.key.get_pressed()
            collision = pygame.sprite.spritecollide(self.player,self.level_objects,False)
            for object in collision :
                if object.sprite_type == 'auto_collect' :
                    object.kill()
                elif object.sprite_type == 'press_to_collect' :
                    self.player_instructions()
                    if keys[pygame.K_r]:
                        object.kill()
                        self.player.inventory.append(object)


    def player_instructions(self):
        font = pygame.font.Font(None, 36)
        text = font.render("Press R to collect", True, 'white')
        self.display_surface.blit(text, (WIDTH/2-100, 100))

    def boss_1(self):
        if self.boss_sprite :
            if self.player.rect.centerx >= 3960 and self.player.rect.centery <= 1698 :
                for rock in self.rock_sprites :
                    rock.animating = True
                    self.obstacle_sprites.add(rock)
        else :
            for rock in self.rock_sprites:
                rock.kill()



    def run(self,main,num):
		# update and draw the game
        if num:
            self.player.kill()
            self.player = Player(
                                    self.initial_point,
                                    [self.visible_sprites,self.attacker_sprites],
                                    self.obstacle_sprites,self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic,self.game.health)
            self.player.game_over=False
            self.game.health=100
            self.player.health=100
            self.player.game_over_screen=False
            self.player.status='right'
            #self.player.rect.topleft=self.initial_point
        
        if self.player.activate:
            self.coef-=0.5
            alpha= ((0.6*self.wave_value2(1/1600,255,0,0))/153)*40+self.coef
            
            self.shield.image.set_alpha(alpha)
            self.shield.rect.centerx=self.player.rect.centerx-10
            self.shield.rect.centery=self.player.rect.centery
            self.shield.hitbox.centerx=self.player.rect.centerx-10
            self.shield.hitbox.centery=self.player.rect.centery
            
        if ((pygame.time.get_ticks()-self.shield_timer))>10000 and self.player.activate:
            self.player.activate=False
            self.shield.kill()
            self.coef=180



        self.visible_sprites.custom_draw(self.player)
        
        self.player.input(self)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        
        self.player_attack_logic()
        self.ui.display(self.player)
        self.collect_object()
        if self.player.game_over_screen:
            main.game_active=False
    def wave_value2(self,f,a,boolean,phase):
        if boolean:
            return a*abs(sin(2*pi*f*pygame.time.get_ticks()+phase))
        else:
            return a*(sin(2*pi*f*pygame.time.get_ticks()+phase))

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self, level_number, scene_number=1):
        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # floor
        if level_number == 1:
            if scene_number == 1:
                image = pygame.image.load('real level/Level_1 map.png')
                tr_image = pygame.transform.scale(image,(10240,11264))
                self.floor_surface = tr_image.convert()
            if scene_number == 2:
                image = pygame.image.load('real level/gym1-1.png')
                tr_image = pygame.transform.scale(image,(768*4,521*4))
                self.floor_surface = tr_image.convert()
            if scene_number == 3:
                image = pygame.image.load('real level/mini_boss.png')
                tr_image = pygame.transform.scale(image,(2048*2,1536*2))
                self.floor_surface = tr_image.convert()
        if level_number == 2:
            self.floor_surface = pygame.image.load('Level 2\BIGMAP.png').convert()
        if level_number == 3:
            if scene_number == 1:
                self.floor_surface = pygame.image.load("Graphics\passage\map.png").convert()
            if scene_number == 2:
                image = pygame.image.load("Graphics/boss_map/map.png").convert() 
                tr_image = pygame.transform.scale(image,(480*3.75,480*3.75))
                self.floor_surface = tr_image.convert()   
        if level_number == 4:
            if scene_number == 1:
                self.floor_surface = pygame.image.load('maps/fairy.png').convert()
            if scene_number == 2:
                self.floor_surface = pygame.image.load('maps/tree1.png').convert()
            if scene_number == 3:
                self.floor_surface = pygame.image.load('maps/chateaux1.png').convert()
            if scene_number == 4:
                self.floor_surface = pygame.image.load('maps/etage11.png').convert()
            if scene_number == 5:
                self.floor_surface = pygame.image.load('maps/etage2.png').convert()
            if scene_number == 6:
                self.floor_surface = pygame.image.load('maps/roof.png').convert()
            if scene_number == 7:
                self.floor_surface = pygame.image.load('maps/sky.png').convert()
        

        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        # offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if
                         hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)



