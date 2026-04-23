import menu

from asyncio import events
import pygame 
import re
from enemy import enemy
from fire import fire
import random

# Dimensiones de ventana
ANCHO = 800
ALTO = 600
#Fotogramas
FPS = 60
#Fuentes
consolas = pygame.font.match_font("consolas")
time = pygame.font.match_font("times")
arial = pygame.font.match_font("arial")
courier = pygame.font.match_font("courier")




# colores por si acaso
NEGRO = (0,0,0)
BLANCO = (255,255,255)
ROJO = (250,0,0)
H_FA2F2F = (250,47,47)
VERDE = (0,255,0)
AZUL = (0,0,255)




# Clase jugador
class player(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()
        #Se cargo la imagen
        self.image_original = pygame.image.load("img/cohete(nuevo).png")
        self.image = self.image_original.copy()
        #Seleccionamos el area del sprite (rectangulo)
        self.rect = self.image.get_rect()
        #Centramos rectangul
        self.rect.center = (400, 540)

        #Variables de control de daño para efectos
        self.daño_timer = 0
        self.sacudida_offset = [0,0]

        #Asignar velocidad
        self.velocidad_x = 0
        self.velocidad_y = 0

        # cadencia de disparos
        self.cadencia = 200
        # obtener el ultimo dispara
        self.ultimate = pygame.time.get_ticks()


    def recibir_daño(self):
        #Activamos el timer (ej. 300 milisegundos de efecto)
        self.daño_timer = pygame.time.get_ticks()



    def update(self):

        # --- LÓGICA DE EFECTOS ---
        ahora = pygame.time.get_ticks()
        
        if ahora - self.daño_timer < 300:
            # 1. Creamos una copia limpia de la imagen
            self.image = self.image_original.copy()
            
            # 2. Creamos una superficie roja del tamaño de la nave
            tinte = pygame.Surface(self.image.get_size()).convert_alpha()
            tinte.fill((255, 0, 0, 70)) # Rojo puro
            
            # 3. La dibujamos sobre la nave usando BLEND_RGB_ADD (esto la pondrá roja/brillante)
            self.image.blit(tinte, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
            
            # 4. Cálculo de sacudida
            self.sacudida_offset = [random.randint(-8, 8), random.randint(-8, 8)]
        else:
            # Volver a la normalidad
            self.image = self.image_original
            self.sacudida_offset = [0, 0]

        


        # asignamos velocidad cada que se ejecuta el ciclo
        self.velocidad_x = 0
        self.velocidad_y = 0

        # capturar pulsasiones del tecleado
        teclas = pygame.key.get_pressed()

        #movimiento hacia la izquierda

        if teclas [pygame.K_a]:
            self.velocidad_x = -10

        #movimiento hacia la derecha
        if teclas [pygame.K_d]:
            self.velocidad_x = 10

        #movimiento hacia la arriba
        if teclas [pygame.K_w]:
            self.velocidad_y = -10

        #movimiento hacia la abajo
        if teclas [pygame.K_s]:
            self.velocidad_y = 10



        #Disparos
        if teclas[pygame.K_SPACE]:
            tiempo = pygame.time.get_ticks()

            if tiempo - self.ultimate > self.cadencia:

                self.disparos()
                self.disparos2()
                self.ultimate = tiempo
                laser.play()





        # Actualizar posicion
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y


        #Limitantes de borde izq, derh
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > ANCHO:
            self.rect.right = ANCHO


        # Limitantes de borde arriba, abajo
        if self.rect.bottom > ALTO:
            self.rect.bottom = ALTO

        if self.rect.top < 0:
            self.rect.top = 0


        # Sumamos el offset al final para que afecte el dibujo
        self.rect.x += self.sacudida_offset[0]
        self.rect.y += self.sacudida_offset[1]



    def disparos(self):
        # Restamos el offset para que la bala salga del lugar real, no del tambaleante
        bala = fire(self.rect.centerx - 40 - self.sacudida_offset[0], self.rect.centery + 20 - self.sacudida_offset[1])
        balas.add(bala)

    def disparos2(self):
        bala = fire(self.rect.centerx + 40 - self.sacudida_offset[0], self.rect.centery + 20 - self.sacudida_offset[1])
        balas.add(bala)




# Aqui le indico a la libreria de python y a pygame, que desde aqui va a iniciar mi videojuego (acciones etc.)
class inicio():
    pygame.init()


#Fuentes externas
pixel = pygame.font.Font("fonts/PressStart2P-Regular.ttf")
pixel_mediana = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 30)
pixel_grande  = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 80)


#Sonidos de ambiente
ambiente = pygame.mixer.Sound("sonidos/sonido_fondo.mp3")
ambiente.set_volume(0.4)

