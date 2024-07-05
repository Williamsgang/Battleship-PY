import pygame

from adhd_version.screens import Screens


class MainMenuScreen(Screens):
    def __init__(self, screen_manager):
        super().__init__(screen_manager)
        self.font = pygame.font.Font(None, 36)
        self.buttons = [
            {"text": "Connect to a Live Game", "rect": pygame.Rect(350, 200, 200, 50), "action": self.start_game},
            {"text": 'Play against AI', "rect": pygame.Rect(350, 200, 200, 50), "action": None},
            {"text": "Settings", "rect": pygame.Rect(350, 300, 200, 50), "action": self.open_settings},
            {"text": "Quit", "rect": pygame.Rect(350, 400, 200, 50), "action": self.quit_game},
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
        self.SCREEN.fill((0, 0, 0))
        for button in self.buttons:
            pygame.draw.rect(self.SCREEN, (0, 255, 0), button["rect"])
            text = self.font.render(button["text"], True, (255, 255, 255))
            self.SCREEN.blit(text, button["rect"].inflate(-10, -10).topleft)

    def start_game(self):
        self.screen_manager.start_game()

    def open_settings(self):
        self.screen_manager.set_screen("settings")

    def quit_game(self):
        pygame.quit()
        quit()
