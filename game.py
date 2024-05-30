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
import pygame
import random

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

# Tetris grid dimensions
GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 30

# Frogger lane dimensions
LANE_HEIGHT = BLOCK_SIZE
LANE_COUNT = 5
SAFE_ZONE_HEIGHT = 5 * BLOCK_SIZE

# Game speed
FPS = 30
FALL_SPEED = 0.25
MOVE_DOWN_SPEED = 0.1

# Tetris shapes
SHAPES = [
    [  # I-shape
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0]
    ],
    [  # J-shape
        [0, 1, 0],
        [0, 1, 0],
        [1, 1, 0]
    ],
    [  # L-shape
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 1]
    ],
    [  # O-shape
        [1, 1],
        [1, 1]
    ],
    [  # S-shape
        [0, 1, 1],
        [1, 1, 0],
        [0, 0, 0]
    ],
    [  # T-shape
        [1, 1, 1],
        [0, 1, 0],
        [0, 0, 0]
    ],
    [  # Z-shape
        [1, 1, 0],
        [0, 1, 1],
        [0, 0, 0]
    ]
]

# Frogger obstacles
OBSTACLE_TYPES = [
    {
        'color': RED,
        'speed': 2,
        'width': 2 * BLOCK_SIZE
    },
    {
        'color': GREEN,
        'speed': -1,
        'width': 3 * BLOCK_SIZE
    }
]

class TetrisPiece:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.randint(1, 3)
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = -2  # Start above the grid

    def draw(self, screen):
        for row_index, row in enumerate(self.shape):
            for col_index, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        screen,
                        self.color,
                        (
                            (self.x + col_index) * BLOCK_SIZE,
                            (self.y + row_index) * BLOCK_SIZE,
                            BLOCK_SIZE,
                            BLOCK_SIZE
                        ),
                        2  # Draw only the border
                    )


class FroggerPlayer:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - BLOCK_SIZE
        self.color = BLUE

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, BLOCK_SIZE, BLOCK_SIZE))

    def move(self, dx, dy):
        self.x += dx * BLOCK_SIZE
        self.y += dy * BLOCK_SIZE

        # Keep player within bounds
        self.x = max(0, min(self.x, SCREEN_WIDTH - BLOCK_SIZE))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - BLOCK_SIZE))


class Obstacle:
    def __init__(self, lane_index, obstacle_type):
        self.lane_index = lane_index
        self.type = obstacle_type
        self.x = random.randint(0, SCREEN_WIDTH - self.type['width'])
        self.y = LANE_HEIGHT + lane_index * LANE_HEIGHT

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            self.type['color'],
            (self.x, self.y, self.type['width'], LANE_HEIGHT)
        )

    def update(self):
        self.x += self.type['speed']
        # Wrap around the screen
        if self.x > SCREEN_WIDTH:
            self.x -= SCREEN_WIDTH + self.type['width']
        elif self.x + self.type['width'] < 0:
            self.x += SCREEN_WIDTH + self.type['width']


def draw_grid(screen):
    for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (SCREEN_WIDTH, y))

def check_collision(player, obstacles):
    for obstacle in obstacles:
        if player.x < obstacle.x + obstacle.type['width'] and \
           player.x + BLOCK_SIZE > obstacle.x and \
           player.y < obstacle.y + LANE_HEIGHT and \
           player.y + BLOCK_SIZE > obstacle.y:
            return True
    return False

def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris-Frogger Mashup")
    clock = pygame.time.Clock()

    # Game variables
    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    current_piece = TetrisPiece()
    player = FroggerPlayer()
    obstacles = [
        Obstacle(lane_index, random.choice(OBSTACLE_TYPES)) for lane_index in range(LANE_COUNT)
    ]
    game_over = False

    while not game_over:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move(-1, 0)
                if event.key == pygame.K_RIGHT:
                    player.move(1, 0)
                if event.key == pygame.K_UP:
                    player.move(0, -1)
                if event.key == pygame.K_DOWN:
                    player.move(0, 1)

        # Update game state
        # ... (Tetris piece movement, collision detection, line clearing)
        # ... (Frogger player collision detection)

        # Update obstacles
        for obstacle in obstacles:
            obstacle.update()

        # Check for Frogger collision
        if check_collision(player, obstacles):
            game_over = True  # Game over if collision occurs

        # Render the game
        screen.fill(BLACK)
        draw_grid(screen)

        # ... (Draw Tetris pieces, Frogger player, and obstacles)

        current_piece.draw(screen)
        player.draw(screen)
        for obstacle in obstacles:
            obstacle.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
import pygame
import random

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Block sizes
BLOCK_SIZE = 40

# Frogger settings
FROG_SIZE = 30
FROG_SPEED = 20

# Controls
CONTROLS = {
    "frog": {
        "up": pygame.K_UP,
        "down": pygame.K_DOWN,
        "left": pygame.K_LEFT,
        "right": pygame.K_RIGHT,
    },
    "blocks": {
        "speed_up": pygame.K_SPACE,
        "speed_down": pygame.K_LSHIFT,
    },
}


class Block:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def move(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.y = -BLOCK_SIZE
            self.x = random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE, BLOCK_SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, BLOCK_SIZE, BLOCK_SIZE))


class Frog:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, direction):
        if direction == "up" and self.y > 0:
            self.y -= FROG_SPEED
        elif direction == "down" and self.y < SCREEN_HEIGHT - FROG_SIZE:
            self.y += FROG_SPEED
        elif direction == "left" and self.x > 0:
            self.x -= FROG_SPEED
        elif direction == "right" and self.x < SCREEN_WIDTH - FROG_SIZE:
            self.x += FROG_SPEED

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, FROG_SIZE, FROG_SIZE))


def check_collision(frog, blocks):
    for block in blocks:
        if (
            frog.x < block.x + BLOCK_SIZE
            and frog.x + FROG_SIZE > block.x
            and frog.y < block.y + BLOCK_SIZE
            and frog.y + FROG_SIZE > block.y
        ):
            return True
    return False


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris-Frogger Mashup")
    clock = pygame.time.Clock()

    frog = Frog(SCREEN_WIDTH // 2 - FROG_SIZE // 2, SCREEN_HEIGHT - FROG_SIZE * 2)
    blocks = []
    for i in range(10):
        x = random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE, BLOCK_SIZE)
        y = random.randrange(-SCREEN_HEIGHT, 0, BLOCK_SIZE)
        speed = random.randint(1, 5)
        blocks.append(Block(x, y, speed))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # Frog controls
                if event.key == CONTROLS["frog"]["up"]:
                    frog.move("up")
                elif event.key == CONTROLS["frog"]["down"]:
                    frog.move("down")
                elif event.key == CONTROLS["frog"]["left"]:
                    frog.move("left")
                elif event.key == CONTROLS["frog"]["right"]:
                    frog.move("right")

                # Block controls
                elif event.key == CONTROLS["blocks"]["speed_up"]:
                    for block in blocks:
                        block.speed += 1
                elif event.key == CONTROLS["blocks"]["speed_down"]:
                    for block in blocks:
                        block.speed = max(1, block.speed - 1)

        # Move the blocks
        for block in blocks:
            block.move()

        # Check for collisions
        if check_collision(frog, blocks):
            print("Game Over!")
            running = False

        # Draw everything
        screen.fill(BLACK)
        frog.draw(screen)
        for block in blocks:
            block.draw(screen)
        pygame.display.flip()

        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
