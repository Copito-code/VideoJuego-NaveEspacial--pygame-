import pygame
import sys
import random
import math

# Dimensiones de ventana
ANCHO = 800
ALTO = 600

#Colores que usaremos especificamente para el menu
BLANCO = (255, 255, 255)
NEGRO = (0,0,0)
CYAN = (0,242,255)
PURPURA = (188,0,255)

class EstrellaFugaz(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        #Cargar imagen de estrella
        try:
            self.image = pygame.image.load("img/estrella_fugaz.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (60,60))

        except pygame.error:
            #imgage de respaldo 
            self.image = pygame.Surface((15,15))
            self.image.fill(BLANCO)

        self.rect = self.image.get_rect()
        self.reset_posicion()

    def reset_posicion(self):
        # Aparece en la esquina superior izquierda, pero un poco fuera de pantalla
        self.rect.x = random.randrange(-200, -50)
        self.rect.y = random.randrange(-200, -50)
        
        # Velocidad balanceada para una diagonal hacia abajo-derecha
        self.velocidad_x = random.randrange(4, 8)
        self.velocidad_y = random.randrange(4, 8)

    

    def draw_glow(self, pantalla):
        # Dibujamos 3 capas de brillo para un efecto suave
        # Capa 1: Brillo grande y muy tenue
        # Capa 2: Brillo mediano
        # Capa 3: Brillo pequeño y más intenso
        
        for i in range(3):
            radio = 15 + (i * 8) # El radio crece en cada capa
            alfa = 100 - (i * 35) # La transparencia baja (se vuelve más invisible)
            
            # Creamos una superficie temporal para el círculo con transparencia
            glow_surf = pygame.Surface((radio * 2, radio * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (0, 242, 255, alfa), (radio, radio), radio)
            
            ajuste_x = 15  # Positivo = Derecha, Negativo = Izquierda
            ajuste_y = 3  # Positivo = Abajo, Negativo = Arriba

            # Dibujamos el brillo desplazado hacia la punta
            pantalla.blit(glow_surf, (self.rect.centerx + ajuste_x - radio, self.rect.centery + ajuste_y - radio))


    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
        
        # Si sale por el fondo o por la derecha de la pantalla
        if self.rect.top > ALTO or self.rect.left > ANCHO:
            self.reset_posicion()




def mostrar_menu(pantalla, fondo, fuente_titulo, fuente_boton):

    #Cargar sonido y variable de control
    try:
        sonido_hover = pygame.mixer.Sound("sonidos/hover_menu.wav")
        sonido_hover.set_volume(0.3)
    
    except:
        sonido_hover = None #Por si el archivo no existe aun

    mouse_sonido = False


    #Creamos un grupo de sprites para las estrellas
    estrellas = pygame.sprite.Group()

    #Creamos unas cuantas estrellas iniciales
    for _ in range(3):
        estrellas.add(EstrellaFugaz())

    clock = pygame.time.Clock() # Reloj para controlar los FPS del menu

    contador_tiempo = 0

    esperando = True
    while esperando:

        clock.tick(60)

        # Dibujamos el fondo original que ay tienes
        pantalla.blit(fondo, (0,0))

        #Creamos el Overlay
        overlay = pygame.Surface((pantalla.get_width(), pantalla.get_height()))
        overlay.set_alpha(150) #Nivel de transparencia
        overlay.fill(NEGRO)
        pantalla.blit(overlay, (0,0))

        #Actualizar y dibujar estrellas fugaces
        estrellas.update()
        for estrella in estrellas:
            estrella.draw_glow(pantalla) # Primero el brillo (capa de atrás)
        estrellas.draw(pantalla)

        # 2. Lógica de animación flotante
        contador_tiempo += 0.05  # Controla la velocidad (más pequeño = más lento)
        # math.sin nos da un valor entre -1 y 1. Multiplicamos por 15 para que suba/baje 15 píxeles.
        desplazamiento_y = math.sin(contador_tiempo) * 15 
        
        # 3. Aplicamos el desplazamiento al centro del título
        pos_y_animada = 250 + desplazamiento_y

       

        #Dibujamos el titulo con padding Lateral
        padding_lateral = 30
        ancho_maximo = pantalla.get_width() - (padding_lateral * 2)
        superficie_titulo = fuente_titulo.render("GAME SPACE", True, CYAN)

        #Si el titulo es mas ancho que el espacio permitido, lo encogemos
        if superficie_titulo.get_width() > ancho_maximo:
            nuevo_alto = int(superficie_titulo.get_height() * (ancho_maximo / superficie_titulo.get_width()))
            superficie_titulo = pygame.transform.scale(superficie_titulo, (ancho_maximo, nuevo_alto))

        rect_titulo = superficie_titulo.get_rect(center=(pantalla.get_width() // 2, pos_y_animada))
        pantalla.blit(superficie_titulo, rect_titulo)


        #Logica del boton
        mouse_pos = pygame.mouse.get_pos()
        #Definimos el rectangulo del boton
        boton_rect = pygame.Rect(0,0,250,60)
        boton_rect.center = (pantalla.get_width() // 2, pantalla.get_height() // 2 + 190)


        #Si el mouse esta sobre el boton, cambia el color 
        if boton_rect.collidepoint(mouse_pos):
            color_actual = PURPURA

            if not mouse_sonido:
                if sonido_hover:
                    sonido_hover.play()
                mouse_sonido = True #Se bloque para que no se repita

            # Dibujamos un segundo borde más grande y fino para el efecto de "energía"
            borde_glow = boton_rect.inflate(10, 10) 
            pygame.draw.rect(pantalla, BLANCO, borde_glow, width=2, border_radius=15)
            
            #si hace click
            if pygame.mouse.get_pressed()[0] == 1:
                esperando = False # Sale del bucle del menu y arranca el juego

        else:
            color_actual = CYAN
            #Resetear la variable 
            mouse_sonido = False #EL mouse salio, listo para sonar de nuevo


        #Dibujamos el boton fisico
        pygame.draw.rect(pantalla, color_actual, boton_rect, border_radius=10)


        #Texto dentro del boton 
        superficie_btn = fuente_boton.render("INICIAR", True, NEGRO)
        rect_btn = superficie_btn.get_rect(center=boton_rect.center)
        pantalla.blit(superficie_btn, rect_btn)


        #Eventos para cerrar la ventana desde el menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()