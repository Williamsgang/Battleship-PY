# screens/user_info.py

import pygame
from logs import logger
from screens import Screens
from server.player_creation import PlayerCreation


class UserInfoGUI(Screens):
    def __init__(self, screen_manager):
        self.log = logger.Logger(self.__class__.__name__)
        super().__init__(screen_manager)
        self.font = pygame.font.Font(None, 36)
        self.username = ""
        self.input_box = pygame.Rect(100, 100, 140, 32)
        self.save_button = pygame.Rect(100, 150, 100, 50)
        self.active = False
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.screen_manager.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.screen_manager.set_screen("settings")
                if self.active:
                    if event.key == pygame.K_RETURN:
                        self.create_player(self.username, self.screen_manager.get_ip_address())
                        self.username = ''
                    elif event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    else:
                        self.username += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_box.collidepoint(event.pos):
                    self.active = not self.active
                else:
                    self.active = False
                self.color = self.color_active if self.active else self.color_inactive

                if self.save_button.collidepoint(event.pos):
                    self.create_player(self.username, self.screen_manager.get_ip_address())
                    self.username = ''

    def update(self):
        pass

    def render(self):
        self.SCREEN.fill((0, 128, 128))
        text = self.font.render("Enter Username:", True, (255, 255, 255))
        self.SCREEN.blit(text, (100, 50))
        txt_surface = self.font.render(self.username, True, self.color)
        width = max(200, txt_surface.get_width() + 10)
        self.input_box.w = width
        self.SCREEN.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        pygame.draw.rect(self.SCREEN, self.color, self.input_box, 2)

        # Render Save Button
        pygame.draw.rect(self.SCREEN, self.color_active, self.save_button)
        save_text = self.font.render("Save", True, (255, 255, 255))
        self.SCREEN.blit(save_text, (self.save_button.x + 15, self.save_button.y + 10))

        back_text = self.font.render("Press ESC to return", True, (255, 255, 255))
        self.SCREEN.blit(back_text, (50, 200))

    def create_player(self, username, ip_address):
        self.log.log_info('create_player', f'Creating player with username: {username} and IP: {ip_address}')
        try:
            player_creator = PlayerCreation(username, ip_address)
            player_info = player_creator.create_player_info()
            player_creator.save_player_info(player_info)
            self.log.log_info('create_player', f'Player {username} created and saved')
        except ValueError as e:
            self.log.log_warning('create_player', str(e))
        except Exception as e:
            self.log.log_error('create_player', f'Error creating player: {e}')
