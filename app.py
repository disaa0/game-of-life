import pygame
import numpy as np

# Set up the Pygame window
pygame.init()
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Conway's Game of Life")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Set up the grid
rows, cols = 50, 50
cell_size = min(width // cols, height // rows)
grid = np.zeros((rows, cols))

# Set up the game
def init_game():
    global grid
    grid = np.zeros((rows, cols))

# Draw the grid on the screen
def draw_grid():
    for i in range(rows):
        for j in range(cols):
            x = j * cell_size
            y = i * cell_size
            if grid[i][j] == 1:
                pygame.draw.rect(screen, WHITE, (x, y, cell_size, cell_size))
            else:
                pygame.draw.rect(screen, BLACK, (x, y, cell_size, cell_size), 1)
    # Draw labels
    generation = font.render("Generation: " + str(num_generations), True, WHITE)
    living_cells = font.render("Living cells: " + str(np.sum(grid)), True, WHITE)
    screen.blit(generation, (10, height - 30))
    screen.blit(living_cells, (width - 170, height - 30))

# Get the number of live neighbors for a given cell
def get_live_neighbors(x, y):
    live_neighbors = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if x + i < 0 or x + i >= rows or y + j < 0 or y + j >= cols:
                continue
            if grid[x + i][y + j] == 1:
                live_neighbors += 1
    return live_neighbors

# Update the game state
def update_game():
    global grid, num_generations
    new_grid = np.zeros((rows, cols))
    for i in range(rows):
        for j in range(cols):
            live_neighbors = get_live_neighbors(i, j)
            if grid[i][j] == 1 and (live_neighbors == 2 or live_neighbors == 3):
                new_grid[i][j] = 1
            elif grid[i][j] == 0 and live_neighbors == 3:
                new_grid[i][j] = 1
    grid = new_grid
    num_generations += 1

# Main game loop
init_game()
running = True
adding_cells = True
font = pygame.font.SysFont('freesansbold.ttf', 30)
num_generations = 0
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and adding_cells:
            x, y = pygame.mouse.get_pos()
            i = y // cell_size
            j = x // cell_size
            if grid[i][j] == 0:
                grid[i][j] = 1
            else:
                grid[i][j] = 0
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            adding_cells = not adding_cells
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            num_generations = 0
            adding_cells = True
            init_game()
            

    # Update the game state and draw the grid
    if not adding_cells:
        update_game()
    screen.fill(BLACK)
    draw_grid()
    if adding_cells:
        pygame.draw.rect(screen, GRAY, (0, 0, width, height), 1)
    pygame.display.update()

    # Wait for a short time before updating the screen
    pygame.time.wait(100)

# Clean up
pygame.quit()