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
