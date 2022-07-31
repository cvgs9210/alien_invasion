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