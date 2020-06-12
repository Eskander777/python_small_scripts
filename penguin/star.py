import pygame
from pygame.sprite import Sprite
from random import randint

class Ball(Sprite):
    """Класс, представляющий один мяч."""
    
    def __init__(self, ai_settings, screen):
        """Инициализирует мяч и создает его в начальном положении."""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        # Загрузка изображение корабля и назначение атрибута rect."""
        self.image = pygame.image.load('images/ball.bmp')
        self.rect = self.image.get_rect()
        
        # Каждый мяч появляется в произвольном месте
        self.rect.x = randint(0, 1180)
        self.rect.y = self.rect.height
        
        # Сохранение точной позиции
        self.y = float(self.rect.y)
        
    def update(self):
        """Перемещает мяч вниз."""
        self.y += self.ai_settings.ball_drop_speed
        self.rect.y = self.y
    
