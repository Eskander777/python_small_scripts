import pygame

class Catcher():
    def __init__(self, ai_settings, screen):
        """Инициализирует ракету и задает ее начальную позицию."""
        self.screen = screen
        self.ai_settings = ai_settings
        
        # Загрузка изображения ракеты и получение прямоугольника
        self.image = pygame.image.load('images/catcher.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # Каждый новая ракета появляется в центре экрана.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        # Сохраниение вещественной координаты центра корабля
        self.center = float(self.rect.centerx)
        
        # Флаги перемещения
        self.moving_left = False
        self.moving_right = False
        
    def update(self):
        """Обновляет позицию ракеты с учетом флага."""
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.catcher_speed_factor
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.catcher_speed_factor
            
        # Обновление атрибута rect на основании self.center.
        self.rect.centerx = self.center
    
    def blitme(self):
        """Рисует ракету в текущей позиции."""
        self.screen.blit(self.image, self.rect)
        
    def center_catcher(self):
        """Размещает ловца в центре нижней стороны."""
        self.center = self.screen.rect.centerx
    
