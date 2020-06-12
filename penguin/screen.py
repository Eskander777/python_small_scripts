import pygame
from pygame.sprite import Group
from tractor import Catcher
from game_stats_1 import MyGameStats
from settings_1 import Settings
import game_functions_1 as gf

def run_game():
    # Инициализирует игру и создает объект экрана.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Grey Sky")
    
    # Создание ловца
    catcher = Catcher(ai_settings, screen)
    # Создание мяча
    balls = Group()
    # Создание экземпляра для хранения игровой статистики.
    stats = MyGameStats(ai_settings)
   
    # Запуск основного цикла игры.
    while True:
        # Отслеживание событий.
        gf.check_events(ai_settings, screen, catcher)
        if stats.game_active:
            catcher.update()
            gf.update_balls(ai_settings, stats, screen, balls, catcher)
        
        gf.update_screen(ai_settings, screen, catcher, balls)

       
run_game()
