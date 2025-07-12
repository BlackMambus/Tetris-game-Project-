import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
COLUMNS = WIDTH // BLOCK_SIZE
ROWS = HEIGHT // BLOCK_SIZE

# Colors
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
COLORS = [(0, 255, 255), (255, 165, 0), (0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0), (128, 0, 128)]

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

# Grid
grid = [[BLACK for _ in range(COLUMNS)] for _ in range(ROWS)]

class Tetromino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = COLUMNS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def valid_move(self, dx, dy):
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    new_x = self.x + j + dx
                    new_y = self.y + i + dy
                    if new_x < 0 or new_x >= COLUMNS or new_y >= ROWS or (new_y >= 0 and grid[new_y][new_x] != BLACK):
                        return False
        return True

    def lock(self):
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    grid[self.y + i][self.x + j] = self.color

def clear_lines():
    global grid
    new_grid = [row for row in grid if any(cell == BLACK for cell in row)]
    lines_cleared = ROWS - len(new_grid)
    for _ in range(lines_cleared):
        new_grid.insert(0, [BLACK for _ in range(COLUMNS)])
    grid = new_grid

def draw_grid():
    for y in range(ROWS):
        for x in range(COLUMNS):
            pygame.draw.rect(screen, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, GRAY, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_tetromino(tetromino):
    for i, row in enumerate(tetromino.shape):
        for j, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, tetromino.color, ((tetromino.x + j) * BLOCK_SIZE, (tetromino.y + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def main():
    running = True
    fall_time = 0
    fall_speed = 500  # milliseconds
    current = Tetromino()

    while running:
        screen.fill(BLACK)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time > fall_speed:
            if current.valid_move(0, 1):
                current.y += 1
            else:
                current.lock()
                clear_lines()
                current = Tetromino()
                if not current.valid_move(0, 0):
                    print("Game Over")
                    running = False
            fall_time = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and current.valid_move(-1, 0):
                    current.x -= 1
                elif event.key == pygame.K_RIGHT and current.valid_move(1, 0):
                    current.x += 1
                elif event.key == pygame.K_DOWN and current.valid_move(0, 1):
                    current.y += 1
                elif event.key == pygame.K_UP:
                    current.rotate()
                    if not current.valid_move(0, 0):
                        current.rotate()
                        current.rotate()
                        current.rotate()

        draw_grid()
        draw_tetromino(current)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()



