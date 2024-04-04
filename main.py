import pygame
from screen import Window

running = True
window_info = Window
clock = pygame.time.Clock()

window_size = [window_info.HEIGHT, window_info.WIDTH]

pygame.init()

app_screen = pygame.display.set_mode(window_size)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(60)

    pygame.display.flip()

pygame.quit()
