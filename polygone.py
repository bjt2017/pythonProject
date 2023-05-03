import pygame
import pyscroll
class Polygone(pygame.sprite.Sprite):
    def __init__(self,x,y,tx,ty,list):
        super(Polygone, self).__init__()
        self.surface = pygame.Surface((tx, ty), pygame.SRCALPHA)
        pygame.draw.polygon(self.surface, (255,0,0), list)
        self.rect = self.surface.get_rect(topleft=(x,y))
        self.mask = pygame.mask.from_surface(self.surface)

