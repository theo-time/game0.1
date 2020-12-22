import pygame


class Box(pygame.sprite.Sprite):

    def __init__(self, game, display, width):
        super().__init__()
        self.game = game
        self.display = display
        self.rect = pygame.Rect(x,y, width, width)
        game.all_blocks.append(self)


    def show(self):
        pygame.draw.rect(self.display, (120,0,0), pygame.Rect(self.rect.x - self.game.cameraX,
                                                              self.rect.y - self.game.cameraY,
                                                              self.rect.width,
                                                              self.rect.height))