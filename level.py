import pygame
from settings import *
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



class Level:

    def __init__(self,level_number,scene_number=1):
        # surface principale
        self.player = None
        self.display_surface = pygame.display.get_surface()
        # types des sprites :
        self.visible_sprites = YSortCameraGroup(level_number,scene_number)
        self.obstacle_sprites = pygame.sprite.Group()
        #attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        #objets à prendre
        self.level_objects = pygame.sprite.Group()
        #roches
        self.rock_sprites = pygame.sprite.Group()
        #boss
        self.boss_sprite = pygame.sprite.Group()
        #level data
        self.number = level_number
        self.scene = scene_number



        #user interface
        self.ui = UI()

        # creation de la map
        if level_number == 1:
            if scene_number == 1:
                self.create_map1_scene1()
            if scene_number == 2:
                self.create_map1_scene2()
        if level_number == 2:
            self.create_map2()



    def create_map1_scene1(self):
        layouts = {
            'grass' : import_csv_layout('real level/CSV/Level_1 map_grass.csv'),
            'plants': import_csv_layout('real level/CSV/Level_1 map_plants.csv'),
            'house': import_csv_layout('real level/CSV/Level_1 map_House.csv'),

            'boundary': import_csv_layout('real level/CSV/Level_1 map_Trees.csv'),
            'rocks': import_csv_layout('real level/CSV/Level_1 map_Rocks.csv'),
            'water_rocks' : import_csv_layout('real level/CSV/Level_1 map_water rocks.csv'),
            'wood' : import_csv_layout('real level/CSV/Level_1 map_Wood.csv'),
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
                        if style == 'boundary' or style == 'rocks' or style == 'wood' or style== 'house':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        if style == 'player' and i==0:
                            self.player = Player((60*16,40*16),
                                                 [self.visible_sprites],
                                                 self.obstacle_sprites,
                                                 self.create_attack,
                                                 self.destroy_attack,
                                                 self.create_magic)
                            Enemy('flying_rock', (x + 200, y + 600),
                                  [self.visible_sprites,self.obstacle_sprites],
                                  self.obstacle_sprites, self.damage_player)
                            Enemy('dragon', (x + 700, y + 600),
                                  [self.visible_sprites, self.attackable_sprites],
                                  '', self.damage_player)


                            i = 1
                        if style == 'water_rocks' :
                            Tile((x, y), [self.obstacle_sprites], 'invisible')

    def create_map1_scene2(self):
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
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        if style == 'player' and col == '163':
                            print(x,y)
                            self.player = Player((x,y),
                                                 [self.visible_sprites],
                                                 self.obstacle_sprites,
                                                 self.create_attack,
                                                 self.destroy_attack,
                                                 self.create_magic)

                            i = 1

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
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
                if collision_sprites :
                    for target_sprite in collision_sprites:
                        target_sprite.get_damage(self.player,attack_sprite.sprite_type)

    def damage_player(self,amount,attack_type):
        if self.player.vulnerable:
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



    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)

        self.player_attack_logic()
        self.ui.display(self.player)
        self.collect_object()


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
                self.floor_surface = pygame.image.load('real level/Level_1 map.png').convert()
            if scene_number == 2:
                self.floor_surface = pygame.image.load('real level/gym1-1.png').convert()
        if level_number == 2:
            self.floor_surface = pygame.image.load('Graphics/outlandssmap.png').convert()

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



