import pygame
import random
import sys

# --- Tetris settings ---
TETRIS_GRID_WIDTH = 10
TETRIS_GRID_HEIGHT = 20
TETRIS_BLOCK_SIZE = 30

# --- Frogger settings ---
FROGGER_LANE_HEIGHT = 50
FROGGER_LANE_COUNT = 5
FROGGER_FROG_SIZE = 25

# --- Colors ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# --- Tetris pieces ---
TETROMINOES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 1], [1, 1]],  # O
]


class Tetris:
    def __init__(self):
        self.grid = [[0 for _ in range(TETRIS_GRID_WIDTH)] for _ in range(TETRIS_GRID_HEIGHT)]
        self.current_piece = {"shape": random.choice(TETROMINOES), "x": 3, "y": 0}
        self.next_piece = random.choice(TETROMINOES)
        self.game_over = False

    def draw(self, screen):
        for y in range(TETRIS_GRID_HEIGHT):
            for x in range(TETRIS_GRID_WIDTH):
                if self.grid[y][x]:
                    pygame.draw.rect(
                        screen,
                        RED,
                        (
                            x * TETRIS_BLOCK_SIZE,
                            y * TETRIS_BLOCK_SIZE,
                            TETRIS_BLOCK_SIZE,
                            TETRIS_BLOCK_SIZE,
                        ),
                        1,
                    )
        self.draw_piece(screen, self.current_piece)

    def draw_piece(self, screen, piece):
        for y in range(len(piece["shape"])):
            for x in range(len(piece["shape"][0])):
                if piece["shape"][y][x]:
                    pygame.draw.rect(
                        screen,
                        BLUE,
                        (
                            (piece["x"] + x) * TETRIS_BLOCK_SIZE,
                            (piece["y"] + y) * TETRIS_BLOCK_SIZE,
                            TETRIS_BLOCK_SIZE,
                            TETRIS_BLOCK_SIZE,
                        ),
                    )

    def move_piece_down(self):
        if not self.collision(self.current_piece["x"], self.current_piece["y"] + 1):
            self.current_piece["y"] += 1
        else:
            self.place_piece()

    def move_piece_left(self):
        if not self.collision(self.current_piece["x"] - 1, self.current_piece["y"]):
            self.current_piece["x"] -= 1

    def move_piece_right(self):
        if not self.collision(self.current_piece["x"] + 1, self.current_piece["y"]):
            self.current_piece["x"] += 1

    def rotate_piece(self):
        rotated_piece = list(zip(*self.current_piece["shape"][::-1]))
        if not self.collision(self.current_piece["x"], self.current_piece["y"], rotated_piece):
            self.current_piece["shape"] = rotated_piece

    def collision(self, x, y, piece=None):
        if piece is None:
            piece = self.current_piece["shape"]
        for row in range(len(piece)):
            for col in range(len(piece[0])):
                if piece[row][col]:  # If block exists in the piece
                    grid_x = x + col
                    grid_y = y + row
                    if (
                        grid_x < 0
                        or grid_x >= TETRIS_GRID_WIDTH
                        or grid_y >= TETRIS_GRID_HEIGHT
                    ):  # Out of bounds check
                        return True
                    if grid_y < 0:
                        continue
                    if self.grid[grid_y][grid_x]:  # Collision with existing block
                        return True
        return False

    def place_piece(self):
        for y in range(len(self.current_piece["shape"])):
            for x in range(len(self.current_piece["shape"][0])):
                if self.current_piece["shape"][y][x]:
                    grid_x = self.current_piece["x"] + x
                    grid_y = self.current_piece["y"] + y
                    if 0 <= grid_y < TETRIS_GRID_HEIGHT:  # Make sure it's within the grid
                        self.grid[grid_y][grid_x] = 1
        self.clear_lines()
        self.new_piece()

    def clear_lines(self):
        lines_to_clear = []
        for y in range(TETRIS_GRID_HEIGHT):
            if all(self.grid[y]):
                lines_to_clear.append(y)
        for y in lines_to_clear:
            del self.grid[y]
            self.grid.insert(0, [0 for _ in range(TETRIS_GRID_WIDTH)])

    def new_piece(self):
        self.current_piece = {"shape": self.next_piece, "x": 3, "y": 0}
        self.next_piece = random.choice(TETROMINOES)
        if self.collision(self.current_piece["x"], self.current_piece["y"]):
            self.game_over = True


