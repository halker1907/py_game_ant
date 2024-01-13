import keyboard
import os
import random
import sys

# настройки
COLS = 10
ROWS = 10
EMPTY = "."
PLAYER = "P"
ANT = "a"
ANTHILL = "A"
ANTHILL_MAX = 4
ANTHILL_MIN = 1
ANTS_IN_ANTHILL_MAX = 10
ANTS_IN_ANTHILL_MIN = 1


class GameObject:
    def __init__(self, y, x, image):
        self.y = y
        self.x = x
        self.image = image

    def move(self, direction, field): # передвижение объектов
        new_y, new_x = self.y, self.x

        if direction == "up" and self.y > 0 and not isinstance(field.cells[self.y - 1][self.x].content, Anthill):
            new_y -= 1
        elif direction == "down" and self.y < field.rows - 1 and not isinstance(field.cells[self.y + 1][self.x].content, Anthill):
            new_y += 1
        elif direction == "left" and self.x > 0 and not isinstance(field.cells[self.y][self.x - 1].content, Anthill):
            new_x -= 1
        elif direction == "right" and self.x < field.cols - 1 and not isinstance(field.cells[self.y][self.x + 1].content, Anthill):
            new_x += 1

        field.cells[self.y][self.x].content = None
        self.y, self.x = new_y, new_x
        field.cells[self.y][self.x].content = self

    def place_object(self, field):
        if field.cells[self.y][self.x].content is None:
            field.cells[self.y][self.x].content = self
        else:
            empty_cells = [(i, j) for i in range(field.rows) for j in range(field.cols) if field.cells[i][j].content is None]
            if empty_cells:
                new_y, new_x = random.choice(empty_cells)
                field.cells[new_y][new_x].content = self
                self.y, self.x = new_y, new_x
            else:
                print(f"Нету места для {self.image}!")

    def draw(self, field): # отрисовка
        field.cells[self.y][self.x].content = self


class Cell:
    def __init__(self, Y=None, X=None):
        self.image = EMPTY
        self.Y = Y
        self.X = X
        self.content = None

    def draw(self):
        if self.content:
            print(self.content.image, end=" ")
        else:
            print(self.image, end=" ")


class Player(GameObject):
    def __init__(self, y=None, x=None):
        super().__init__(y, x, PLAYER)

    def move(self, direction, field):
        super().move(direction, field)

class Ant(GameObject):
    def __init__(self, y, x):
        super().__init__(y, x, ANT)
        self.direction = random.choice(["up", "down", "left", "right"])
    
    def update_direction(self):
        self.direction = random.choice(["up", "down", "left", "right"])

    def move(self, field):
        new_y, new_x = self.y, self.x


        if self.direction == "up" and self.y > 0 and not isinstance(field.cells[self.y - 1][self.x].content, Anthill):
            new_y -= 1
        elif self.direction == "down" and self.y < field.rows - 1 and not isinstance(field.cells[self.y + 1][self.x].content, Anthill):
            new_y += 1
        elif self.direction == "left" and self.x > 0 and not isinstance(field.cells[self.y][self.x - 1].content, Anthill):
            new_x -= 1
        elif self.direction == "right" and self.x < field.cols - 1 and not isinstance(field.cells[self.y][self.x + 1].content, Anthill):
            new_x += 1

        field.cells[self.y][self.x].content = None
        self.y, self.x = new_y, new_x
        field.cells[self.y][self.x].content = self


class Anthill(GameObject):
    def __init__(self, x, y, quantity):
        super().__init__(y, x, ANTHILL)
        self.quantity = quantity
        self.spawn_counter = 0
        self.ants_counter = ANTS_IN_ANTHILL_MAX

    def place(self, field):
        super().place_object(field)

    def draw(self, field):
        super().draw(field)


