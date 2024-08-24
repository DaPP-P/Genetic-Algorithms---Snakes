import pygame as pg
from random import randrange

class ControllableSnake:
    def __init__(self, tile_size, border_margin, window_size):
        self.TILE_SIZE = tile_size
        self.BORDER_MARGIN = border_margin
        self.WINDOW = window_size
        self.RANGE = (
            tile_size // 2 + border_margin,
            window_size - tile_size // 2 - border_margin,
            tile_size,
        )
        self.playable_area = pg.Rect(
            border_margin, border_margin, 
            window_size - 2 * border_margin, 
            window_size - 2 * border_margin
        )
        self.snake = pg.rect.Rect([0, 0, tile_size - 2, tile_size - 2])
        self.food = self.snake.copy()
        self.food.center = self.get_random_position_in_playable_area()
        self.foods = [self.food]
        self.length = 3
        self.direction_map = {
            0: (tile_size, 0),  # Right
            1: (-tile_size, 0),  # Left
            2: (0, -tile_size),  # Up
            3: (0, tile_size)   # Down
        }
        self.starterDir = randrange(0, 4)  # 0: Right, 1: Left, 2: Up, 3: Down
        self.snake_dir = self.direction_map[self.starterDir]
        self.snake.center = self.get_random_position_in_playable_area()
        self.segments = [self.snake.copy()]
        for _ in range(1, self.length):
            new_segment = self.snake.copy()
            if self.starterDir == 0:  # Right
                new_segment.x -= tile_size * _
            elif self.starterDir == 1:  # Left
                new_segment.x += tile_size * _
            elif self.starterDir == 2:  # Up
                new_segment.y += tile_size * _
            elif self.starterDir == 3:  # Down
                new_segment.y -= tile_size * _
            self.segments.insert(0, new_segment)

    def get_random_position_in_playable_area(self):
        while True:
            pos = [randrange(*self.RANGE), randrange(*self.RANGE)]
            temp_rect = pg.rect.Rect([0, 0, self.TILE_SIZE - 2, self.TILE_SIZE - 2])
            temp_rect.center = pos
            if self.playable_area.contains(temp_rect):
                return pos

    def move(self):
        self.snake.move_ip(self.snake_dir)
        self.segments.append(self.snake.copy())
        self.segments = self.segments[-self.length:]

    def check_collision(self):
        self_eating = pg.Rect.collidelist(self.snake, self.segments[:-1]) != -1
        snake_outside = not self.playable_area.contains(self.snake)
        if snake_outside or self_eating:
            self.snake.center = self.get_random_position_in_playable_area()
            self.length = 3
            self.starterDir = randrange(0, 4)  # Randomize direction again on reset
            self.snake_dir = self.direction_map[self.starterDir]
            self.segments = [self.snake.copy()]
            for _ in range(1, self.length):
                new_segment = self.snake.copy()
                if self.starterDir == 0:  # Right
                    new_segment.x -= self.TILE_SIZE * _
                elif self.starterDir == 1:  # Left
                    new_segment.x += self.TILE_SIZE * _
                elif self.starterDir == 2:  # Up
                    new_segment.y += self.TILE_SIZE * _
                elif self.starterDir == 3:  # Down
                    new_segment.y -= self.TILE_SIZE * _
                self.segments.insert(0, new_segment)
            self.food.center = self.get_random_position_in_playable_area()
            self.foods = [self.food]

    def check_food_collision(self):
        for f in self.foods[:]:
            if self.snake.colliderect(f):
                self.foods.remove(f)
                self.length += 1

    def draw(self, screen):
        pg.draw.rect(screen, 'black', self.segments[-1])  # Draw the head in black
        for segment in self.segments[:-1]:  # Draw the body segments in a lighter color
            pg.draw.rect(screen, (65, 65, 65), segment)  # Using a dark gray for body
        for f in self.foods:
            pg.draw.rect(screen, 'white', f)

    def handle_event(self, event):
        """Handle key events to change the snake's direction."""
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w and self.snake_dir != (0, self.TILE_SIZE):
                self.snake_dir = (0, -self.TILE_SIZE)
            elif event.key == pg.K_s and self.snake_dir != (0, -self.TILE_SIZE):
                self.snake_dir = (0, self.TILE_SIZE)
            elif event.key == pg.K_a and self.snake_dir != (self.TILE_SIZE, 0):
                self.snake_dir = (-self.TILE_SIZE, 0)
            elif event.key == pg.K_d and self.snake_dir != (-self.TILE_SIZE, 0):
                self.snake_dir = (self.TILE_SIZE, 0)
