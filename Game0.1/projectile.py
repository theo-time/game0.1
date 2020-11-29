import pygame

#definition de la class projectile

class Projectile(pygame.sprite.Sprite):

   #Realisation du constructeur de la class
    def __init__(self, player, direction):
        super().__init__()
        self.velocity = direction * 9
        self.player = player
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
            monster.Damage(self.player.attack)

        #verifier et suppr si notre projectile n'est plus présent sur l'ecran
        if self.rect.x > 1080:
            self.Remove()

