import pygame
from lib import *


class Window:
    resolutions = [(1024, 768), 
                   (1280, 720),   # 720p
                   (1920, 1080),  # 1080p
                   (1366, 768),
                   (800, 600),
                   (2560, 1440),
                   (3840, 2160),
                   (7680, 4320)]

    def __init__(self, height, width, selected_screen):
        self.selected_screen = selected_screen
        self.screens = Screens(self.selected_screen)
        self.width = width
        self.height = height

    def get_resolution(self):
        return self.height, self.width

    def set_resolution(self, height, width):
        self.height = height
        self.width = width

    def main_menu(self):
        Screens.set_selected_screen(0)


class Button:
    def __init__(self, text, command=None, color='white', size=(100, 50), font=('Arial', 14)):
        assert font[0] in fonts, "Font not supported"
        assert font[1] in sizes, "Size not supported"
        self.text = text
        self.command = command  # Callback function to be executed when the button is clicked
        self.color = color  # Button color
        self.size = size  # Button size (width, height)
        self.font = font  # Button font (font type, size)

    def click(self):
        if self.command is not None:
            self.command()  # Execute the button's command when clicked

    def set_color(self, color):
        self.color = color  # Set new color

    def set_size(self, size):
        self.size = size  # Set new size

    def set_font(self, font):
        self.font = font  # Set new font


class Screens:
    MENU_SCREEN = 0
    SETTINGS_SCREEN = 1
    GAME_SCREEN = 2

    def __init__(self, selected_screen):
        self.selected_screen = selected_screen
        self.screen = pygame.display.set_mode(Window.resolutions[0])

    def set_selected_screen(self, screen):
        self.selected_screen = screen

    def get_selected_screen(self):
        return self.selected_screen

    def display_screen(self):
        if self.selected_screen == self.MENU_SCREEN:
            print("Displaying Menu Screen")
            self.screen.fill(Colors.RED)

        elif self.selected_screen == self.SETTINGS_SCREEN:
            print("Displaying Settings Screen")
            self.screen.fill(Colors.GREEN)

        elif self.selected_screen == self.GAME_SCREEN:
            print("Displaying Game Screen")
            self.screen.fill(Colors.BLUE)
