import pygame
import sys

from game import Game

from box import Box

pygame.init()

font = pygame.font.Font(None, 30)
clock = pygame.time.Clock()

# this has been committed

#Fenetre menu principal
pygame.display.set_caption("PaulGame")
screen = pygame.display.set_mode((1080, 720))

#import du bg
background = pygame.image.load('assets/background.jpg')

#import de la bannière
banner = pygame.image.load('assets/realbanner.png')
banner = pygame.transform.scale(banner,(600, 300))
banner_rect = banner.get_rect()
banner_rect.x = screen.get_width() / 4

#import charger notre bouton pour lancer la partie
play_button = pygame.image.load('assets/button.png')
play_button = pygame.transform.scale(play_button, (400, 150))
play_button_rect = play_button.get_rect()
play_button_rect.x = screen.get_width() / 3
play_button_rect.y = screen.get_width() / 3.9

#redimensionnement de l'image
background = pygame.transform.scale(background,(1200,800))

#charger notre jeu
game = Game(screen)

# création des boîtes
box1 = Box(game,screen, 0, screen.get_height() - 50, 10000, 50)
box2 = Box(game,screen, 400, screen.get_height() - 230, screen.get_width(), 50)
box3 = Box(game,screen, 50, screen.get_height() - 300, 200, 50)

running = True



def Text(text, x, y):
    msg = font.render(text, True, pygame.Color('white'))
    screen.blit(msg, (x, y))


mur = pygame.Surface((25, 25))
mur.fill((0,0,0))

niveau = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


def dessiner_niveau(surface, niveau):
    """Dessine le niveau sur la surface donnée.

    Utilise la surface `mur` pour dessiner les cases de valeur 1
    """
    for j, ligne in enumerate(niveau):
        for i, case in enumerate(ligne):
            if case == 1:
                surface.blit(mur, (i * 25, j * 25))


#Boucle tant running = vrai
while running:
    #appliquer Bg du jeu
    #temp_surf = screen.copy
    #screen.fill( (0, 0, 0))  # here, you can fill the screen with whatever you want to take the place of what was there before
    #screen.blit(temp_surf, (20, 20))
    screen.blit(background,(0,-100))

    #verifier si l jeu a débuté
    if game.is_playing:
        #declencher les instructions de la partie
        game.Update(screen)

        # Affichage du jeu
        game.render()

        # Handling and displaying time
        clock.tick(30)
        game.time += 1

        # Time Display
        Text("FPS : " + str(int(clock.get_fps())), 50, 50)

        # Kills display
        Text("Kills : " + str(game.player.kills), 50, 100)

        # Projectiles length display
        Text(" Projectiles :" + str(len(game.player.all_projectiles)), 50, 150)

        # Number of Zombies
        Text("Zombies : " + str(len(game.all_monster)), 50, 200)

        # move camera
        mousex, mouseY = pygame.mouse.get_pos()
        #game.cameraX = mousex

    #verifier si le jeu n'a pas commencé puis ajouter l'ecran de bienvenu
    else:
        screen.blit(banner, banner_rect)
        screen.blit(play_button, play_button_rect)



    #dessiner_niveau(screen, niveau)

    #maj de l'écran
    pygame.display.flip()

    #si le joueur ferme la fenetre + verif des events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("Fermeture du jeu")
        #detecter si un joueur lache une touche du clavier
        elif event.type == pygame.KEYDOWN:
           game.pressed[event.key] = True
           #detecter si la touche espace est désenclenchée pour arrêter le tir
           if event.key == pygame.K_SPACE:
               game.player.isFiring = True

        elif event.type == pygame.KEYUP:

           game.pressed[event.key] = False
           #detecter si la touche espace est désenclenchée pour arrêter le tir
           if event.key == pygame.K_SPACE:
               game.player.isFiring = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            #verification pour savoir s'il y a clique sur le bouton
            if play_button_rect.collidepoint(event.pos):
                #mettre le jeu en mode run
                game.start()






def bloque_sur_collision(old_pos, new_pos, vx, vy, blocks):
    """Tente de déplacer old_pos vers new_pos dans le niveau.

    S'il y a collision avec les éléments du niveau, new_pos sera ajusté pour
    être adjacent aux éléments avec lesquels il entre en collision.
    On passe également en argument les vitesses `vx` et `vy`.

    La fonction retourne la position modifiée pour new_pos ainsi que les
    vitesses modifiées selon les éventuelles collisions.
    """
    old_rect = pygame.Rect(old_pos, (25, 25))
    new_rect = pygame.Rect(new_pos, (25, 25))
    i, j = from_coord_to_grid(new_pos)


    for block in blocks:
        if not new_rect.colliderect(block):
            continue

        dx_correction, dy_correction = compute_penetration(block, old_rect, new_rect)
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

    # Deuxième phase. On teste à présent les distances de pénétrations pour
    # les blocks qui en possédaient sur les 2 axes.
    for block in collide_later:
        dx_correction, dy_correction = compute_penetration(block, old_rect, new_rect)
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
    return x, y, vx, vy

