import sys

import pygame

from settings import Settings

class AlienInvasion:
    """Clase general para gestionar los recursos y el comportammiento del juego."""

    def __init__(self):
        """Inicializa el juego y crea recursos."""
        pygame.init()
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        #Configura el color del fondo.
        #self.bg_color = (230, 230, 230)

    def run_game(self):
        """Inicia el bucle principal para el juego"""
        while True:
            #Busca eventos del teclado y el raton
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            #Redibuja la pantalla en cada paso por le bucle
            self.screen.fill(self.settings.bg_color)
            
            #Hace visible la ultima pantalla dibujada.
            pygame.display.flip()

if __name__ == '__main__':
    #Hace una instancia del juego y lo ejecuta.
    ai = AlienInvasion()
    ai.run_game()