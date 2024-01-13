import pygame
import random

width = 1920
height = 1080
r = random.randint(0, 255)
g = random.randint(0, 255)
b = random.randint(0, 255)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("поле")

cell_size = 20
rows = height // cell_size
cols = width // cell_size

black = (r, g, b)
white = (255, 255, 255)

def draw_grid():
    for x in range(0, width, cell_size):
        for y in range(0, height, cell_size):
            rect = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(screen, white, rect, 1)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
    
    screen.fill(black)
    draw_grid()

    pygame.display.flip()

pygame.quit()
        