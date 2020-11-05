import pygame
import random
class Monster(pygame.sprite.Sprite):

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 0.5
        self.image = pygame.image.load("assets/mechant.png")
        self.image = pygame.transform.scale(self.image, (90, 90))
        self.rect = self.image.get_rect()
        self.rect.x = 1000 + random.randint(0, 300)
        self.rect.y = 450 + random.randint(-10, 100)
        self.velocity = random.randint(1, 4)

    def Damage(self, amount):
        #infliger les dégats
        self.health -= amount

        #verifier si PV<= 0 ?

        if self.health <= 0:
            #On ne le supprime pas, on le fait respawn
            self.rect.x = 1000 + random.randint(0, 300)
            self.rect.y = 450 + random.randint(-10, 100)
            self.velocity = random.randint(1, 4)
            self.health = self.max_health

    def Update_Health_Bar(self, surface):

        #définir la position de la jauge ainsi que la largeur/epaisseur
        #dessiner notre barre de vie
        pygame.draw.rect(surface,(60, 63, 60), [self.rect.x + 10, self.rect.y - 15, self.max_health, 5])
        pygame.draw.rect(surface, (111, 210, 46), [self.rect.x + 10, self.rect.y - 15, self.health, 5])

    def forward(self):
        # le deplacement ne sqe efait que ssi pas de collision mais il faut nécéssairement faire avec un groupe
        if not self.game.Check_Collision(self, self.game.all_players):
            self.rect.x -= self.velocity
        # si le monstre est en collision avec le joueur
        else:
        # on inflige les dégats au joueur
            self.game.player.Damage(self.attack)