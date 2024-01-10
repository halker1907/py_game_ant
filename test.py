import pygame


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.is_game = True
        self.main_loop()

    def handle_events(self):
        """TODO: выход по клавише esc"""
        events = pygame.event.get()
        for event in events:
            if event.type is pygame.QUIT:
                self.is_game = False

    def render(self):
        self.screen.fill((BLACK))
        pygame.display.flip()

    def main_loop(self):
        while self.is_game:
            self.handle_events()
            pygame.draw.rect(self.screen, WHITE, (20, 20, 10, 10))
            pygame.display.update()
        # логика игры
        self.render()
        

if __name__ == '__main__':
    Game()
