# screens/game_screen.py

import pygame

from screens import Screens


class GameGUI(Screens):
    def __init__(self, screen_manager):
        super().__init__(screen_manager)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.screen_manager.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.screen_manager.set_screen("main_menu")

    def update(self):
        pass

    def render(self):
        self.SCREEN.fill((0, 128, 0))
        font = pygame.font.Font(None, 36)
        text = font.render("Game Screen - Press ESC to return to main menu", True, (255, 255, 255))
        self.SCREEN.blit(text, (50, 50))