#sonido de disparo
laser = pygame.mixer.Sound("sonidos/disparo.wav")
laser.set_volume(0.2)

#sonidos de puntos
puntos = pygame.mixer.Sound("sonidos/point.wav")
puntos.set_volume(0.2)


#cambiar el volumen
# pygame.mixer.music.set_volume(0.2)


ambiente.play()


#Dibujando la pantalla del jugador
pantalla = pygame.display.set_mode((ANCHO, ALTO)) #Esto me contruye mi pantalla 


#Fondo de pantalla
fondo = pygame.transform.scale(pygame.image.load("img/fondo_espacial.png").convert(),(1000, 600))


#Titulo de la ventana
pygame.display.set_caption("Game Space")


clock = pygame.time.Clock()

#Sprites
jugador = pygame.sprite.Group()
balas = pygame.sprite.Group()
enemigo = pygame.sprite.Group()



# añadir sprites
jugadores = player()
jugador.add(jugadores)


#Sistema de puntuacion
puntuacion = 0
def text(pantalla, fuente_cargada, texto, color,x,y, offset=(0,0)):
    superficie = fuente_cargada.render(texto, True, color)
    rectangulo = superficie.get_rect()
    #sumamos el offset a la posicion original
    rectangulo.center = (x + offset[0], y + offset[0])
    pantalla.blit(superficie, rectangulo)



# Llamamos a la funcion del menu
# Le pasamos la pantalla, el fondo y las fuentes que ya creaste

menu.mostrar_menu(pantalla, fondo, pixel_grande, pixel_mediana)


#Reiniciar el tiempo: Esto e vital para que tus 5sg empiecen a contar desde que se cierra el menu

tiempo_inicio = pygame.time.get_ticks()



#Ciclo del video juego
ejecutando = True # Variable con valor Verdadero


#Posicion inicial del fondo
fondo_y = 0
velocidad_fondo = 2 #Puedes aumentar este numero para parezca que va mas rapido


# Crear variable de tiempo antes de emepezar el juego
tiempo_inicio = pygame.time.get_ticks()
espera_inicial = 5000 #5000 milisegundos son 5sg






while ejecutando: #Mientras siga siendo verdadero me va a ajecutar ciertas acciones

    clock.tick(FPS)

    #Aumentar la Y del fondo para que baje
    fondo_y += velocidad_fondo

    if fondo_y >= ALTO:
        fondo_y = 0


    # Dibujamos el fondo dos veces para que no queden huecos negros

    pantalla.blit(fondo, (0,fondo_y)) #Establece algo a la patalla (el fondo) El primer parametro es la variable fondo, el segundo son sus coordenadas

    pantalla.blit(fondo, (0, fondo_y - ALTO)) # El segundo fondo se dibuja justo Arriba del primero


    for event in pygame.event.get(): #Esto sirve para tomr los eventos de la ventana del video juego

        if event.type == pygame.QUIT: #Esto es para que cuando se le de en la X, se elimina la ventana
            ejecutando = False

    #Muestra de puntuacion
    color_puntos = BLANCO
    offset_puntos = (0,0)
    ahora = pygame.time.get_ticks()

    if ahora -jugadores.daño_timer < 300:
        color_puntos = ROJO
        offset_puntos = jugadores.sacudida_offset

    #Dibujamos el color y offset dinamicos
    text(pantalla,pixel_mediana,str(puntuacion).zfill(4),color_puntos,700,50, offset_puntos)


    #actualizacion de sprites
    jugador.update()
    enemigo.update()
    balas.update()

    
    #Colisiones de personajes
    colision_nave = pygame.sprite.groupcollide(enemigo,jugador, False,False)
    colision_bala = pygame.sprite.groupcollide(enemigo, balas, True, True) 



    #Condicones de colision
    if colision_nave:
        puntuacion -= 10

        for j in jugador:
            j.recibir_daño()
        
    
    if puntuacion < 0:
        puntuacion = 0
         

    if colision_bala:
        puntuacion += 30
        puntos.play()
        


    
    # Condicionar la aparacion de enemigo
    tiempo_actual = pygame.time.get_ticks()

    if not enemigo and (tiempo_actual - tiempo_inicio) > 5000: 
        for x in range(10):
            enemigos = enemy()
            enemigo.add(enemigos)



    #dibujando sprites
    jugador.draw(pantalla)
    enemigo.draw(pantalla)
    balas.draw(pantalla)

    

    pygame.display.flip()












#NOTAS:
#pygame.image.load carga la imagen, el .convert funciona para que las imagenes esten masterizadas y tengan mejor rendimiento , luego establezco las coordenas