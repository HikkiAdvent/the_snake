from random import randint, choice

import pygame as pg


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

SPEED = 8

clock = pg.time.Clock()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)


class GameObject():
    """Родительский класс игровых объектов.

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

    def draw(self, surface, position):
        """Метод отрисовки объекта.
        Внутри класса Gameobject является нерабочим.
        """
        rect = pg.Rect(
            (position[0], position[1]),
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

    def __init__(self, gameobject=(), body_color=APPLE_COLOR):
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

            if self.position in gameobject:
                continue
            return


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
    6. last_delete()
        Стирает след змейки.

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
        Определяет следующие направление Змейки.
        Используется в методе update_direction().
    6. last
        Хранит в себе положение хвоста Змейки
    """

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализация Змейки."""
        super().__init__(body_color)
        self.reset()

    def draw(self, surface, color):
        """Отрисовывает Змейку на экране."""
        head = self.get_head_position()
        super().draw(surface, head)
        self.last_delete(surface, color)

    def last_delete(self, surface, color):
        """Стирает след Змейки."""
        rect = (
            pg.Rect((self.last[0], self.last[1]), (GRID_SIZE, GRID_SIZE))
        )
        pg.draw.rect(surface, color, rect)
        pg.draw.rect(surface, color, rect, 1)

    def update_direction(self, next_direction=None):
        """Метод обновления направления Змейки после нажатия на кнопку."""
        if next_direction:
            self.direction = next_direction

    def move(self):
        """Обновляет позицию Змейки, добавляя новую голову в начало списка.

        Проверяет столкновение Змейки с самой собой и выход за границы экрана.
        """
        head = self.get_head_position()
        fir_direction, sec_direction = self.direction
        new_position = ((head[0] + fir_direction * GRID_SIZE) % SCREEN_WIDTH,
                        (head[1] + sec_direction * GRID_SIZE) % SCREEN_HEIGHT)

        self.positions.insert(0, new_position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def get_head_position(self):
        """Возвращает положение головы."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает Змейку в начальное состояние."""
        self.length = 1
        self.direction = choice(direct)
        self.next_direction = None
        self.positions = [self.position]
        self.last = self.positions[-1]


def handle_keys(game_object):
    """Определяет нажатие клавиш."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.update_direction(UP)
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.update_direction(DOWN)
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.update_direction(LEFT)
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.update_direction(RIGHT)


def main():
    """Функция запускает игру."""
    pg.init()
    pg.display.set_caption('Змейка')
    screen.fill(BOARD_BACKGROUND_COLOR)
    snake = Snake()
    apple = Apple(snake.positions)
    apple.draw(screen, apple.position)

    while True:

        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        snake.draw(screen, BOARD_BACKGROUND_COLOR)

        if snake.get_head_position() == apple.position:
            apple.randomize_position(snake.positions)
            apple.draw(screen, apple.position)
            snake.length += 1

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.draw(screen, apple.position)

        pg.display.update()


if __name__ == '__main__':

    main()
