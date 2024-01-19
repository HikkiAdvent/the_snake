from random import randint, choice


import pygame as pg


# Инициализация PyGame:
pg.init()


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE


# Цвет яблока и змеи
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)


# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
direct = [UP, DOWN, LEFT, RIGHT]
# Цвета фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)


# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)


# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()
screen.fill((0, 0, 0))


class GameObject():
    """Базовый класс, от которого наследуются другие игровые объекты."""

    def __init__(self, body_color=None):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def draw(self):
        """Метод отрисовки объекта"""
        pass


class Apple(GameObject):
    """Класс объекта Яблоко"""

    def __init__(self, body_color=APPLE_COLOR):
        """Инициализация Яблока"""
        print("Class Apple")
        super().__init__(body_color)

    def randomize_position(self, gameobject):
        """Задаёт координаты появления яблока"""
        while True:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

            if self.position in gameobject.positions:
                continue
            else:
                break

    def draw(self, surface):
        """Метод отрисовки объекта"""
        rect = pg.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pg.draw.rect(surface, self.body_color, rect)
        pg.draw.rect(surface, (93, 216, 228), rect, 1)


class Snake(GameObject):
    """Класс объекта Змейка"""

    def __init__(self, body_color=SNAKE_COLOR):
        """инициализация змейки"""
        print("Class Snake")
        super().__init__(body_color)
        self.reset()

    def draw(self, surface, gameobject):
        """Отрисовывает змейку на экране"""
        head = self.get_head_position()
        rect = (
            pg.Rect((head[0], head[1]), (GRID_SIZE, GRID_SIZE))
        )
        pg.draw.rect(surface, self.body_color, rect)
        pg.draw.rect(surface, (93, 216, 228), rect, 1)

    def last_delete(self, surface):
        """Тут будет описание."""
        tail = self.last
        if len(self.positions) >= self.length:
            rect = (
                pg.Rect((tail[0], tail[1]), (GRID_SIZE, GRID_SIZE))
            )
            pg.draw.rect(surface, BOARD_BACKGROUND_COLOR, rect)
            pg.draw.rect(surface, BOARD_BACKGROUND_COLOR, rect, 1)
            self.last = self.positions.pop()

    def update_direction(self, next_direction=None):
        """Метод обновления направления Змейки после нажатия на кнопку."""
        if next_direction:
            self.direction = next_direction

    def move(self, gameobject, surface):
        """Обновляет позицию змейки (координаты каждой секции),
        добавляя новую голову в начало списка
        """
        head = self.get_head_position()
        new_position = (head[0] + self.direction[0] * GRID_SIZE,
                        head[1] + self.direction[1] * GRID_SIZE)

        if new_position[0] >= SCREEN_WIDTH:
            new_position = (0, head[1] + self.direction[1] * GRID_SIZE)
        elif new_position[0] < 0:
            new_position = (620, head[1] + self.direction[1] * GRID_SIZE)
        elif new_position[1] >= SCREEN_HEIGHT:
            new_position = (head[0] + self.direction[0] * GRID_SIZE, 0)
        elif new_position[1] < 0:
            new_position = (head[0] + self.direction[0] * GRID_SIZE, 460)

        self.positions.insert(0, new_position)

        if new_position == gameobject.position:
            gameobject.randomize_position(self)
        elif new_position != gameobject.position:
            self.last_delete(surface)

        if self.positions[0] in self.positions[1:]:
            self.reset()
            surface.fill(BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        """Возвращает положение головы"""
        return self.positions[0]

    def reset(self):
        """сбрасывает змейку в начальное состояние
        после столкновения с самой собой
        """
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
    """Функция запускает игру"""
    apple = Apple()
    snake = Snake()
    apple.randomize_position(snake)

    while True:

        print(len(snake.positions), snake.last)
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move(apple, screen)
        apple.draw(screen)
        snake.draw(screen, apple)

#        # Столкновение змеи с яблоком
#        if snake.positions[0] == apple.position:
#            snake.positions.insert(snake.length, snake.positions[0])
#            snake.length += 1
#            apple.randomize_position()

        pg.display.update()


if __name__ == '__main__':

    main()
