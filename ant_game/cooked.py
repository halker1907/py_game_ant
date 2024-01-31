import pygame
import random
import sys

R = random.randint(0, 255)
G = random.randint(0, 255)
B = random.randint(0, 255)
ANTS_IN_ANTHILL_MAX = 10
IMAGE_ANTHILL = pygame.image.load('house_ant.png')
IMAGE_PLAYER = pygame.image.load('anteater.png')
IMAGE_ANT = pygame.image.load('ants.png')


class Player:
    def __init__(self, cell_size, num_cells_x, num_cells_y, field_num_cells_x, field_num_cells_y):
        self.cell_size = cell_size
        self.x = random.randint(0, num_cells_x - 1)
        self.y = random.randint(0, num_cells_y - 1)
        self.num_cells_x = field_num_cells_x
        self.num_cells_y = field_num_cells_y

    def move(self, dx, dy, anthill_positions):
        new_x = (self.x + dx) % self.num_cells_x
        new_y = (self.y + dy) % self.num_cells_y

        if (new_x, new_y) not in anthill_positions:
            self.x = new_x
            self.y = new_y

class Anthill:
    def __init__(self, cell_size, num_cells_x, num_cells_y):
        self.cell_size = cell_size
        self.num_cells_x = num_cells_x
        self.num_cells_y = num_cells_y


class Ant:
    def __init__(self, cell_size, num_cells_x, num_cells_y, existing_positions):
        self.cell_size = cell_size
        self.num_cells_x = num_cells_x
        self.num_cells_y = num_cells_y
        self.x_anthill = random.randint(0, self.num_cells_x - 1)
        self.y_anthill = random.randint(0, self.num_cells_y - 1)
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.ants_counter = ANTS_IN_ANTHILL_MAX
        self.positions_a = self.generate_positions_ants(existing_positions)
        self.positions = self.generate_random_positions(existing_positions)

    def generate_random_positions(self, existing_positions):
        positions = set()
        num_anthills = random.randint(1, 4)
        while len(positions) < num_anthills:
            position = (self.x_anthill, self.y_anthill)
            if position not in existing_positions and position not in positions:
                positions.add(position)
        return positions

    def generate_positions_ants(self, existing_positions):
        positions_a = set()
        num_ant = random.randint(1, 4)
        while len(positions_a) < num_ant:
            x_a = self.x_anthill - 1 or + 1
            y_a = self.y_anthill - 1 or + 1
            position = (x_a, y_a)
            if positions_a not in existing_positions and position not in positions_a:
                positions_a.add(position)
        return positions_a

    def move_ants(self):
        if self.direction == 'up':
            self.ant_y -= 1
        if self.direction == 'down':
            self.ant_y += 1
        if self.direction == 'left':
            self.ant_x -= 1
        if self.direction == 'right':
            self.ant_x += 1



class Field:
    def __init__(self, screen, cell_size, num_cells_x, num_cells_y):
        self.cell_size = cell_size
        self.screen = screen
        self.num_cells_x = num_cells_x
        self.num_cells_y = num_cells_y
        self.r = random.randint(0, 255)
        self.g = random.randint(0, 255)
        self.b = random.randint(0, 255)
        self.player = Player(self.cell_size, self.num_cells_x, self.num_cells_y, num_cells_x, num_cells_y)
        self.ant = Ant(self.cell_size, self.num_cells_x, self.num_cells_y, {(self.player.x, self.player.y)})
        self.font = pygame.font.Font(None, self.cell_size)
        pygame.display.set_caption("поле")

    def render(self, offset_x, offset_y):
        for x in range(self.num_cells_x):
            for y in range(self.num_cells_y):
                cell_surface = pygame.Surface((self.cell_size, self.cell_size))
                cell_surface.fill((R, G, B))
                pygame.draw.rect(cell_surface, (0, 0, 0), cell_surface.get_rect(), 2)

                cell_rect = cell_surface.get_rect(
                    topleft=(offset_x + x * self.cell_size, offset_y + y * self.cell_size)
                )

                self.screen.blit(cell_surface, cell_rect.topleft)

        # Отрисовка игрока
        scale_p = pygame.transform.scale(
        IMAGE_PLAYER, (IMAGE_PLAYER.get_width() // 9,
            IMAGE_PLAYER.get_height() // 9))
        player_rect = IMAGE_PLAYER.get_rect(
            center=(offset_x + (self.player.x + 5.1) * self.cell_size,
                    offset_y + (self.player.y + 5.3) * self.cell_size)
        )
        self.screen.blit(scale_p, player_rect.topleft)

        # Отрисовка муравейников
        for position in self.ant.positions:
            scale = pygame.transform.scale(
            IMAGE_ANTHILL, (IMAGE_ANTHILL.get_width() // 10,
                IMAGE_ANTHILL.get_height() // 10))
            anthill_rect = IMAGE_ANTHILL.get_rect(
                center=(offset_x + (position[0] + 5.1) * self.cell_size,
                        offset_y + (position[1] + 5.2) * self.cell_size)
            )
            self.screen.blit(scale, anthill_rect.topleft)

                # инфа на экране
        font = pygame.font.Font(None, 72)
        text = font.render("сделано ходов:", True, (R, G, B))
        place = text.get_rect(center=(500, 450))
        self.screen.blit(text, place)

        text2 = font.render("", True, (R, G, B))
        place2 = text2.get_rect(center=(500, 500))
        self.screen.blit(text2, place2)
                         
        # Отрисовка муравьёв
        for position in self.ant.positions_a:
            scale = pygame.transform.scale(
            IMAGE_ANT, (IMAGE_ANT.get_width() // 10,
                IMAGE_ANT.get_height() // 10))
            anthill_rect = IMAGE_ANT.get_rect(
                center=(offset_x + (position[0] + 5.1) * self.cell_size,
                        offset_y + (position[1] + 5.2) * self.cell_size)
            )
            self.screen.blit(scale, anthill_rect.topleft)


class Window:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080))
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.cell_size = 50
        self.num_cells_x = 10
        self.num_cells_y = 10
        self.offset_x = 0
        self.offset_y = 0

        self.field = Field(self.screen, self.cell_size, self.num_cells_x, self.num_cells_y)

    def run(self):
        while self.is_running:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.render()

    def handle_events(self):
        anthill_positions = self.field.anthill.positions
        self.counter_move = 0 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_running = False

                elif event.key == pygame.K_UP:
                    self.field.player.move(0, -1, anthill_positions)
                    self.counter_move += 1

                elif event.key == pygame.K_DOWN:
                    self.field.player.move(0, 1, anthill_positions)
                    self.counter_move += 1

                elif event.key == pygame.K_LEFT:
                    self.field.player.move(-1, 0, anthill_positions)
                    self.counter_move += 1

                elif event.key == pygame.K_RIGHT:
                    self.field.player.move(1, 0, anthill_positions)
                    self.counter_move += 1

    def update(self):
        pass

    def render(self):
        self.screen.fill((255, 255, 255))
        self.offset_x = (self.screen.get_width() - self.num_cells_x * self.cell_size) // 2
        self.offset_y = (self.screen.get_height() - self.num_cells_y * self.cell_size) // 2

        self.field.render(self.offset_x, self.offset_y)

        pygame.display.flip()

    def quit_game(self):
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Window()
    game.run()
    game.quit_game()