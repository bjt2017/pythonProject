import pygame

# Initialisation de Pygame
pygame.init()

# Définition des couleurs RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Définition de la taille de la fenêtre
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Création de la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)


triangle_speed = 5

class Triange(pygame.sprite.Sprite):
    def __init__(self,x,y,list):
        super(Triange, self).__init__()
        self.triangle = pygame.Surface((100, 100), pygame.SRCALPHA)
        pygame.draw.polygon(self.triangle, RED, list)
        self.rect = self.triangle.get_rect(center=(x,y))
        self.mask = pygame.mask.from_surface(self.triangle)
    def colision(self,signe,signe2):
        # Déplacer le sprite de triangle
        self.rect.move_ip(signe, signe2)
        if (pygame.sprite.spritecollide(self, triangle_group, False, pygame.sprite.collide_mask)):
            self.rect.move_ip(-signe, -signe2)
        else:
            self.rect.move_ip(signe*triangle_speed -signe, signe2*triangle_speed -signe2)


        if pygame.sprite.spritecollide(triangle1, triangle_group, False, pygame.sprite.collide_mask):
            self.rect.move_ip(triangle_speed*(-signe), triangle_speed*(-signe2))

            for i in range(1, triangle_speed + 2):
                if pygame.sprite.spritecollide(triangle1, triangle_group, False, pygame.sprite.collide_mask):
                    self.rect.move_ip(-signe, -signe2)
                    break
                self.rect.move_ip(signe, signe2)


    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.colision(-1,0)
        elif keys[pygame.K_RIGHT]:
            self.colision(1,0)
        if keys[pygame.K_UP]:
            self.colision(0,-1)
        elif keys[pygame.K_DOWN]:
            self.colision(0,1)



triangle_group = pygame.sprite.Group()
triangle1 = Triange(SCREEN_WIDTH/2-50, SCREEN_HEIGHT/2,[(0, 100), (50, 0), (100, 100)])
triangle2 = Triange(200, 100,[(0, 100), (50, 0), (100, 100)])
carre = Triange(100, 100,[(0, 0), (16, 0), (16, 16)])


triangle_group.add(triangle2)
triangle_group.add(carre)
# Boucle principale
running = True
while running:
    triangle1.update()
    clock = pygame.time.Clock()
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Gestion des touches fléchées
    keys = pygame.key.get_pressed()


    # Effacement de l'écran
    screen.fill((0, 0, 0, 0))

    # Dessin des triangles
    screen.blit(triangle1.triangle, triangle1.rect)
    screen.blit(triangle2.triangle, triangle2.rect)
    screen.blit(carre.triangle, carre.rect)
    print(triangle1.mask)
    #outline = [(p[0] + triangle2.rect.x, p[1] + triangle2.rect.y) for p in triangle2.mask.outline(every=1)]
    #pygame.draw.lines(screen,(255,0,255),False,outline)

    if(pygame.sprite.spritecollide(triangle1,triangle_group,False,pygame.sprite.collide_mask)):
        print(True)


    # Actualisation de l'affichage
    pygame.display.flip()
    clock.tick(60)

# Fermeture de Pygame
pygame.quit()

