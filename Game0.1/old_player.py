import pygame

import box

from projectile import Projectile

#creation de la class joueur

class Player(pygame.sprite.Sprite):

    def __init__(self, game, screen):
        super().__init__()
        self.game = game
        self.screen = screen
        self.health = 100
        self.max_health = 100
        self.attack = 10

        self.velocity = 10
        self.speed = pygame.math.Vector2(0,0)
        self.acc = pygame.math.Vector2(0,0)
        self.all_projectiles = pygame.sprite.Group()
        self.image_right = pygame.image.load('assets/playercow.png')
        self.image_left = pygame.transform.flip(self.image_right, True, False)
        self.image = self.image_right
        self.rect = self.image.get_rect()
        self.old_rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 0
        self.onGround = False
        self.gAcc = 1
        self.maxG = 10
        self.direction = 1
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

    def update(self):
        # Update speed
        #if not (self.game.Check_Collision(self, self.game.all_monster) or self.rect.collidelist(self.game.all_boxes) >= 0) :
        self.speed.x += self.acc.x
        self.speed.y += min(self.maxG ,self.acc.y)

        # Record past rect
        self.old_rect = self.rect.copy()
        print("past rect", self.old_rect, self.game.time)

        # Update position
        self.rect.x += self.speed.x
        self.rect.y += self.speed.y

        redirection = self.game.bloque_collision(self.old_rect, self.rect, self.speed.x, self.speed.y, self.game.all_boxes)

        # Update position
        self.rect.x = redirection[0]
        self.rect.y = redirection[1]

        # Reset speed on 0 if collision
        self.speed.x = redirection[2]
        self.speed.y = redirection[3]

        #collide_obj = self.collision_detection()

        # Prevent colliding
        #if collide_obj:
        #    print(collide_obj.rect, self.past_rect, self.rect, self.game.time)
#
 #           dy_correction, dx_correction = self.game.compute_penetration(collide_obj.rect, self.past_rect, self.rect)
  #          self.rect.top += dy_correction
   ##         self.rect.left += dx_correction
     #       print(dx_correction)
            #breakpoint()
            #pygame.draw.rect(self.screen, (0,0,0), self.rect)

        self.onGround = redirection[4]

        print("*******************")
        print("POS :",self.rect.x,self.rect.y)
        print("SPEED :",self.speed.x,self.speed.y)
        print("ACC :",self.acc.x,self.acc.y)
        print("OnGround : ", self.onGround)
        print("*******************")

        # Reset acceleration
        self.acc.x = 0
        self.acc.y = 0



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

    def gravity(self):
        self.acc.y += self.gAcc
       #if (self.game.Check_Collision(self, self.game.all_monster) or self.rect.collidelist(self.game.all_boxes) >= 0):
            #if self.speed.y > 0:
                #print(self.rect.collidelist(self.game.all_boxes))
                #print("ONGROUND : ", self.onGround)
                 # Only stops you if falling
                #self.onGround = True
                #self.speed.y = 0
       #else:
           #self.onGround = False
        #self.acc.y += self.gAcc # how fast player falls
           #print("ONGROUND : ", self.onGround)
