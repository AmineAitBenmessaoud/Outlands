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

class Level:

    def __init__(self):
        # surface principale
        self.player = None
        self.display_surface = pygame.display.get_surface()
        # types des sprites :
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        #attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        #objets à prendre
        self.level_objects = pygame.sprite.Group()
        #roches
        self.rock_sprites = pygame.sprite.Group()


        # creation de la map
        self.create_map()

        #user interface
        self.ui = UI()




    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('csv_new/outlandsmapboop_floor blocks2.csv'),
            'rock1': import_csv_layout('csv_new/outlandsmapboop_rocks1floorblocks.csv'),
            'rock2': import_csv_layout('csv_new/outlandsmapboop_rocks2floorblocks.csv'),
            'entities':import_csv_layout('csv_new/playerenemies_player.csv')
        }
        i = 0
        j = 0
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        #test
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')

                        if  style == 'rock1':
                            if i%4 == 0 :
                                rock = pygame.image.load('Graphics/08.png')
                                Rock((x, y), [self.visible_sprites,self.rock_sprites], 'rock',rock)
                            i+=1

                        if style == 'rock2' :
                            if j%4 == 0 :
                                rock = pygame.image.load('Graphics/rocks/08_0.png')
                                Rock((x, y), [self.visible_sprites,self.rock_sprites], 'rock',rock)
                            j+=1




                        if style == 'entities' :
                                if col == '394' :
                                    Enemy('bamboo', (2600, 6500),
                                          [self.visible_sprites, self.attackable_sprites],
                                          self.obstacle_sprites,self.damage_player)
                                    image = pygame.image.load('NinjaAdventure/Items/Food/Beaf.png')
                                    image = pygame.transform.scale(image,(64,64))
                                    Tile((2700, 6700), [self.visible_sprites,self.level_objects], 'auto_collect',image)
                                    image2 = pygame.image.load('NinjaAdventure/Items/Potion/Hear.png')
                                    image2 = pygame.transform.scale(image2,(64,64))
                                    Tile((2700, 6800), [self.visible_sprites,self.level_objects], 'press_to_collect',image2)



                                    print(x,y)
                                    self.player = Player((x,y),
                                                         [self.visible_sprites],
                                                         self.obstacle_sprites,
                                                         self.create_attack,
                                                         self.destroy_attack,
                                                         self.create_magic)
                                else :
                                    if col == '390':
                                        monster_name = 'bamboo'
                                    elif col == '391' :
                                        monster_name = 'spirit'
                                    elif col == '392' :
                                        monster_name = 'raccoon'
                                    else :
                                        monster_name = 'squid'
                                    Enemy(monster_name,(x,y),
                                          [self.visible_sprites,self.attackable_sprites],
                                          self.obstacle_sprites,self.damage_player)





    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visible_sprites,self.attack_sprites])

    def create_magic(self,style,strength,cost):
        print(style)
        print(strength)
        print(cost)

    def destroy_attack(self):
        if self.current_attack:
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


    def run(self):
        if self.player.rect.centerx >= 4064 and self.player.rect.centery <= 1698 :
            pass
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)

        self.player_attack_logic()
        self.ui.display(self.player)
        self.collect_object()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # floor
        self.floor_surface = pygame.image.load('Graphics/outlandsmapboop.png').convert()

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

    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)



