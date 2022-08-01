class Settings:
    """Una clase para guardar toda la configuracion de alien invasion."""

    def __init__(self):
        """Inicializa la configuracion del juego"""
        #Configuracion de la pantalla
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        #Configuración de la nave
        self.ship_speed = 1.5
        self.ship_limit = 3
        #Configuracion de las balas
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60 ,60)
        self.bullets_allowed = 3
        # Configuraciones del alien.
        self.alien_speed = 5.0
        self.fleet_drop_speed = 10
        # flet_direction de 1 representa derecha; -1 representa izquierda.
        self.fleet_direction = 1 