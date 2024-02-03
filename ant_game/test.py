import pygame
import sys

width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("fnf")

while True:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                     pygame.quit()
                     sys.exit()



    pygame.display.flip()