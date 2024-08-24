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

# Create Food instance that can be beaten by both snakes
food_items = []

# Create a list a of random snakes
no_of_random_snakes = 20
random_snakes = []

# Initialize 10 random snakes
for _ in range(no_of_random_snakes):
    random_snake = RandomSnake(TILE_SIZE, BORDER_MARGIN, WINDOW)
    random_snakes.append(random_snake)

# Timer Setup
SPAWN_FOOD_EVENT = pg.USEREVENT + 1
pg.time.set_timer(SPAWN_FOOD_EVENT, 250)  # Set timer for every 1 second
time, time_step = 0, 150

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
            food_items.append(new_food)

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

        # Move each random snake
        for random_snake in random_snakes:
            random_snake.move()

        # Check collisions for the controllable snake with all random snakes
        for random_snake in random_snakes:
            controllable_snake.check_collision(random_snake.segments)
            random_snake.check_collision(controllable_snake.segments)
            for other_snake in random_snakes:
                if other_snake != random_snake:
                    random_snake.check_collision(other_snake.segments)


        # Check food collisions
        controllable_snake.check_food_collision(food_items)
        for random_snake in random_snakes:
            random_snake.check_food_collision(food_items)

    # Draw snakes
    controllable_snake.draw(screen)

    # Draw all random snakes
    for random_snake in random_snakes:
        random_snake.draw(screen)
    
    # Draw food
    for food in food_items:
        pg.draw.rect(screen, 'white', food)

    pg.display.flip()
    clock.tick(60)
