import sys

import pygame
from star import Ball
from tractor import Catcher

def check_keydown_events(event, ai_settings, screen, catcher):
    """Реагирует на нажатие клавиш."""
    if event.key == pygame.K_RIGHT:
        catcher.moving_right = True
    elif event.key == pygame.K_LEFT:
        catcher.moving_left = True
    elif event.key == pygame.K_q:
        sys.exit()
        
def check_keyup_events(event, catcher):
    """Реагирует на отпускание клавиш."""
    if event.key == pygame.K_RIGHT:
        catcher.moving_right = False
    elif event.key == pygame.K_LEFT:
        catcher.moving_left = False
        
def check_events(ai_settings, screen, catcher):
    """Обрабатывает нажатия клавиш и события мыши."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, catcher)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, catcher)

def update_screen(ai_settings, screen, catcher, balls):
    """Обновляет изображение на экране и отображает новый экран."""
    # При каждом проходе цикла перерисовывается экран.
    screen.fill(ai_settings.bg_color) 
    catcher.blitme()
    balls.draw(screen)
        
    # Отображение последнего прорисованного экрана.
    pygame.display.flip()
    
def create_ball(ai_settings, screen, balls):
    """Создает новый мяч, когда старый исчез."""
    if len(balls) < ai_settings.balls_allowed:
        new_ball = Ball(ai_settings, screen)
        balls.add(new_ball)

def update_balls(ai_settings, stats, screen, balls, catcher):
    """Обновляет позицию мяча и удаляет вышедший за край экрана."""
    # Создание нового мяча
    create_ball(ai_settings, screen, balls)
    # Обновление позиции мяча.
    balls.update()
    ball_reach_bottom(ai_settings, stats, screen, catcher, balls)
    
    # Удаление мячей, вышедших за край экрана.
    for ball in balls.copy():
        if ball.rect.bottom >= 800:
            balls.remove(ball)
    check_catching(ai_settings, screen, balls, catcher, ball)
            
def check_catching(ai_settings, screen, balls, catcher, ball):
    """Обработка ловли мяча."""
    # При обнаружении соприкосновения, удалить мяч
    collisions = pygame.sprite.spritecollideany(catcher, balls)
    if collisions:
        balls.remove(ball)
        
def ball_reach_bottom(ai_settings, stats, screen, catcher, balls):
    """Останавливает игру, если мяч достиг края."""
    screen_rect = screen.get_rect()
    for ball in balls.sprites():
        if ball.rect.bottom >= screen_rect.bottom:
            if stats.attempts_left > 0:
                # Уменьшение attempts_left
                stats.attempts_left -= 1 
            else:
                stats.game_active = False
            
