import sys
from time import sleep
from turtle import Screen

import pygame

from bullet import Bullet
from alien import Alien
from settings import Settings
from game_stats import GameStats
from ship import Ship

class AlienInvasion:
    """Clase general para gestionar los recursos y el comportammiento del juego."""

    def __init__(self):
        """Inicializa el juego y crea recursos."""
        pygame.init()
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode(
           (self.settings.screen_width, self.settings.screen_height))
        """PANTALLA COMPLETA
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height"""
        pygame.display.set_caption("Alien Invasion")

        # Crea una instancia para guardar las esat6disticas del juego.
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        #Configura el color del fondo.
        #self.bg_color = (230, 230, 230)

    def run_game(self):
        """Inicia el bucle principal para el juego"""
        while True:

            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            
            self._update_screen()

    def _check_events(self):
        #Busca eventos del teclado y el raton
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
    
    def _check_keydown_events(self, event):
        """Responde a pulsaciones de teclas"""
        if event.key == pygame.K_RIGHT:
            #Mueve la nave a la derecha
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Responde a las liberaciones de las teclas"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Crea una bala nueva y la añade al grupo de balas"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """Crea la flota de aliens."""
        # Hace un alien y halla el número de aliens en una fila.
        # El esapcio entre aliens es igual a la anchura de un alien.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2* alien_width)

        # Determina el numero de filas de aliens que caben en la pantalla.
        ship_height = self.ship.rect.height
        available_space_y =  (self.settings.screen_height - (3* alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        # Crea la flota completa de aliens.
        for row_number in range(number_rows):
            # Crea la primera fila de alien 
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
    
    def _check_fleet_edges(self):
        """Responde adecuadamente si algun alien ha llegado a un borde."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _check_bullet_alien_collisions(self):
        """Responde a las colisiones bala-alien."""
        # Retira todas las balas y aliens que han colisionado
        # Si hay, se deshace de la bala y del alien.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            # Destruye las balas existentes y crea una flota nueva
            self.bullets.empty()
            self._create_fleet()

    def _check_aliens_bottom(self):
        """Comprueba si algun alien ha llegado al fondo de la pantalla."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Trata esto como si la nave hubiese sido alcanzada.
                self._ship_hit()
                break

    def _change_fleet_direction(self):
        """Baja toda la flota y cambia su direccion."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_alien(self, alien_number, row_number):
        # Crea un alien y lo coloca en la fila.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_screen(self):
        #Redibuja la pantalla en cada paso por le bucle
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        #Hace visible la ultima pantalla dibujada.
        pygame.display.flip()

    def _update_bullets(self):
        """Actualiza la posicion de las balas y se deshace de las viejas"""
        # Actualiza las posiciones de la balas.
        self.bullets.update()

        # Se deshace de las blas que han desaparecido
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        #print(len(self.bullets))
        self._check_bullet_alien_collisions()

    def _update_aliens(self):
        """
        Comprueba si la flota esta en un borde,
        despues actualiza las posiciones de todas las flotas.
        """
        self._check_fleet_edges()
        """Actualiza las posiciones de todos los aliens de la flota."""
        self.aliens.update()

        # Busca colisiones alien-nave.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            #print("Ship hit!!!")
            self._ship_hit()
        
        # Busca aliens llegando al fondo de la pantalla.
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Responde al impacto de un alien con la nave."""
        if self.stats.ships_left > 0:

            # Disminuye ships_left.
            self.stats.ships_left -= 1

            # Se deshace de los aliens y balas restantes.
            self.aliens.empty()
            self.bullets.empty()

            # Crea una flota nueva y centra la nave
            self._create_fleet()
            self.ship.center_ship()

            # Pausa
            sleep(0.5)
        else:
            self.stats.game_active = False

if __name__ == '__main__':
    #Hace una instancia del juego y lo ejecuta.
    ai = AlienInvasion()
    ai.run_game()