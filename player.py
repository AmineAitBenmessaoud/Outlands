import pygame
from settings import *
from support import import_folder
from entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites,create_attack,destroy_attack,create_magic):
        super().__init__(groups)
        self.image = pygame.image.load('player/caracter_main.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect

        #graphics setup :
        self.import_player_assets()
        self.status = 'right'
        self.obstacle_sprites = obstacle_sprites

        #mouvement
        self.past_direction = pygame.math.Vector2()
        self.past_direction.x=1
        self.attacking = False
        self.numattack=-1
        self.attack_cooldown = 400
        self.animation_speed=0.5
        
        self.attack_time = None

        #weapon
        self.creat_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200


        #magic
        self.creat_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None
        self.switch_duration_cooldown = 400

        #stats
        self.stats = {'health': 100,'energy': 60, 'attack': 10,'magic': 4,'speed': 20}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 0
        self.speed = self.stats['speed']

        #damage timer
        self.already_vulnerable=False
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 2200

        #inventory
        self.inventory = []

        self.game_over=False
        self.gameover_index=0
        self.game_over_screen=False




    def import_player_assets(self):
        #folder management
        character_path = 'player/'
        self.animations = {'left': [],'right': [],
			'right_idle':[],'left_idle':[],
			'right_attack_0':[],'left_attack_0':[],
			'right_attack_1':[],'left_attack_1':[],
			'right_attack_2':[],'left_attack_2':[],
			'dam_left': [],'dam_right': [],
			'gameover_left': [],'gameover_right': [],
		}
        for animation in self.animations.keys():
            full_path = character_path + animation + '/images'
            self.animations[animation] = import_folder(full_path)

    def input(self):
            if not self.game_over:
                
                if not self.attacking:
                    
                    keys = pygame.key.get_pressed()
                    

                    # movement input
                    if keys[pygame.K_UP] and self.past_direction.x == 1:
                        self.direction.y = -1
                        self.status = 'right'
                    elif keys[pygame.K_DOWN] and self.past_direction.x == 1:
                        self.direction.y = 1
                        self.status = 'right'
                    elif keys[pygame.K_UP] and self.past_direction.x == -1:
                        self.direction.y = -1
                        self.status = 'left'
                    elif keys[pygame.K_DOWN] and self.past_direction.x == -1:
                        self.direction.y = 1
                        self.status = 'left'
                    else:
                        self.direction.y = 0

                    if keys[pygame.K_RIGHT]:
                        self.direction.x = 1
                        self.past_direction.x = 1
                        self.status = 'right'
                    elif keys[pygame.K_LEFT]:
                        self.direction.x = -1
                        self.past_direction.x = -1
                        self.status = 'left'
                    else:
                        self.direction.x = 0

                    # attack input 
                    if keys[pygame.K_SPACE]:
                        self.attacking = True
                        if self.numattack<2:
                            self.numattack+=1
                        else:
                            self.numattack=0
                        self.attack_time = pygame.time.get_ticks()
                        

                    if keys[pygame.K_LCTRL]:
                        self.attacking = True
                        self.attack_time = pygame.time.get_ticks()
                        style = list(magic_data.keys())[self.magic_index]
                        strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                        cost = list(magic_data.values())[self.magic_index]['cost']
                        self.create_magic(style,strength,cost)
                        if self.numattack<2:
                            self.numattack+=1
                        else:
                            self.numattack=0
                        self.attack_time = pygame.time.get_ticks()
                        

                    
                    if keys[pygame.K_q] and self.can_switch_weapon:
                        self.can_switch_weapon=False
                        self.weapon_switch_time = pygame.time.get_ticks()
                        if self.weapon_index < len(list(weapon_data.keys())) - 1:
                            self.weapon_index += 1
                        else:
                            self.weapon_index = 0
                            
                        self.weapon = list(weapon_data.keys())[self.weapon_index]

                    if keys[pygame.K_e] and self.can_switch_magic:
                        self.can_switch_magic = False
                        self.weapon_switch_time = pygame.time.get_ticks()
                        self.magic_switch_time = pygame.time.get_ticks()
                        
                        if self.magic_index < len(list(magic_data.keys())) - 1:
                            self.magic_index += 1
                        else:
                            self.magic_index = 0

                        self.magic = list(magic_data.keys())[self.magic_index]


                self.magic = list(magic_data.keys())[self.magic_index]


    def get_status(self):
        if not self.game_over:
            if not self.vulnerable and not self.already_vulnerable:
                if self.past_direction.x == 1:
                    self.status='dam_right'
                if self.past_direction.x == - 1:
                    self.status='dam_left'
            elif  not 'dam' in self.status:
                
                
                # idle status
                if self.direction.x == 0 and self.direction.y == 0:
                    if not 'idle' in self.status and not 'attack' in self.status:
                        self.status = self.status + '_idle'

                if self.attacking:
                    self.direction.x = 0
                    self.direction.y = 0
                    if not 'attack' in self.status:
                        if 'idle' in self.status:
                            self.status = self.status.replace('_idle','_attack_'+str(self.numattack))
                        else:
                            self.status = self.status + '_attack_'+str(self.numattack)
                    else:
                        self.status=self.status[:-1]+str(self.numattack)
                

                else:
                    if 'attack' in self.status:
                        self.status = self.status.replace(self.status[self.status.index('_attack'):],'')
        if self.health<=0:
            self.game_over=True
            if self.past_direction.x==-1:
                self.status='gameover_left'
            if self.past_direction.x==1:
                self.status='gameover_right'
            if self.gameover_index==10 and 'gameover' in self.status:
                self.game_over_screen=True



    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown :
                self.attacking = False
        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True
                self.already_vulnerable=False


    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index 
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation) :
                if not self.game_over:
                    self.frame_index = 0
                else:
                    self.frame_index =len(animation)-1
                    self.gameover_index+=1

        
        



        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        # flicker 
        if not self.vulnerable and not self.game_over:
            if self.frame_index== 3:
                self.already_vulnerable=True
                if self.past_direction.x==1:
                    self.status='right'
                if self.past_direction.x==-1:
                    self.status='left'
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
            



    #oui
    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage
    def get_attack(self):
        return self.attacking
    def get_direct(self):
        return self.direction
    # to understand
    def update(self):
        
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
