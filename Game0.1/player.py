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
        self.isFiring = False

        # Stats
        self.kills = 0

        # initialise on gun
        self.weapon = Weapon(game, screen, self, "gun", 30, 30, 100)


    def Damage(self, amount):
        if self.health - amount > amount:
         self.health -= amount
        else:
            # si le joueur est à 0PV
            self.game.game_over()

    def Update_Health_Bar(self, surface):
        pygame.draw.rect(surface,(60, 63, 60), [self.rect.x + 20 - self.game.cameraX, self.rect.y - 5 - self.game.cameraY, self.max_health, 5])
        pygame.draw.rect(surface, (111, 210, 46), [self.rect.x + 20 - self.game.cameraX, self.rect.y - 5  - self.game.cameraY, self.health, 5])

    def attack(self):
        # lancement d'un projectile toute les x frames
        self.weapon.fire()

    def move_right(self):
        #if not self.game.Check_Collision(self, self.game.all_monster):
        #self.rect.x += self.velocity
        self.acc.x = (self.velocity - self.speed.x)
        self.direction = 1
        self.image = self.image_right


    def move_left(self):
        #self.rect.x -= self.velocity
        self.acc.x = ( -self.velocity - self.speed.x)
        self.direction = -1
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
        if self.game.pressed.get(pygame.K_RIGHT):
            self.move_right()
        elif self.game.pressed.get(pygame.K_LEFT):
            self.move_left()
        else:
            if self.onGround:
                self.stop()

        if self.rect.x - self.game.cameraX > self.screen.get_width() * 1/2 :
            self.game.cameraX += 10

        if self.rect.x - self.game.cameraX < self.screen.get_width() * 1/2 :
            self.game.cameraX -= 10

        # Jump
        #if self.game.pressed.get(pygame.K_DOWN):
            #self.move_bottom()
        if self.game.pressed.get(pygame.K_UP) and self.onGround :
            self.move_up()

        # Dies if falls
        if self.rect.y > self.screen.get_height():
            self.game.game_over()

    def collision_detection(self):
        #monster = self.game.Check_Collision(self, self.game.all_monster)
        i = self.rect.collidelist(self.game.all_boxes)
        if i >= 0:
            return self.game.all_boxes[i]
        else:
            return False

    def show(self):
        self.screen.blit(self.image, ( self.rect.x - self.game.cameraX, self.rect.y - self.game.cameraY))

class Weapon():

    def __init__(self, game, screen, player, name, damage, rateOfFire, range):
        self.game = game
        self.screen = screen
        self.player = player
        self.name = name
        self.damage = damage
        self.rateOfFire = rateOfFire
        self.range = range

        self.clock = 0

        self.all_projectiles = pygame.sprite.Group()

    def fire(self):
        if(self.player.isFiring):
            print(self.clock)
            if(self.clock % self.rateOfFire == 0):
                self.game.all_projectiles.add(Projectile(self.screen, self.game, self.player, self.player.direction, self.damage))

            self.clock += 1
        else:
            self.clock = 0# TODO : a bit moins bourrin svp
            print("reInit")

        # TODO: make all classes inherit from one objects which bears the reference to screen and game
