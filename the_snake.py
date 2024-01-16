from random import randint, choice

import pygame as pg

pg.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE


APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

direct = [UP, DOWN, LEFT, RIGHT]


BOARD_BACKGROUND_COLOR = (0, 0, 0)


SPEED = 5

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject():
    """Родительский класс игровых объектов.
    Служит для инициализациии дочерних классов в игре.

    Методы:
    1. __init__(self, body_color=None)
        Создание объекта.
    2. draw()
        Нужен для переопределения в дочерних классах.

    Атрибуты:
    1. position
        Создаётся внутри конструктора, по умолчанию - центр экрана.
    2. body_color
        Создаётся внутри конструктора, по умолчанию задаётся
        None при создании объекта.
    """

    def __init__(self, body_color=None):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def draw(self, surface):
        """Метод отрисовки объекта.
        Внутри класса Gameobject является нерабочим.
        """
        rect = pg.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pg.draw.rect(surface, self.body_color, rect)
        pg.draw.rect(surface, (93, 216, 228), rect, 1)


class Apple(GameObject):
    """Класс объекта Яблоко, дочерний класс Gameobject.

    Методы:
    1. __init__(body_color=APPLE_COLOR)
        Создание объекта с атрибутами body_color, position.
    2. randomize_position()
        Задаёт случайную позицию Яблоку.
    3. draw()
        Отрисовывает Яблоко на заданной позиции.

    Атрибуты:
    1. position
        Создаётся внутри конструктора при помощи randomize_position().
    2. body_color
        Создаётся внутри конструктора, значение по умолчанию - APPLE_COLOR.
    """

    def __init__(self, body_color=APPLE_COLOR, gameobject=None):
        """Инициализация Яблока."""
        super().__init__(body_color)
        self.randomize_position(gameobject)

    def randomize_position(self, gameobject):
        """Задаёт случайные координаты Яблока.
        Проверяет, чтобы Яблоко не появилось в Змейке,
        переданном в аргументы.
        """
        while True:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

            if self.position in gameobject.positions:
                continue
            else:
                break

    def draw(self, surface):
        """Метод отрисовки Яблока"""
        rect = pg.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pg.draw.rect(surface, self.body_color, rect)
        pg.draw.rect(surface, (93, 216, 228), rect, 1)


class Snake(GameObject):
    """Класс объекта Змейка, дочерний класс Gameobject.

    Методы:
    1. __init__(body_color=SNAKE_COLOR)
        Создание объекта с атрибутами body_color, position, length, direction,
        next_direction.
    2. update_direction()
        Обновляет направление объекта в атрибуте direction.
    3. draw()
        Отрисовывает Змейку.
    4. move()
        Перемещает Змейку по сцене и проверяет положение объекта.
    5. reset()
        Сбрасывает атрибуты Змейки до изначальных.
        Применяется в методе move().

    Атрибуты:
    1. position
        Создаётся внутри конструктора.
        По умолчанию выставлен центр экрана.
    2. body_color
        Создаётся внутри конструктора, значение по умолчанию - SNAKE_COLOR.
    3. length
        Атрибут длинны объекта.
    4. direction
        Определяет направление движения.
        В начале выбирается случайное направление.
    5. next_direction
        Определяет следующие направление объекта.
        Используется в методе update_direction().
    """

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализация Змейки."""
        super().__init__(body_color)
        self.reset()

    def draw(self, surface):
        """Отрисовывает Змейку на экране."""
        for position in self.positions:
            rect = (
                pg.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pg.draw.rect(surface, self.body_color, rect)
            pg.draw.rect(surface, (93, 216, 228), rect, 1)

    def update_direction(self, next_direction):
        """Метод обновления направления Змейки после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию Змейки (координаты каждой секции),
         добавляя новую голову в начало списка.

        Проверяет столкновение Змейки с самой собой.
        """
        head = self.get_head_position()
        new_position = (head[0] + self.direction[0] * GRID_SIZE,
                        head[1] + self.direction[1] * GRID_SIZE)

        # Помогаем змейке появиться в другой части экрана,
        # если она покинула его границы
        if new_position[0] >= SCREEN_WIDTH:
            new_position = (0, head[1] + self.direction[1] * GRID_SIZE)
        elif new_position[0] < 0:
            new_position = (620, head[1] + self.direction[1] * GRID_SIZE)
        elif new_position[1] >= SCREEN_HEIGHT:
            new_position = (head[0] + self.direction[0] * GRID_SIZE, 0)
        elif new_position[1] < 0:
            new_position = (head[0] + self.direction[0] * GRID_SIZE, 460)

        self.positions.insert(0, new_position)
        self.positions.pop()

        if self.positions[0] in self.positions[1:]:
            self.reset()

    def get_head_position(self):
        """Возвращает положение головы."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает Змейки в начальное состояние."""
        self.length = 1
        self.direction = choice(direct)
        self.next_direction = None
        self.positions = [self.position]


def handle_keys(game_object):
    """Определяет нажатие клавиш."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Функция запускает игру."""
    snake = Snake()
    apple = Apple(gameobject=snake)

    while True:
        screen.fill((0, 0, 0))
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        apple.draw(screen)
        snake.draw(screen)
        # Столкновение змеи с яблоком
        if snake.get_head_position() == apple.position:
            snake.positions.insert(snake.length, snake.positions[0])
            snake.length += 1
            apple.randomize_position(snake)

        pg.display.update()


if __name__ == '__main__':
    main()
