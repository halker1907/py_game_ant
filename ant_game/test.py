import pygame
import sys
pygame.font.init()
 
sc = pygame.display.set_mode((300, 200))
sc.fill((255, 255, 255))
 
f1 = pygame.font.Font(None, 36)
text1 = f1.render('Hello Привет', True,
                  (180, 0, 0))
 
f2 = pygame.font.SysFont('serif', 48)
text2 = f2.render("World Мир", False,
                  (0, 180, 0))
 
sc.blit(text1, (10, 50))
sc.blit(text2, (10, 100))
pygame.display.update()
 
while 1:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()