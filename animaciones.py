import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, centro, lista_frames):
        super().__init__()
        self.frames = lista_frames
        self.frames_actual = 0
        self.image = self.frames[self.frames_actual]
        self.rect = self.image.get_rect()
        self.rect.center = centro


        #Control de velocidad de la animacion
        self.ultimo_update = pygame.time.get_ticks()
        self.ms_por_frame = 80 #Cuanto menor el numero, mas rapida la explosion

    def update(self):
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_update > self.ms_por_frame:
            self.ultimo_update = ahora
            self.frames_actual += 1

            #Si llegamos al final de la lista, eliminamos el sprite
            if self.frames_actual >= len(self.frames):
                self.kill()

            else:
                self.image = self.frames[self.frames_actual]
        
