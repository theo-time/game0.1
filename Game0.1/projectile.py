import pygame

#definition de la class projectile

class Projectile(pygame.sprite.Sprite):

   #Realisation du constructeur de la class
    def __init__(self, screen, game, player, direction):
        super().__init__()
        self.screen = screen
        self.game = game
        self.player = player

        self.speed = 50
        self.range = screen.get_width()
        self.firing_point = self.player.rect.x
        self.velocity = direction * self.speed
        self.image = pygame.image.load("assets/cheese.png")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 90
        self.rect.y = player.rect.y + 60
        self.origin_image = self.image
        self.angle = 0


    def Rotate(self):
        #faire tourner le projectile, angle=vitesse
        self.angle += 14
        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)
    #methode pour suppr les projectiles

    def Remove(self):
        self.player.all_projectiles.remove(self)

    #méthode pour le mouvement du projectile

    def Move(self):
        self.rect.x += self.velocity
        self.Rotate()

        #verifier si ke projectile entre en collision avec un monstre
        for monster in self.player.game.Check_Collision(self, self.player.game.all_monster):
            self.Remove()
            #infliger degats
            monster.Damage(self.player.attack, self.player)

        #verifier et suppr si notre projectile est à la fin de sa range
        if abs(self.rect.x - self.firing_point) > self.range:
            self.Remove()



    def show(self):
        self.screen.blit(self.image, (self.rect.x - self.game.cameraX, self.rect.y - self.game.cameraY))
