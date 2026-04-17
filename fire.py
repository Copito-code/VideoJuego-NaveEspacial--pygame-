import pygame
from math import degrees

# Dimensiones de la ventana
ANCHO = 800
ALTO = 600

# colores por si acaso
NEGRO = (0,0,0)
BLANCO = (255,255,255)
ROJO = (250,0,0)
H_FA2F2F = (250,47,47)
VERDE = (0,255,0)
AZUL = (0,0,255)


class fire(pygame.sprite.Sprite):
    def __init__(self, x,y):

        super().__init__()

        self.image = pygame.image.load("img/misil_nuevo2.png")
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x

    def update(self):
        self.rect.y -= 10

        if self.rect.bottom < 0:
            self.kill
        



