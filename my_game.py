import pygame as pg
from random import randrange

# Constants
WINDOW = 700
TILE_SIZE = 10
BORDER_MARGIN = 25
RANGE = (
    TILE_SIZE // 2 + BORDER_MARGIN,
    WINDOW - TILE_SIZE // 2 - BORDER_MARGIN,
    TILE_SIZE,
)

# World Setup
playable_area = pg.Rect(BORDER_MARGIN, BORDER_MARGIN, WINDOW - 2 * BORDER_MARGIN, WINDOW - 2 * BORDER_MARGIN)

# Function to generate a random position within the playable area
def get_random_position_in_playable_area():
    while True:
        pos = [randrange(*RANGE), randrange(*RANGE)]
        # Create a temporary rect to check position
        temp_rect = pg.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
        temp_rect.center = pos
        if playable_area.contains(temp_rect):
            return pos
        
# Snake Setup
get_random_position = lambda: [randrange(*RANGE), randrange(*RANGE)]
snake = pg.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
snake.center = get_random_position_in_playable_area()
length = 3  # Set initial length to 3
segments = [snake.copy()]

# Choose a random initial direction
starterDir = randrange(0, 4)  # 0, 1, 2, 3 representing 'right', 'left', 'up', 'down'
direction_map = {
    0: (TILE_SIZE, 0),  # Right
    1: (-TILE_SIZE, 0),  # Left
    2: (0, -TILE_SIZE),  # Up
    3: (0, TILE_SIZE)   # Down
}

# Set initial direction
snake_dir = direction_map[starterDir]

# Position initial segments based on the chosen direction
for _ in range(1, length):
    new_segment = snake.copy()
    if starterDir == 0:  # Right
        new_segment.x -= TILE_SIZE * _
    elif starterDir == 1:  # Left
        new_segment.x += TILE_SIZE * _
    elif starterDir == 2:  # Up
        new_segment.y += TILE_SIZE * _
    elif starterDir == 3:  # Down
        new_segment.y -= TILE_SIZE * _
    segments.insert(0, new_segment)

time, time_step = 0, 110

# Food Setup
food = snake.copy()
food.center = get_random_position_in_playable_area()
foods = [food]  # List to keep track of multiple food pieces

# Pygame Setup
screen = pg.display.set_mode([WINDOW] * 2)
clock = pg.time.Clock()
dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}

# Timer Setup
SPAWN_FOOD_EVENT = pg.USEREVENT + 1
pg.time.set_timer(SPAWN_FOOD_EVENT, 1500)  # Set timer for every 1.5 seconds

# Game stuff
while True:

    # If quits
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()

        # Movements
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w and dirs[pg.K_w]:
                snake_dir = (0, -TILE_SIZE)
                dirs = {pg.K_w: 1, pg.K_s: 0, pg.K_a: 1, pg.K_d: 1}
            if event.key == pg.K_s and dirs[pg.K_s]:
                snake_dir = (0, TILE_SIZE)
                dirs = {pg.K_w: 0, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
            if event.key == pg.K_a and dirs[pg.K_a]:
                snake_dir = (-TILE_SIZE, 0)
                dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 0}
            if event.key == pg.K_d and dirs[pg.K_d]:
                snake_dir = (TILE_SIZE, 0)
                dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 0, pg.K_d: 1}
        if event.type == SPAWN_FOOD_EVENT:
            new_food = snake.copy()
            new_food.center = get_random_position_in_playable_area()
            foods.append(new_food)

    # Fill the entire screen with blue
    screen.fill('blue')

    # Fill the playable area with green
    pg.draw.rect(screen, 'green', playable_area)

    # Draw snake
    pg.draw.rect(screen, 'black', segments[-1])  # Draw the head in black
    for segment in segments[:-1]:  # Draw the body segments in a lighter color
        pg.draw.rect(screen, (65, 65, 65), segment)  # Using a dark gray for body


    # Draw food
    for f in foods:
        pg.draw.rect(screen, 'white', f)    

    # Move snake
    time_now = pg.time.get_ticks()
    if time_now - time > time_step:
        time = time_now
        snake.move_ip(snake_dir)
        segments.append(snake.copy())
        segments = segments[-length:]

    # Checks borders and self-eating
    self_eating = pg.Rect.collidelist(snake, segments[:-1]) != -1
    snake_outside = not playable_area.contains(snake)
    
    if snake_outside or self_eating:
        snake.center = get_random_position()
        length = 3
        starterDir = randrange(0, 4)  # Randomize direction again on reset
        snake_dir = direction_map[starterDir]
        segments = [snake.copy()]
        for _ in range(1, length):
            new_segment = snake.copy()
            if starterDir == 0:  # Right
                new_segment.x -= TILE_SIZE * _
            elif starterDir == 1:  # Left
                new_segment.x += TILE_SIZE * _
            elif starterDir == 2:  # Up
                new_segment.y += TILE_SIZE * _
            elif starterDir == 3:  # Down
                new_segment.y -= TILE_SIZE * _
            segments.insert(0, new_segment)
        foods = [food]  # Reset food to a single piece

    # Check food collision
    for f in foods[:]:
        if snake.colliderect(f):
            foods.remove(f)
            length += 1

    pg.display.flip()
    clock.tick(60)
