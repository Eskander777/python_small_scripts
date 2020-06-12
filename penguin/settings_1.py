class Settings():
    """Класс для хранения настроек игры."""
    
    def __init__(self):
        """Инициализирует настройки игры."""
        # Параметры экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (182, 182, 182)
        
        # Настройки ловца
        self.catcher_speed_factor = 1
        self.lose_limit = 2
        
        # Настройки мяча
        self.ball_speed_factor = 1
        self.ball_drop_speed = 0.3
        self.balls_allowed = 1
        
        
     
