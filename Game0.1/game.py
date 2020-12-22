import pygame

from player import Player
#creation d'une classe pour représenter le jeu
from monster import Monster

class Game:

    def __init__(self, screen):

        # Caméra
        self.cameraX = 0
        self.cameraY = 0

        #definir si le jeu a commencé ou non
        self.is_playing = False
        self.all_objects = []
        self.all_boxes = []

        #generer notre joueur quand on lance une game
        self.all_players = pygame.sprite.Group()
        self.player = Player(self, screen)
        self.all_players.add(self.player)
        self.screen = screen

        #groupe de monstre
        self.all_monster = pygame.sprite.Group()


        self.pressed = {}
        self.walkCount = 0
        self.time = 0

    def start(self):
        self.is_playing = True

        self.spawn_monster()
        self.spawn_monster()
        self.spawn_monster()
        self.spawn_monster()
        self.spawn_monster()
        self.spawn_monster()


    def game_over(self):
        #remise à 0
        self.all_monster = pygame.sprite.Group()
        self.player.health = self.player.max_health
        self.is_playing = False

    def Update(self, screen):

        # recuperer les projectiles du joueur
        for Projectile in self.player.all_projectiles:
            Projectile.Move()

        # Each 50 frame, create new Zomb
        if self.time % 50 == 0:
            self.spawn_monster()

        # recupérer les monstres de notre jeu
        for monster in self.all_monster:
            monster.orient()
            monster.forward()
            monster.Update_Health_Bar(screen)
            monster.show()

        # appliquer l'ensemble des images de son groupe de projectiles
        for projectile in self.player.all_projectiles:
            projectile.show()

        self.player.move()
        self.player.lauch_projectile()

        #Appliquer la gravité
        for object in self.all_objects:
            object.gravity()
            object.update()

    def Check_Collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)


    def compute_penetration(self, block, old_rect, new_rect):
        """Calcule la distance de pénétration du `new_rect` dans le `block` donné.

        `block`, `old_rect` et `new_rect` sont des pygame.Rect.
        Retourne les distances `dx_correction` et `dy_correction`.
        """
        #print(block, old_rect, new_rect)
        dx_correction = dy_correction = 0.0
        if old_rect.bottom <= block.top < new_rect.bottom:
            dy_correction = block.top - new_rect.bottom
        elif old_rect.top >= block.bottom > new_rect.top:
            dy_correction = block.bottom - new_rect.top

        if old_rect.right <= block.left < new_rect.right:
            dx_correction = block.left - new_rect.right
        elif old_rect.left >= block.right > new_rect.left:
            dx_correction = block.right - new_rect.left
        return dx_correction, dy_correction

    def bloque_collision(self, old_rect, new_rect, vx, vy, blocks):
        """Tente de déplacer old_pos vers new_pos dans le niveau.

        S'il y a collision avec les éléments du niveau, new_pos sera ajusté pour
        être adjacent aux éléments avec lesquels il entre en collision.
        On passe également en argument les vitesses `vx` et `vy`.

        La fonction retourne la position modifiée pour new_pos ainsi que les
        vitesses modifiées selon les éventuelles collisions.
        """
        #old_rect = pygame.Rect(old_pos, (25, 25))
        #new_rect = pygame.Rect(new_pos, (25, 25))
        #i, j = from_coord_to_grid(new_pos)
        collide_later = list()
        onGround = False

        for block in blocks:
            if not new_rect.colliderect(block):
                continue

            dx_correction, dy_correction = self.compute_penetration(block.rect, old_rect, new_rect)
            # Dans cette première phase, on n'ajuste que les pénétrations sur un
            # seul axe.
            if dx_correction == 0.0:
                new_rect.top += dy_correction
                vy = 0.0
            elif dy_correction == 0.0:
                new_rect.left += dx_correction
                vx = 0.0
            else:
                collide_later.append(block)
            if dy_correction < 0:
                onGround = True

        # Deuxième phase. On teste à présent les distances de pénétrations pour
        # les blocks qui en possédaient sur les 2 axes.
        for block in collide_later:
            dx_correction, dy_correction = self.compute_penetration(block.rect, old_rect, new_rect)
            if dx_correction == dy_correction == 0.0:
                # Finalement plus de pénétration. Le new_rect a bougé précédemment
                # lors d'une résolution de collision
                continue
            if abs(dx_correction) < abs(dy_correction):
                # Faire la correction que sur l'axe X (plus bas)
                dy_correction = 0.0
            elif abs(dy_correction) < abs(dx_correction):
                # Faire la correction que sur l'axe Y (plus bas)
                dx_correction = 0.0
            if dy_correction != 0.0:
                new_rect.top += dy_correction
                vy = 0.0
            elif dx_correction != 0.0:
                new_rect.left += dx_correction
                vx = 0.0



        x, y = new_rect.topleft
        return x, y, vx, vy, onGround

    def render(self):
        # appliquer image joueur
        self.player.show()

        # actualiser la barre de vie du joueur
        self.player.Update_Health_Bar(self.screen)
        # Afficher les boîtes
        for box in self.all_boxes :
            box.show()

    def spawn_monster(self):
        monster = Monster(self, self.screen)
        self.all_monster.add(monster)


