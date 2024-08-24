import pygame as pg
from controllableSnake import ControllableSnake
from randomSnake import RandomSnake
from random import randrange

# Constants
WINDOW = 700
TILE_SIZE = 10
BORDER_MARGIN = 25

# Initialize Pygame
pg.init()
screen = pg.display.set_mode([WINDOW] * 2)
clock = pg.time.Clock()

# Create Snake instance
controllable_snake = ControllableSnake(TILE_SIZE, BORDER_MARGIN, WINDOW)
random_snake = RandomSnake(TILE_SIZE, BORDER_MARGIN, WINDOW)

# Timer Setup
SPAWN_FOOD_EVENT = pg.USEREVENT + 1
pg.time.set_timer(SPAWN_FOOD_EVENT, 1500)  # Set timer for every 1.5 seconds
time, time_step = 0, 110

# Game loop
while True:
    # Event handling
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

        # Delegate event handling to the snake
        controllable_snake.handle_event(event)
        random_snake.handle_event(event)

        if event.type == SPAWN_FOOD_EVENT:
            new_food = pg.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
            new_food.center = controllable_snake.get_random_position_in_playable_area()
            controllable_snake.foods.append(new_food)

    # Fill the entire screen with blue
    screen.fill('blue')

    # Fill the playable area with green
    pg.draw.rect(screen, 'green', controllable_snake.playable_area)

    # Move snake
    time_now = pg.time.get_ticks()
    if time_now - time > time_step:
        time = time_now
        controllable_snake.move()
        random_snake.move()
        controllable_snake.check_collision()
        random_snake.check_collision()
        controllable_snake.check_food_collision()
        random_snake.check_food_collision

    # Draw everything
    controllable_snake.draw(screen)
    random_snake.draw(screen)

    pg.display.flip()
    clock.tick(60)
