import pygame

from screen import Window, Button, Screens

running = True
window_info = Window(*Window.resolutions[0])
clock = pygame.time.Clock()
screens = Screens()
screens.get_selected_screen()

main_menu_btn = Button("Main Menu",  screens.display_screen())


window_size = window_info.get_resolution()

pygame.init()

app_screen = pygame.display.set_mode(window_size)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(60)

    pygame.display.flip()

pygame.quit()

