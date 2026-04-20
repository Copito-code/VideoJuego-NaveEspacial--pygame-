import pygame
import sys

#Colores que usaremos especificamente para el menu
BLANCO = (255, 255, 255)
NEGRO = (0,0,0)
CYAN = (0,242,255)
PURPURA = (188,0,255)

def mostrar_menu(pantalla, fondo, fuente_titulo, fuente_boton):
    esperando = True
    while esperando:
        # Dibujamos el fondo original que ay tienes
        pantalla.blit(fondo, (0,0))

        #Creamos el Overlay
        overlay = pygame.Surface((pantalla.get_width(), pantalla.get_height()))
        overlay.set_alpha(150) #Nivel de transparencia
        overlay.fill(NEGRO)
        pantalla.blit(overlay, (0,0))

        #Dibujamos el titulo
        superficie_titulo = fuente_titulo.render("GAME SPACE", True, CYAN)
        rect_titulo = superficie_titulo.get_rect(center=(pantalla.get_width() // 2, 150))
        pantalla.blit(superficie_titulo, rect_titulo)


        #Logica del boton
        mouse_pos = pygame.mouse.get_pos()
        #Definimos el rectangulo del boton
        boton_rect = pygame.Rect(0,0,250,60)
        boton_rect.center = (pantalla.get_width() // 2, pantalla.get_height() // 2 +250)


        #Si el mouse esta sobre el boton, cambia el color 
        if boton_rect.collidepoint(mouse_pos):
            color_actual = PURPURA
            #si hace click
            if pygame.mouse.get_pressed()[0] == 1:
                esperando = False # Sale del bucle del menu y arranca el juego

        else:
            color_actual = CYAN


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