import pygame
from projectile import Projectile

#creation de la class joueur

class Player(pygame.sprite.Sprite):

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.velocity = 10
        self.all_projectiles = pygame.sprite.Group()
        self.image = pygame.image.load('assets/playercow.png')
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 450

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
        self.all_projectiles.add(Projectile(self))

    def move_right(self):
        if not self.game.Check_Collision(self, self.game.all_monster):
            self.rect.x += self.velocity

    def move_left(self):
        self.rect.x -= self.velocity

    def move_bottom(self):
        self.rect.y += 5

    def move_up(self):
        self.rect.y -= 5