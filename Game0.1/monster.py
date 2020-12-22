import pygame
import random
from base_object import Base_Object

class Monster(Base_Object):

    def __init__(self, game, screen):
        super().__init__(game, screen)

        self.health = 100
        self.max_health = 100
        self.attack = 0.5
        self.image = pygame.image.load("assets/mechant.png")
        self.image = pygame.transform.scale(self.image, (90, 90))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0,300)
        self.rect.y = 300
        self.velocity = random.randint(1, 4)
        self.direction = 1
        self.spawn()
        self.clock = 0
        self.walkCount = 0
        self.image_number = 0

        self.walkRight = [pygame.image.load('assets/Zombie/Zombie1/animation/Walk1.png'),
                          pygame.image.load('assets/Zombie/Zombie1/animation/Walk2.png'),
                          pygame.image.load('assets/Zombie/Zombie1/animation/Walk3.png'),
                          pygame.image.load('assets/Zombie/Zombie1/animation/Walk4.png'),
                          pygame.image.load('assets/Zombie/Zombie1/animation/Walk5.png'),
                          pygame.image.load('assets/Zombie/Zombie1/animation/Walk6.png')]


        self.walkLeft = [0,0,0,0,0,0]
        for i in range(0,6):
            self.walkLeft[i] = pygame.transform.flip(self.walkRight[i], True, False)

        self.char = pygame.image.load('assets/Zombie/Zombie1/animation/Idle1.png')

        for i in range(0,6):
            #self.walkLeft[i] = pygame.transform.scale(self.walkLeft[i], (self.rect.width, self.rect.height))
            self.walkLeft[i] = pygame.transform.rotozoom(self.walkLeft[i], 0, 0.3)
            self.walkRight[i] = pygame.transform.rotozoom(self.walkRight[i], 0, 0.3)
            #self.walkRight[i] = pygame.transform.scale(self.walkRight[i], (self.rect.width, self.rect.height))

    def Damage(self, amount, player):
        #infliger les dégats
        self.health -= amount

        #verifier si PV<= 0 ?

        if self.health <= 0:
            #On ne le supprime pas, on le fait respawn
            self.spawn()
            player.kills += 1

    def spawn(self):
        self.rect.x = 1200
        self.rect.y = self.screen.get_height() - 450
        self.velocity = random.randint(1, 4)
        self.health = self.max_health

    def Update_Health_Bar(self, surface):

        #définir la position de la jauge ainsi que la largeur/epaisseur
        #dessiner notre barre de vie
        pygame.draw.rect(surface,(60, 63, 60), [self.rect.x + 10 - self.game.cameraX, self.rect.y - 15 - self.game.cameraY, self.max_health, 5])
        pygame.draw.rect(surface, (111, 210, 46), [self.rect.x + 10 - self.game.cameraX, self.rect.y - 15 - self.game.cameraY, self.health, 5])

    def orient(self):
        # Orients itself toward the player
        if self.game.player.rect.x - self.rect.x > 0:
            self.direction = 1
        else:
            self.direction = -1

    def forward(self):
        # le deplacement ne sqe efait que ssi pas de collision mais il faut nécéssairement faire avec un groupe
        if not self.game.Check_Collision(self, self.game.all_players):
            self.rect.x += self.velocity * self.direction
        # si le monstre est en collision avec le joueur
        else:
        # on inflige les dégats au joueur
            self.game.player.Damage(self.attack)


    def show(self):
        # We have 6 images for our walking animation, I want to show the same image for 3 frames
        # so I use the number 18 as an upper bound for walkCount  images shown
        # 3 times each animation.
        self.clock += 1

        # Each 10 frames, change image
        if self.clock % 10 == 0:
            self.walkCount += 1

        # reset counter
        if self.walkCount > 4:
            self.walkCount = 0


        if self.direction == -1:  # If we are facing left

            self.screen.blit(self.walkLeft[self.walkCount], (self.rect.x - self.game.cameraX, self.rect.y - self.game.cameraY))  # We integer divide walkCount by 3 to ensure each
            self.game.walkCount += 1  # image is shown 3 times every animation
        elif self.direction == 1:

            self.screen.blit(self.walkRight[self.walkCount], (self.rect.x - self.game.cameraX, self.rect.y - self.game.cameraY))
            self.game.walkCount += 1
        #else:
            #self.screen.blit(self.char, (x, y))  # If the character is standing still

