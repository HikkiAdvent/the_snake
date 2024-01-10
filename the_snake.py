from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

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

# Цвета фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
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
        self.randomize_position()

    def randomize_position(self):
        """Задаёт координаты появления яблока"""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, surface):
        """Метод отрисовки объекта"""
        rect = pygame.Rect(
             (self.position[0], self.position[1]),
             (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, (93, 216, 228), rect, 1)


class Snake(GameObject):
    """Класс объекта Змейка"""

    def __init__(self, body_color=SNAKE_COLOR):
        """инициализация змейки"""
        print("Class Snake")
        super().__init__(body_color)
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.positions = [self.position]

    def draw(self, surface):
        """Отрисовывает змейку на экране"""
        for position in self.positions:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, (93, 216, 228), rect, 1)

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки (координаты каждой секции),
        добавляя новую голову в начало списка
        """
        head = self.get_head_position()
        new_position = (head[0] + self.direction[0] * GRID_SIZE, head[1] + self.direction[1] * GRID_SIZE)

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
        """Возвращает положение головы"""
        return self.positions[0]

    def reset(self):
        """сбрасывает змейку в начальное состояние
        после столкновения с самой собой
        """
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]


def handle_keys(game_object):
    """Определяет нажатие клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Функция запускает игру"""
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        screen.fill((0, 0, 0))
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        apple.draw(screen)
        snake.draw(screen)
        # Столкновение змеи с яблоком
        if snake.positions[0] == apple.position:
            snake.positions.insert(snake.length, snake.positions[0])
            snake.length += 1
            apple.randomize_position()

        pygame.display.update()


if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self, surface):
#     rect = pygame.Rect(
#         (self.position[0], self.position[1]),
#         (GRID_SIZE, GRID_SIZE)
#     )
#     pygame.draw.rect(surface, self.body_color, rect)
#     pygame.draw.rect(surface, (93, 216, 228), rect, 1)

# # Метод draw класса Snake
# def draw(self, surface):
#     for position in self.positions[:-1]:
#         rect = (
#             pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
#         )
#         pygame.draw.rect(surface, self.body_color, rect)
#         pygame.draw.rect(surface, (93, 216, 228), rect, 1)

#     # Отрисовка головы змейки
#     head = self.positions[0]
#     head_rect = pygame.Rect((head[0], head[1]), (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(surface, self.body_color, head_rect)
#     pygame.draw.rect(surface, (93, 216, 228), head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(
#             (self.last[0], self.last[1]),
#             (GRID_SIZE, GRID_SIZE)
#         )
#         pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
