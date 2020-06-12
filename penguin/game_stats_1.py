class MyGameStats():
    """Отслеживание статистики для игры."""
    
    def __init__(self, ai_settings):
        """Инициализирует статистику."""
        self.ai_settings = ai_settings
        self.reset_stats()
        # Игра запускается в активном состоянии.
        self.game_active = True
        
    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры."""
        self.attempts_left = self.ai_settings.lose_limit
