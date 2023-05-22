import pygame
from settings import *
from entity import Entity
from support import *
class ally(Entity):
    def __init__(self,ally_name,pos,groups,obstacle_sprites,map,sprite_type,id):

        self.id=id
        # general setup
        super().__init__(groups)
        self.sprite_type = sprite_type
        
        # graphics setup
        self.import_graphics(ally_name)
        self.status = 'idle_left'
        if 'fairy' in ally_name:self.status = 'left'
        self.frame_index=0

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        #movement
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites
        self.ismoving=False
        self.olddirectionx=-1
        self.direct=pygame.math.Vector2(WIDTH,HEIGHT).magnitude()

        self.distance = 0
        self.distance_vect=pygame.math.Vector2() 
        self.direction= pygame.math.Vector2() 
        self.dist_vect_sign= pygame.math.Vector2()
        self.directionx= pygame.math.Vector2() 
        self.num=0

        # stats
        self.ally_name = ally_name
        ally_info = ally_data[self.ally_name]
        self.health = ally_info['health']
        self.speed = ally_info['speed']
        self.resistance = ally_info['resistance']
        self.animation_speed = ally_info['animation_speed']
        self.text=ally_info['text']

        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 4500
        self.map=map

    def import_graphics(self,name):
        self.animations = {'idle_left':[] , 'move_left':[] ,'attack_left':[],
                           'idle_right':[] , 'move_right':[] ,'attack_right':[]}
        main_path = f'Graphics/{name}/'
        
        if 'fairy'in name:
            self.animations = {'down':[],'up':[],'right':[],'left':[]}
            for animation in self.animations.keys():
                self.animations[animation] = import_folder(main_path + animation +'/images/') 
        

    def get_player_distance_direction(self,player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        self.distance_vect=player_vec - enemy_vec
        self.distance = (self.distance_vect).magnitude()
        self.dist_vect_sign[0]=self.distance_vect[0]
        self.dist_vect_sign[1]=self.distance_vect[1]
        self.distance_vect[0]=abs(self.distance_vect[0])
        self.distance_vect[1]=abs(self.distance_vect[1])

        if self.vulnerable:
            if self.distance > 0  :
                self.direction = (player_vec - enemy_vec).normalize()
            else:
                self.direction = pygame.math.Vector2()

        return (self.distance,self.direction,self.distance_vect,self.dist_vect_sign)

    def get_status(self,player,mode=1):
        if mode:
            self.distance = self.get_player_distance_direction(player)[0]
            self.distance_vect=self.get_player_distance_direction(player)[2]
            
            if self.vulnerable:
                self.direction= self.get_player_distance_direction(player)[1]
            if self.map==4 :
                if self.vulnerable: 
                    self.frame_index = 0
                if 'fairy'in self.ally_name:
                        # movement input
                    if     self.direction[0]>0 and float(self.distance_vect[0])>200 :
                        self.status = 'right'
                    elif    self.direction[0]<0 and float(self.distance_vect[0])>200:
                        self.status = 'left'
                    elif     float(self.distance_vect[0])<200 and self.direction[1]>0 :
                        self.status = 'down'
                    elif    self.direction[1]<0 and float(self.distance_vect[0])<200:
                        self.status = 'up'
                    else:
                        self.status = 'down'
        else:#follow path
            pass   
    def actions(self,player):
        if self.vulnerable:
            if self.ismoving or 'move' in self.status:
                self.direction = self.get_player_distance_direction(player)[1]
            else:
                self.direction = pygame.math.Vector2()
       

    def animate(self):
        print(self.frame_index,'****')
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if 'attack' in self.status :
                self.can_attack = False
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)


        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else :
            self.image.set_alpha(255)


    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.vulnerable :
            if current_time - self.hit_time >= self.invincibility_duration*3/8:
                self.vulnerable = True

    def get_damage(self,player,level):
        if self.vulnerable :
            self.direction = self.get_player_distance_direction(player)[1]
            if player.attacking :
                if  level.ui.frame_index!=8:
                    level.ui.frame_index+=1
                self.health -= player.get_full_weapon_damage()
                self.hit_time = pygame.time.get_ticks()
                self.vulnerable = False

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance
    def check_death(self):
        if self.health <= 0:
            self.kill()
            self.dead=True

    def in_the_list(self,list):
        for enemy in list:
            if enemy.id==self.id:
                return True
        return False
    def update(self):
        if self.distance<=1100:
            
            self.near=True
            
            self.hit_reaction()
            self.animate()
            self.cooldowns()
            self.check_death()

    def ally_update(self,player):
        self.get_status(player)
        self.actions(player)
        self.move(self.speed)