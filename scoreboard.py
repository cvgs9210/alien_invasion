import pygame.font
 
class Scoreboard:
    """Una clase para dar informacion de la puntuacion"""

    def __init__(self, ai_game):
        """Inicializa los atributos de la puntuacion."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Configuracion de fuente para la informacion de la puntuacion.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Prepara la imagen de la puntuacion inicial.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()

    def prep_score(self):
        """Convierte la puntuacion en una imagen renderizada."""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_tag = self.font.render("SCORE: ", True, self.text_color, self.settings.bg_color)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Muestra la puntuacion en la parte superior derecha de la pantalla
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
        # Muestra la etiqueta SCORE
        self.score_tag_rect = self.score_tag.get_rect()
        self.score_tag_rect.right = self.score_rect.left
        self.score_tag_rect.top = self.score_rect.top

    def show_score(self):
        """Dibuja la puntuacion en la pantalla."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.level_tag, self.level_tag_rect)
        self.screen.blit(self.score_tag, self.score_tag_rect)
        self.screen.blit(self.high_score_tag, self.high_score_tag_rect)

    def prep_high_score(self):
        """Convierte la puntuacion mas alta en una imagen renderizada."""
        high_score =round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_tag = self.font.render("HIGH SCORE: ", True, self.text_color, self.settings.bg_color)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        # Centra la puntuacion mas alta en la parte superior de la pantalla.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
        # Muestra la etiqueta HIGH SCORE
        self.high_score_tag_rect = self.high_score_tag.get_rect()
        self.high_score_tag_rect.right = self.high_score_rect.left
        self.high_score_tag_rect.top = self.high_score_rect.top

    def prep_level(self):
        """Convierte el nivel en una iamgen renderizada"""
        level_str = str(self.stats.level)
        self.level_tag = self.font.render("LEVEL: ", True, self.text_color, self.settings.bg_color)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        # Coloca el nivel debajo de la puntuacion.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10
        # Muestra la etiqueta LEVEL
        self.level_tag_rect = self.level_tag.get_rect()
        self.level_tag_rect.right = self.level_rect.left
        self.level_tag_rect.top = self.level_rect.top

    def check_high_score(self):
        """Comprueba si hay una nueva puntuacion mas alta"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
