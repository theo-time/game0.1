import pygame
from game import Game
pygame.init()

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
game = Game()

running = True

#Boucle tant running = vrai
while running:
    #appliquer Bg du jeu
    screen.blit(background,(0,-100))

    #verifier si l jeu a débuté
    if game.is_playing:
        #declencher les instructions de la partie
        game.Update(screen)

    #verifier si le jeu n'a pas commencé puis ajouter l'ecran de bienvenu
    else:
        screen.blit(banner, banner_rect)
        screen.blit(play_button, play_button_rect)
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

           #detecter si la touche espace est enc lenchée pour lancer le projectile
           if event.key == pygame.K_SPACE:
               game.player.lauch_projectile()

        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            #verification pour savoir s'il y a clique sur le bouton
            if play_button_rect.collidepoint(event.pos):
                #mettre le jeu en mode run
                game.start()

