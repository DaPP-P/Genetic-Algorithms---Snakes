import pygame as pg
from random import randrange

class RandomSnake:
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
        # Randomly choose a direction to move, ensuring it's not the opposite of current direction
        opposite_direction = (-self.snake_dir[0], -self.snake_dir[1])
        
        while True:
            new_direction = self.direction_map[randrange(0, 4)]
            if new_direction != opposite_direction:
                self.snake_dir = new_direction
                break
        
        self.snake.move_ip(self.snake_dir)
        self.segments.append(self.snake.copy())
        self.segments = self.segments[-self.length:]

    def check_collision(self, other_snake_segments):
        self_eating = pg.Rect.collidelist(self.snake, self.segments[:-1]) != -1
        snake_outside = not self.playable_area.contains(self.snake)
        collision_with_other_snake = pg.Rect.collidelist(self.snake, other_snake_segments) != -1

        
        if snake_outside or self_eating or collision_with_other_snake:
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


    def check_food_collision(self, food_items):
        for food in food_items[:]:
            if self.snake.colliderect(food):
                food_items.remove(food)
                self.length += 1

    def draw(self, screen):
        pg.draw.rect(screen, 'red', self.segments[-1])  # Draw the head in red
        for segment in self.segments[:-1]:  # Draw the body segments in a lighter color
            pg.draw.rect(screen, (255, 102, 102), segment)  # Using a light red for the body


    def handle_event(self, event):
        """Handle key events to change the snake's direction."""
