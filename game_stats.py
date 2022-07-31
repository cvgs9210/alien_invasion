class GameStats:
    """Sigue las estadisticas de Alien Invasion"""

    def __init__(self, ai_games):
        """Inicializa las estadisticas"""
        self.settings = ai_games.settings
        self.reset_stats()
        
        # Inicia Alien Invasion en estado activo.
        self.game_active = True

    def reset_stats(self):
        """Inicializa las estadisticas que pueden cambiar durante el juego."""
        self.ships_left = self.settings.ship_limit