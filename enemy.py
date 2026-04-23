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
        self.rect.y = random.randrange(-300, -100)

        #Movimientos
        self.velocidad_x = random.randrange(-3,5)
        while self.velocidad_x == 0: # Si sale 0, tira el dado de nuevo
            self.velocidad_x = random.randrange(-3, 5)
        self.velocidad_y = random.randrange(2,10)

    def update(self):
        # 1. Aplicamos el movimiento
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        # 2. EL REGENERADOR (Teletransporte)
        # Si la parte superior del OVNI pasa el fondo de la pantalla
        if self.rect.top > ALTO:
            self.rect.x = random.randrange(ANCHO - self.rect.width)
            self.rect.y = random.randrange(-150, -50)
            # Asignamos nuevas velocidades para que no se queden en 0
            self.velocidad_y = random.randrange(2, 10) 
            self.velocidad_x = random.randrange(-3, 5)
            
            while self.velocidad_x == 0: # Evitamos que el nuevo respawn sea tieso
                self.velocidad_x = random.randrange(-3, 5)

        # 3. LÍMITES LATERALES (Solo rebote en los lados)
        # Esto reemplaza tus antiguos "if self.rect.left < 0" etc.
        if self.rect.left < 0:
            self.rect.left = 0 
            self.velocidad_x *= -1 
        elif self.rect.right > ANCHO:
            self.rect.right = ANCHO
            self.velocidad_x *= -1












