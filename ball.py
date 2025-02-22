import pygame
import math

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 500
BALL_RADIUS = 40
gravity = 0.5
restitution = -0.9  # Bounciness
ground_y = HEIGHT - 50  # Ground level
jump_strength = -16  # Strength of jump

# Ball properties
x, y = WIDTH // 2, BALL_RADIUS + 10
velocity_y = 0
stretch_factor = 1.0
squash_factor = 1.0
bouncing = True

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Rubber Ball")
clock = pygame.time.Clock()

running = True
while running:
    screen.fill((30, 30, 30))  # Background color
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and y + BALL_RADIUS >= ground_y:
                velocity_y = jump_strength  # Jump when space is pressed
    
    # Apply gravity
    velocity_y += gravity
    y += velocity_y
    
    # Collision with ground
    if y + BALL_RADIUS >= ground_y:
        y = ground_y - BALL_RADIUS  # Reset position
        if abs(velocity_y) > 1:
            velocity_y *= restitution  # Reverse velocity
            stretch_factor = 1.3  # Stretch on impact
            squash_factor = 0.7  # Squash on impact
        else:
            velocity_y = 0
            stretch_factor = 1.0
            squash_factor = 1.0
    else:
        stretch_factor = max(1.0, stretch_factor - 0.1)  # Restore shape gradually
        squash_factor = min(1.0, squash_factor + 0.1)
    
    # Draw ball with deformation
    ball_width = int(BALL_RADIUS * 2 * stretch_factor)
    ball_height = int(BALL_RADIUS * 2 * squash_factor)
    ball_surface = pygame.Surface((ball_width, ball_height), pygame.SRCALPHA)
    pygame.draw.ellipse(ball_surface, (255, 69, 0), (0, 0, ball_width, ball_height))
    screen.blit(ball_surface, (x - ball_width // 2, y - ball_height // 2))
    
    # Draw ground
    pygame.draw.rect(screen, (100, 100, 100), (0, ground_y, WIDTH, HEIGHT - ground_y))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
