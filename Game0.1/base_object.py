import pygame

class Base_Object(pygame.sprite.Sprite):


    def __init__(self, game, screen):
        super().__init__()
        game.all_objects.append(self)
        self.game = game
        self.screen = screen

        # Image
        self.image_right = pygame.image.load('assets/playercow.png')
        self.image_left = pygame.transform.flip(self.image_right, True, False)
        self.image = self.image_right

        # Physics engine
        self.rect = self.image.get_rect()
        self.old_rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 0
        self.onGround = False
        self.gAcc = 1
        self.maxG = 10
        self.speed = pygame.math.Vector2(0,0)
        self.acc = pygame.math.Vector2(0,0)

    # Falls on the ground with gAcc
    def gravity(self):
        self.acc.y += self.gAcc

    #
    def update(self):
        # Update speed
        #if not (self.game.Check_Collision(self, self.game.all_monster) or self.rect.collidelist(self.game.all_boxes) >= 0) :
        self.speed.x += self.acc.x
        self.speed.y += min(self.maxG ,self.acc.y)

        # Record past rect
        self.old_rect = self.rect.copy()

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

        self.onGround = redirection[4]

        # Reset acceleration
        self.acc.x = 0
        self.acc.y = 0

