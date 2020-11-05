import pygame
from player import Player
#creation d'une classe pour représenter le jeu
from monster import Monster

class Game:

    def __init__(self):
        #definir si le jeu a commencé ou non
        self.is_playing = False
        #generer notre joueur quand on lance une game
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)
        #groupe de monstre
        self.all_monster = pygame.sprite.Group()
        self.pressed = {}

    def start(self):
        self.is_playing = True
        self.spawn_monster()
        self.spawn_monster()
        self.spawn_monster()

    def game_over(self):
        #remise à 0
        self.all_monster = pygame.sprite.Group()
        self.player.health = self.player.max_health
        self.is_playing = False

    def Update(self, screen):
        # appliquer image joueur
        screen.blit(self.player.image, self.player.rect)

        # actualiser la barre de vie du joueur
        self.player.Update_Health_Bar(screen)

        # recuperer les projectiles du joueur
        for Projectile in self.player.all_projectiles:
            Projectile.Move()

        # recupérer les monstres de notre jeu
        for monster in self.all_monster:
            monster.forward()
            monster.Update_Health_Bar(screen)

        # appliquer l'ensemble des images de son groupe de projectiles
        self.player.all_projectiles.draw(screen)

        # appliquer l'ensemble des images de mon grp de monstre
        self.all_monster.draw(screen)

        # verifier si le joueur veut aller de gauche à droite
        if self.pressed.get(pygame.K_RIGHT) and self.player.rect.x < 940:
            self.player.move_right()
        elif self.pressed.get(pygame.K_LEFT) and self.player.rect.x > -30:
            self.player.move_left()
        elif self.pressed.get(pygame.K_DOWN) and self.player.rect.y < 520:
            self.player.move_bottom()
        elif self.pressed.get(pygame.K_UP) and self.player.rect.y > 450:
            self.player.move_up()

    def Check_Collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def spawn_monster(self):
        monster = Monster(self)
        self.all_monster.add(monster)