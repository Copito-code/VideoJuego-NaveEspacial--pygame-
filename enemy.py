import pygame
import random

ANCHO = 800
ALTO = 600

# colores por si acaso
NEGRO = (0,0,0)
BLANCO = (255,255,255)
ROJO = (250,0,0)
H_FA2F2F = (250,47,47)
VERDE = (0,255,0)
AZUL = (0,0,255)

#clase enemigo 

class enemy(pygame.sprite.Sprite):
    def __init__(self):
    
        #Heredamos la variable de la clase sprite
        super().__init__()

        self.image = pygame.image.load("img/ovni_enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (450, 500)

        #Aparaicion random
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = random.randrange(300 - self.rect.height)

        #Movimientos
        self.velocidad_x = random.randrange(1,10)
        self.velocidad_y = random.randrange(1,10)

    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y


        #Limite izq y derh
        if self.rect.left < 0:
            self.velocidad_x += 1

        if self.rect.right > ANCHO:
            self.velocidad_x -= 1

        #Limite abajo y arriba
        if self.rect.bottom > ALTO:
            self.velocidad_y -=1

        if self.rect.top < 0:
            self.velocidad_y += 1
        










