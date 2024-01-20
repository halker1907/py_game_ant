import pygame
import random

R = random.randint(0, 255)
G = random.randint(0, 255)
B = random.randint(0, 255)
R_P = random.randint(0, 255)
G_P = random.randint(0, 255)
B_P = random.randint(0, 255)
R_A = random.randint(0, 255)
G_A = random.randint(0, 255)
B_A = random.randint(0, 255)
ANTS_IN_ANTHILL_MAX = 10
IMAGE_ANHILL = pygame.image.load('house_ant.png')
IMAGE_PLAYER = pygame.image.load('anteater.png')


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
    def __init__(self, cell_size, num_cells_x, num_cells_y, existing_positions):
        self.cell_size = cell_size
        self.num_cells_x = num_cells_x
        self.num_cells_y = num_cells_y
        self.positions = self.generate_random_positions(existing_positions)

    def generate_random_positions(self, existing_positions):
        positions = set()
        num_anthills = random.randint(1, 4)
        while len(positions) < num_anthills:
            x = random.randint(0, self.num_cells_x - 1)
            y = random.randint(0, self.num_cells_y - 1)
            position = (x, y)
            if position not in existing_positions and position not in positions:
                positions.add(position)
        return positions

class Ant:
    def __init__(self, cell_size, num_cells_x, num_cells_y, field_num_cells_x, field_num_cells_y):
        self.cell_size = cell_size
        self.x = random.randint(0, num_cells_x - 1)
        self.y = random.randint(0, num_cells_y - 1)
        self.num_cells_x = field_num_cells_x
        self.num_cells_y = field_num_cells_y
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.ants_counter = ANTS_IN_ANTHILL_MAX


    def move_ants(self):
        if self.direction == 'up':
            self.ant_y -= 1
        if self.direction == 'down':
            self.ant_y += 1
        if self.direction == 'left':
            self.ant_x -= 1
        if self.direction == 'right':
            self.ant_x += 1

    def spawn_ants(self):
        for anthill in self.anthills:
            if anthill.ants_counter > 0 and anthill.spawn_counter == 0:
                # Получаем координаты муравейника
                anthill_x, anthill_y = anthill.x, anthill.y

                # Получаем координаты всех соседних клеток вокруг муравейника
                neighbors = [
                    (anthill_y - 1, anthill_x - 1), (anthill_y - 1, anthill_x), (anthill_y - 1, anthill_x + 1),
                    (anthill_y, anthill_x - 1), (anthill_y, anthill_x + 1),
                    (anthill_y + 1, anthill_x - 1), (anthill_y + 1, anthill_x), (anthill_y + 1, anthill_x + 1)
                ]

                # Фильтруем только пустые клетки
                empty_neighbors = [(y, x) for y, x in neighbors if 0 <= y < self.rows and 0 <= x < self.cols and not self.cells[y][x].content]

                # Выбираем случайную пустую клетку, если они есть
                if empty_neighbors:
                    ant_y, ant_x = random.choice(empty_neighbors)
                    ant = Ant(y=ant_y, x=ant_x)
                    self.cells[ant_y][ant_x].content = ant
                    anthill.ants_counter -= 1
                    anthill.spawn_counter = 1

            if anthill.spawn_counter > 0:
                anthill.spawn_counter += 1
                if anthill.spawn_counter > 5:
                    anthill.spawn_counter = 0


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
        self.anthill = Anthill(self.cell_size, self.num_cells_x, self.num_cells_y, {(self.player.x, self.player.y)})
        self.ant = Ant(self.cell_size, self.num_cells_x, self.num_cells_y, num_cells_x, num_cells_y)
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
        flip = pygame.transform.flip(IMAGE_PLAYER, True, False)
        player_rect = IMAGE_PLAYER.get_rect(
            center=(offset_x + (self.player.x + 5.1) * self.cell_size,
                    offset_y + (self.player.y + 5.3) * self.cell_size)
        )
        self.screen.blit(scale_p, player_rect.topleft)

        # Отрисовка муравейников
        for position in self.anthill.positions:
            scale = pygame.transform.scale(
            IMAGE_ANHILL, (IMAGE_ANHILL.get_width() // 10,
                IMAGE_ANHILL.get_height() // 10))
            anthill_rect = IMAGE_ANHILL.get_rect(
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_running = False
                elif event.key == pygame.K_UP:
                    self.field.player.move(0, -1, anthill_positions)
                elif event.key == pygame.K_DOWN:
                    self.field.player.move(0, 1, anthill_positions)
                elif event.key == pygame.K_LEFT:
                    self.field.player.move(-1, 0, anthill_positions)
                elif event.key == pygame.K_RIGHT:
                    self.field.player.move(1, 0, anthill_positions)

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