import pygame
pygame.init()
pygame.display.set_caption('Deep Game Extractor')

from screen import *

clock = pygame.time.Clock()

config.current_screen = IntroScreen()

running = True
while running:
    config.screen.fill(config.background)

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            config.save_config()

    # Update
    config.current_screen.update(events)

    # Draw
    config.current_screen.draw()

    pygame.display.flip()
    clock.tick(60)
