import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_SPEED = 5
CELL_SIZE = 40
NUM_COLLECTIBLES = 5

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple 2D Maze Game")

# Maze generation using recursive division algorithm
def generate_maze(grid_width, grid_height):
    maze = [[1 for _ in range(grid_width)] for _ in range(grid_height)]
    
    def carve_passages(cx, cy):
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = cx + dx * 2, cy + dy * 2
            if 0 <= nx < grid_width and 0 <= ny < grid_height and maze[ny][nx] == 1:
                maze[cy + dy][cx + dx] = 0
                maze[ny][nx] = 0
                carve_passages(nx, ny)
    
    maze[1][1] = 0
    carve_passages(1, 1)
    return maze

# Function to reset the maze, player position, and collectibles
def reset_game():
    global maze_grid, walls, player, collectibles, level_exits
    maze_grid = generate_maze(WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE)
    walls = [pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE) 
             for y in range(len(maze_grid)) for x in range(len(maze_grid[0])) if maze_grid[y][x] == 1]
    collectibles = []
    
    for y in range(len(maze_grid)):
        for x in range(len(maze_grid[0])):
            if maze_grid[y][x] == 0:
                player = pygame.Rect(x * CELL_SIZE + CELL_SIZE // 4, y * CELL_SIZE + CELL_SIZE // 4, 30, 30)
                break
        else:
            continue
        break
    
    while len(collectibles) < NUM_COLLECTIBLES:
        x, y = random.randint(0, WIDTH // CELL_SIZE - 1), random.randint(0, HEIGHT // CELL_SIZE - 1)
        if maze_grid[y][x] == 0:
            collectibles.append(pygame.Rect(x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2, 10, 10))

# Initialize game
score = 0
level_exits = 0
reset_game()

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(FPS)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Player movement with collision detection
    keys = pygame.key.get_pressed()
    new_x, new_y = player.x, player.y
    if keys[pygame.K_LEFT]:
        new_x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        new_x += PLAYER_SPEED
    if keys[pygame.K_UP]:
        new_y -= PLAYER_SPEED
    if keys[pygame.K_DOWN]:
        new_y += PLAYER_SPEED
    
    temp_player = pygame.Rect(new_x, new_y, player.width, player.height)
    if not any(temp_player.colliderect(wall) for wall in walls):
        player.x, player.y = new_x, new_y
    
    # Check if player exits the screen
    if player.x < 0 or player.x > WIDTH - player.width or player.y < 0 or player.y > HEIGHT - player.height:
        level_exits += 1
        reset_game()
    
    # Check for collectible collisions
    for collectible in collectibles[:]:
        if player.colliderect(collectible):
            collectibles.remove(collectible)
            score += 1
    
    # Drawing
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, player)
    for wall in walls:
        pygame.draw.rect(screen, BLACK, wall)
    for collectible in collectibles:
        pygame.draw.ellipse(screen, RED, collectible)
    
    # Display score and level exits
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, YELLOW)
    exit_text = font.render(f"Level Exits: {level_exits}", True, YELLOW)
    screen.blit(score_text, (10, 10))
    screen.blit(exit_text, (10, HEIGHT-30))
    
    pygame.display.flip()

# Quit pygame
pygame.quit()
