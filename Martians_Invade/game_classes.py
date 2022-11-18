import pygame
import random
import math


class SpaceMan(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, screen_width, screen_height, image_list):
        pygame.sprite.Sprite.__init__(self)
        self.step_counter = 0
        self.Step_counter = 0
        self.number_of_updates_made = 0
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.Surface((width, height))
        self.image_list = image_list
        self.image = image_list[0]
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.radius = width/2 
        self.velocity = 3
        self.walking = True
        self.score = 0
        self.enemies_killed = 0
        self.health = 5


    def rotate(self):
        # getting the mouse x and y position 
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

        #Angle logic
        deltaX = self.mouse_x - self.rect.x
        deltaY = self.mouse_y - self.rect.y
        self.angle = math.atan2(deltaX, deltaY) * 180 / math.pi       
        
        if self.walking:
            old_center = self.rect.center
            self.image = self.image_list[self.Step_counter]
            self.image.set_colorkey((0, 0, 0))
            self.image = pygame.transform.rotate(self.image, self.angle)
            self.rect = self.image.get_rect()
            self.rect.center = old_center
        
        if not self.walking:
            old_center = self.rect.center
            self.image = self.image_list[0]
            self.image.set_colorkey((0, 0, 0))
            self.image = pygame.transform.rotate(self.image, self.angle)
            self.rect = self.image.get_rect()
            self.rect.center = old_center

        
    def fire(self, bulett_image):
        self.rotate()
        if self.angle >= 75 and self.angle <= 180  or\
            self.angle <= -90: 
            bullet = Projectiles(self.rect.centerx, self.rect.centery, self.mouse_x, self.mouse_y, bulett_image, self.screen_width, self.screen_height)
        
        if self.angle <=-62:
            bullet = Projectiles(self.rect.left, self.rect.top + 20, self.mouse_x, self.mouse_y, bulett_image, self.screen_width, self.screen_height)
            
        if self.angle < 75 and self.angle > -62:
            bullet = Projectiles(self.rect.left, self.rect.centery, self.mouse_x, self.mouse_y, bulett_image, self.screen_width, self.screen_height)

        return bullet

    def update(self):
        self.rotate()
        event = pygame.key.get_pressed()            
        if event[pygame.K_a] and self.rect.x > self.velocity:
            self.rect.x -= self.velocity

        if event[pygame.K_d] and self.rect.right < self.screen_width - self.velocity:
            self.rect.x += self.velocity

        if event[pygame.K_w] and self.rect.y > self.velocity:
            self.rect.y -= self.velocity

        if event[pygame.K_s] and self.rect.bottom < self.screen_height - self.velocity:
            self.rect.y += self.velocity
        
        if event != [pygame.K_a] or event != [pygame.K_d] or event != [pygame.K_w] or event != [pygame.K_s]:
            self.walking = False
            
        if event[pygame.K_a] or event[pygame.K_d] or event[pygame.K_w] or event[pygame.K_s]:
            self.walking = True

        if self.number_of_updates_made % 7 == 0:
            if self.Step_counter == 7:
                self.Step_counter = 0
            self.Step_counter += 1
        self.number_of_updates_made += 1


class Aliens(pygame.sprite.Sprite):
    def __init__(self, width, height, screen_width, screen_height, image_list, level, boss_or_not, health, power):
        pygame.sprite.Sprite.__init__(self)
        # Creating lists of all possible spawn locations
        Spawn_left = [-width, random.randint(0,screen_height - height -5)]
        Spawn_right = [screen_width + width, random.randint(0,screen_height - height -5)]
        Spawn_top = [random.randint(0,screen_width - width -5), -height]
        Spawn_bottom = [random.randint(0,screen_width - width -5), screen_height + height]
        # creating a list of lists to be used at various levels
        left_and_right_spawn = [Spawn_left, Spawn_right]
        all_spawn_locations = [Spawn_left, Spawn_right, Spawn_top, Spawn_bottom]
        self.level = level
        self.is_a_boss = boss_or_not
        self.image = pygame.Surface((width,height))
        self.image_list = image_list
        self.image = self.image_list[0]
        self.image.set_colorkey((0, 0, 0))
        self.velocity = 1.5
        self.is_a_boss = boss_or_not
        self.rect = self.image.get_rect()
        self.radius = width/2 # The radius variable will be used to give more accurate collisions between the player and enemies
        self.attacking = False
        self.health = health
        self.power = power
        self.Step_counter = 0
        self.attack_counter = 10
        self.number_of_updates_made = 0
        if level == 1 or level == 2:
            self.rect.x , self.rect.y = Spawn_right
        if level <= 5 and level >2:
            self.rect.x , self.rect.y = random.choice(left_and_right_spawn)
        if level > 5:
            self.rect.x , self.rect.y = random.choice(all_spawn_locations)



    def rotate(self, player_center):
        # rotate logic
        deltaX = player_center[0] - self.rect.x
        deltaY = player_center[1] - self.rect.y
        self.angle = math.atan2(deltaX, deltaY) * 180 / math.pi #pygame has a +180 and a -180 instead of 360

        if self.attacking:
            self.image = self.image_list[self.attack_counter]
        if not self.attacking:
            self.image = self.image_list[self.Step_counter]

        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.rotate(self.image, self.angle) 
    

    def check_if_attacking(self, player_center):
        '''
        this if statement is being used to see how close the enemies are to the player,
        if the ememies are in range the attacking variable is changed to confirm they are in attacking distance
        note this could also potentially be done by collision detection...
        (drawing a bigger circle around the player (wont be seen by user)to check if they are in range)
        '''
        if (self.rect.centerx <= player_center[0] + 100 and self.rect.centerx >= player_center[0] - 100)\
                and (self.rect.centery <= player_center[1] + 100 and self.rect.centery >= player_center[1] - 100):
                self.attacking = True
        #if the enemies are not in range stated above the state of attacking is turned to false
        else:
            self.attacking = False


    def update(self, player_center, Blast_back_active):
        self.rotate(player_center)
        self.check_if_attacking(player_center)

        self.position = pygame.math.Vector2(self.rect.x, self.rect.y)
        self.direction = pygame.math.Vector2(player_center) - self .position
        self.direction = self.direction.normalize()

        if Blast_back_active:
            self.position -= self.direction * self.velocity
            self.rect.x, self.rect.y = (round(self.position.x), round(self.position.y))
            
        if not Blast_back_active:
            self.position += self.direction * self.velocity
            self.rect.x, self.rect.y = (round(self.position.x), round(self.position.y))

        if self.number_of_updates_made % 7 == 0:
            if self.Step_counter == 9:
                self.Step_counter = 0
            if self.attack_counter == 17:
                self.attack_counter = 10
            self.Step_counter += 1
            self.attack_counter += 1
        self.number_of_updates_made +=1


class Projectiles(pygame.sprite.Sprite):
    def __init__(self, x, y, mouse_x, mouse_y, image, screen_width, screen_height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,30))
        self.image = image
        self.image.set_colorkey((0, 0, 0))
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = 10
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.position = pygame.math.Vector2(self.rect.x, self.rect.y)
        self.direction = pygame.math.Vector2(self.mouse_x,self.mouse_y) - self .position
        self.direction = self.direction.normalize()


    def update(self): 
        self.position += self.direction * self.velocity
        self.rect.x, self.rect.y = (round(self.position.x), round(self.position.y))
        # an if statement is being used to check if the bullet leaves the screen if it does the bullet is removed
        if self.rect.x == self.screen_width or self.rect.x == 0 or \
            self.rect.y == self.screen_height or self.rect.y == 0:
            self.kill()

