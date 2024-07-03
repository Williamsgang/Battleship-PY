# screens/settings_screen.py

import pygame

from screens import Screens


class SettingsGUI(Screens):
    def __init__(self, screen_manager):
        super().__init__(screen_manager)
        self.font = pygame.font.Font(None, 36)
        self.buttons = [
            {"text": "User Info", "rect": pygame.Rect(100, 150, 200, 50), "action": self.show_user_info},
        ]

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.screen_manager.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.screen_manager.set_screen("main_menu")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in self.buttons:
                    if button["rect"].collidepoint(event.pos):
                        button["action"]()

    def update(self):
        pass

    def render(self):
        self.SCREEN.fill((128, 0, 0))
        for button in self.buttons:
            pygame.draw.rect(self.SCREEN, (255, 255, 255), button["rect"])
            text = self.font.render(button["text"], True, (0, 0, 0))
            self.SCREEN.blit(text, button["rect"].topleft)

    def show_user_info(self):
        self.screen_manager.set_screen("user_info")
