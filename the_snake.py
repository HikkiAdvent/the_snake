from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE


# Цвет яблока и змеи
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)



APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

direct = [UP, DOWN, LEFT, RIGHT]


BOARD_BACKGROUND_COLOR = (0, 0, 0)


# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
...


def main():
    # Тут нужно создать экземпляры классов.
    ...

    # while True:
        # clock.tick(SPEED)

        # Тут опишите основную логику игры.
        # ...


if __name__ == '__main__':

    main()
