# screens/main_menu_screen.py

import pygame

from .screens import Screens


class MainMenuGUI(Screens):
    def __init__(self, screen_manager):
        super().__init__(screen_manager)
        self.font = pygame.font.Font(None, 36)
        self.buttons = [
            {"text": "Start Game", "rect": pygame.Rect(100, 150, 200, 50), "action": self.start_game},
            {"text": "Settings", "rect": pygame.Rect(100, 250, 200, 50), "action": self.open_settings},
            {"text": "Quit", "rect": pygame.Rect(100, 350, 200, 50), "action": self.quit_game},

        ]

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.screen_manager.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in self.buttons:
                    if button["rect"].collidepoint(event.pos):
                        button["action"]()

    def update(self):
        pass

    def render(self):
        self.SCREEN.fill((0, 0, 128))
        for button in self.buttons:
            pygame.draw.rect(self.SCREEN, (255, 255, 255), button["rect"])
            text = self.font.render(button["text"], True, (0, 0, 0))
            self.SCREEN.blit(text, button["rect"].topleft)

    def start_game(self):
        self.screen_manager.set_screen("game")

    def open_settings(self):
        self.screen_manager.set_screen("settings")

    def quit_game(self):
        self.screen_manager.running = False