class Frogger:
    def __init__(self):
        self.frog_x = (
            TETRIS_GRID_WIDTH * TETRIS_BLOCK_SIZE
            + (SCREEN_WIDTH - TETRIS_GRID_WIDTH * TETRIS_BLOCK_SIZE) // 2
            - FROGGER_FROG_SIZE // 2
        )
        self.frog_y = SCREEN_HEIGHT - FROGGER_LANE_HEIGHT - FROGGER_FROG_SIZE // 2
        self.lanes = [
            [
                {"x": random.randint(0, SCREEN_WIDTH - 50), "speed": 2}
                for _ in range(random.randint(1, 3))
            ]
            for _ in range(FROGGER_LANE_COUNT)
        ]

    def draw(self, screen):
        # Draw Frogger section
        pygame.draw.rect(
            screen,
            GREEN,
            (
                TETRIS_GRID_WIDTH * TETRIS_BLOCK_SIZE,
                0,
                SCREEN_WIDTH - TETRIS_GRID_WIDTH * TETRIS_BLOCK_SIZE,
                SCREEN_HEIGHT,
            ),
        )
        # Draw lanes and obstacles
        for i, lane in enumerate(self.lanes):
            for obstacle in lane:
                pygame.draw.rect(
                    screen,
                    BLUE,
                    (
                        obstacle["x"],
                        i * FROGGER_LANE_HEIGHT,
                        50,  # Obstacle width
                        FROGGER_LANE_HEIGHT,
                    ),
                )
                obstacle["x"] += obstacle["speed"]
                if obstacle["x"] > SCREEN_WIDTH:
                    obstacle["x"] = -50
        # Draw frog
        pygame.draw.circle(
            screen, WHITE, (self.frog_x + FROGGER_FROG_SIZE // 2, self.frog_y + FROGGER_FROG_SIZE // 2), FROGGER_FROG_SIZE // 2
        )

    def move_frog(self, dx, dy):
        self.frog_x += dx
        self.frog_y += dy
        # Keep frog within bounds
        self.frog_x = max(
            TETRIS_GRID_WIDTH * TETRIS_BLOCK_SIZE,
            min(self.frog_x, SCREEN_WIDTH - FROGGER_FROG_SIZE),
        )
        self.frog_y = max(0, min(self.frog_y, SCREEN_HEIGHT - FROGGER_FROG_SIZE))


# --- Game initialization ---
pygame.init()
SCREEN_WIDTH = 600
SCREEN_HEIGHT = TETRIS_GRID_HEIGHT * TETRIS_BLOCK_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris-Frogger Mashup")
clock = pygame.time.Clock()
tetris = Tetris()
frogger = Frogger()
fall_speed = 0.25
fall_time = 0

# --- Game loop ---
while True:
    # --- Event handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                tetris.move_piece_left()
            if event.key == pygame.K_RIGHT:
                tetris.move_piece_right()
            if event.key == pygame.K_DOWN:
                tetris.move_piece_down()
            if event.key == pygame.K_UP:
                tetris.rotate_piece()
            # Frogger controls
            if event.key == pygame.K_a:
                frogger.move_frog(-FROGGER_FROG_SIZE, 0)  # Move left
            if event.key == pygame.K_d:
                frogger.move_frog(FROGGER_FROG_SIZE, 0)  # Move right
            if event.key == pygame.K_w:
                frogger.move_frog(0, -FROGGER_LANE_HEIGHT)  # Move up
            if event.key == pygame.K_s:
                frogger.move_frog(0, FROGGER_LANE_HEIGHT)  # Move down

    # --- Game logic ---
    fall_time += clock.get_time() / 1000  # Convert milliseconds to seconds
    if fall_time >= fall_speed:
        fall_time = 0
        tetris.move_piece_down()

    screen.fill(BLACK)

    tetris.draw(screen)
    frogger.draw(screen)

    pygame.display.flip()
    clock.tick(60)  # Limit frame rate to 60 FPS
