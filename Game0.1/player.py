import pygame

import box

from base_object import Base_Object
from projectile import Projectile

#creation de la class joueur

class Player(Base_Object):

    def __init__(self, game, screen):
        super().__init__(game, screen)

        # Life
        self.health = 100
        self.max_health = 100

        # Moving
        self.velocity = 10
        self.direction = 1

        # Attack
        self.attack = 10
        self.all_projectiles = pygame.sprite.Group()
        self.isFiring = False


    def Damage(self, amount):
        if self.health - amount > amount:
         self.health -= amount
        else:
            # si le joueur est à 0PV
            self.game.game_over()

    def Update_Health_Bar(self, surface):
        pygame.draw.rect(surface,(60, 63, 60), [self.rect.x + 20, self.rect.y - 5, self.max_health, 5])
        pygame.draw.rect(surface, (111, 210, 46), [self.rect.x + 20, self.rect.y - 5, self.health, 5])

    def lauch_projectile(self):
        #creation d'une nouvelle instance de la class projectile
        if self.isFiring:
            self.all_projectiles.add(Projectile(self,self.direction))

    def move_right(self):
        #if not self.game.Check_Collision(self, self.game.all_monster):
        #self.rect.x += self.velocity
        self.acc.x = (self.velocity - self.speed.x)
        print(self.speed.x ,self.velocity)
        self.direction = 1
        self.image = self.image_right


    def move_left(self):
        #self.rect.x -= self.velocity
        self.acc.x = ( -self.velocity - self.speed.x)
        self.direction = -1
        print(self.acc.x ,self.speed.x ,-self.velocity)
        self.image = pygame.transform.flip(self.image, True, False)
        self.image = self.image_left

    def move_bottom(self):
        self.rect.y += 50

    def move_up(self):
        self.acc.y -= 20

    def stop(self):
        self.acc.x = -self.speed.x

    def move(self):
        # Walk
        #if self.onGround:
        if self.game.pressed.get(pygame.K_RIGHT) and self.rect.x < 940:
            self.move_right()
        elif self.game.pressed.get(pygame.K_LEFT) and self.rect.x > -30:
            self.move_left()
        else:
            if self.onGround:
                self.stop()

        # Jump
        #if self.game.pressed.get(pygame.K_DOWN):
            #self.move_bottom()
        if self.game.pressed.get(pygame.K_UP) and self.onGround :
            self.move_up()

    def collision_detection(self):
        #monster = self.game.Check_Collision(self, self.game.all_monster)
        i = self.rect.collidelist(self.game.all_boxes)
        if i >= 0:
            return self.game.all_boxes[i]
        else:
            return False

