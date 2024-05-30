import pygame
import random

# --- Constants ---
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
GRID_SIZE = 40
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
FPS = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Tetris Shapes
TETROMINOES = [
    [  # Square
        [1, 1],
        [1, 1]
    ],
    [  # Line
        [1, 1, 1, 1]
    ],
    [  # T-shape
        [1, 1, 1],
        [0, 1, 0]
    ],
    [  # L-shape
        [1, 0],
        [1, 0],
        [1, 1]
    ],
    [  # Reverse L-shape
        [0, 1],
        [0, 1],
        [1, 1]
    ]
]

# --- Classes ---

class Block:
    def __init__(self, x, y, color=WHITE):
        self.x = x
        self.y = y
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

class Tetromino:
    def __init__(self):
        self.type = random.choice(TETROMINOES)
        self.color = random.choice([GREEN, RED])
        self.rotation = 0
        self.x = GRID_WIDTH // 2 - len(self.type[0]) // 2
        self.y = -2  # Start above the screen

    def draw(self, screen):
        for row_index, row in enumerate(self.type):
            for col_index, cell in enumerate(row):
                if cell:
                    block = Block(self.x + col_index, self.y + row_index, self.color)
                    block.draw(screen)

    def move_down(self):
        self.y += 1

    def move_left(self, grid):
        if self.can_move(grid, -1, 0):
            self.x -= 1

    def move_right(self, grid):
        if self.can_move(grid, 1, 0):
            self.x += 1

    def rotate(self, grid):
        # Transpose the shape matrix (flip rows and columns)
        rotated = list(zip(*self.type[::-1]))
        if self.can_move(grid, 0, 0, rotated):
            self.type = rotated

    def can_move(self, grid, dx, dy, new_shape=None):
        if new_shape is None:
            new_shape = self.type
        for row_index, row in enumerate(new_shape):
            for col_index, cell in enumerate(row):
                if cell:
                    new_x = self.x + col_index + dx
                    new_y = self.y + row_index + dy

                    # Check boundaries
                    if (
                        new_x < 0
                        or new_x >= GRID_WIDTH
                        or new_y >= GRID_HEIGHT
                        or (new_y >= 0 and grid[new_y][new_x])  # Check collision with grid
                    ):
                        return False
        return True

class Frog(Block):
    def __init__(self, x, y):
        super().__init__(x, y, GREEN)

    def move(self, dx, dy, grid):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT and not grid[new_y][new_x]:
            self.x = new_x
            self.y = new_y

# --- Functions ---
def draw_grid(screen):
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (SCREEN_WIDTH, y))

def create_grid():
    return [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def place_tetromino_on_grid(tetromino, grid):
    for row_index, row in enumerate(tetromino.type):
        for col_index, cell in enumerate(row):
            if cell:
                grid[tetromino.y + row_index][tetromino.x + col_index] = Block(
                    tetromino.x + col_index, tetromino.y + row_index, tetromino.color
                )

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris-Frogger")
    clock = pygame.time.Clock()

    grid = create_grid()
    frog = Frog(GRID_WIDTH // 2, GRID_HEIGHT - 1)
    current_tetromino = Tetromino()

    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    frog.move(-1, 0, grid)
                if event.key == pygame.K_RIGHT:
                    frog.move(1, 0, grid)
                if event.key == pygame.K_UP:
                    frog.move(0, -1, grid)
                if event.key == pygame.K_DOWN:
                    frog.move(0, 1, grid)

        # Tetris Logic
        if current_tetromino.can_move(grid, 0, 1):
            current_tetromino.move_down()
        else:
            # Place the tetromino on the grid
            place_tetromino_on_grid(current_tetromino, grid)
            current_tetromino = Tetromino()

        # Drawing
        screen.fill(BLACK)
        draw_grid(screen)
        frog.draw(screen)
        current_tetromino.draw(screen)

        # Draw blocks in the grid
        for row in grid:
            for block in row:
                if block:
                    block.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
