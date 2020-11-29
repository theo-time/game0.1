import pygame


class Box(pygame.sprite.Sprite):

    def __init__(self, game, display, x, y, width, height):
        super().__init__()
        self.game = game
        self.display = display
        self.rect = pygame.Rect(x,y, width, height)
        game.all_boxes.append(self)


    def show(self):
        pygame.draw.rect(self.display, (120,0,0), self.rect)