class Field:
    def __init__(self, cell=Cell, player=Player, anthill=Anthill):
        self.game_over = False
        self.rows = ROWS
        self.cols = COLS
        self.anthills = []
        self.cells = [[cell(Y=y, X=x) for x in range(COLS)] for y in range(ROWS)]
        self.player = player(y=random.randint(0, ROWS - 1), x=random.randint(0, COLS - 1))
        self.player.place_object(self)
        self.player.draw(self)

    def drawrows(self): # отрисовывает ряды и строки 
        for row in self.cells:
            for cell in row:
                cell.draw()
            print()

    def add_anthill(self, anthill): # добавление в поле муравейника
        self.anthills.append(anthill)
        anthill.place_object(self)

    def add_anthills(self):
        """ спавн муравейников """
        available_cells = [(x, y) for x in range(self.cols) for y in range(self.rows) if (x, y) != (self.player.x, self.player.y)]

        quantity = random.randint(ANTHILL_MIN, ANTHILL_MAX)

        for i in range(quantity):
            if not available_cells:
                break
            anthill_x, anthill_y = random.choice(available_cells)
            available_cells.remove((anthill_x, anthill_y))

            anthill = Anthill(x=anthill_x, y=anthill_y, quantity=random.randint(ANTHILL_MIN, ANTHILL_MAX))
            self.add_anthill(anthill)
    

    def spawn_ants(self):
        """ спавн муравьeв """
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

    def move_ants(self):
        """ передвижение муравья """
        for row in self.cells:
            for cell in row:
                if cell.content and isinstance(cell.content, Ant):
                    ant = cell.content
                    ant.move(self)
                    ant.update_direction()

        # Проверка на наличие муравьев во всех муравейниках
        total_ants = sum(anthill.ants_counter for anthill in self.anthills)

        # Проверка на наличие муравьев на поле
        ants_on_field = any(cell.content and isinstance(cell.content, Ant) for row in self.cells for cell in row)

        if total_ants == 0 and not ants_on_field:
            self.game_over = True

def clear_screen():
    """ очистка экрана """
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


class Game:
    def __init__(self):
        self.field = Field()
        self.field.add_anthills()
        self.ants_eaten = 0
        self.ants_escaped = 0
        self.dop_bals = 0

    def keyboard_event(self, event):
        """ события происходящи при нажатии клавиш """
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == "up":
                self.field.player.move("up", self.field)
            elif event.name == "down":
                self.field.player.move("down", self.field)
            elif event.name == "left":
                self.field.player.move("left", self.field)
            elif event.name == "right":
                self.field.player.move("right", self.field)
            elif event.name == "esc":
                print("♦ Вы вышли из игры ♦")
                return True
            elif event.name == "l" or "k":
                self.dop_bals += 1
        return False

    def update_game_state(self):
        clear_screen()
        self.field.drawrows()
        self.field.spawn_ants()
        self.field.move_ants()

        if self.field.game_over:
            self.statistics()

    def statistics(self):
        """ статистика игры """
        self.total_ants_eaten = sum(anthill.quantity - anthill.ants_counter for anthill in self.field.anthills) #всего съедено муравьев
        escaped_ants = ANTS_IN_ANTHILL_MAX - self.total_ants_eaten

        print(f"\n♦ Игра закончена! Статистика: ♦")
        print(f"♦ Съедено муравьёв ♦: {self.total_ants_eaten}")
        print(f"♦ Сбежало муравьёв ♦: {escaped_ants}")
        print(f"♦ Баллов: {self.total_ants_eaten}/{ANTS_IN_ANTHILL_MAX} ♦")
        print(f"♦ Доплнительные баллы: {self.dop_bals} ♦")
        if self.total_ants_eaten == ANTS_IN_ANTHILL_MAX:
            print("•◘ Результат: Идеально ◘•")
        elif self.total_ants_eaten + self.dop_bals >= escaped_ants:
            print("•◘ Результат: Хорошо ◘•")
        else:
            print("•◘ Результат: Плохо ◘•")

    def run(self): # запускает игру
        self.field.drawrows()

        while not self.field.game_over:
            event = keyboard.read_event(suppress=True)
            if self.keyboard_event(event):
                break
            os.system("cls")
            self.update_game_state()

game_run = Game()
game_run.run()