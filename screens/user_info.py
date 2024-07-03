# screens/user_info.py

import pygame

from .screens import Screens

class UserInfoGUI(Screens):
    def __init__(self, screen_manager):
        super.__init__(screen_manager)
        self.font = pygame.font.Font(None, 36)