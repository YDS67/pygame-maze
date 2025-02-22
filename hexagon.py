import pygame
import math

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
FPS = 60
G = 0.2  # Gravity
BOUNCE_DAMPING = 0.9

# Hexagon properties
HEX_RADIUS = 200
HEX_CENTER = (WIDTH // 2, HEIGHT // 2)
HEX_ANGLE = 0  # Rotation angle
ROTATION_SPEED = 1  # Degrees per frame

# Ball properties
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_vel = [2, -3]
BALL_RADIUS = 15

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rotating Hexagon with Bouncing Ball")
clock = pygame.time.Clock()

# Function to get hexagon points
def get_hexagon_points(center, radius, angle):
    points = []
    for i in range(6):
        theta = math.radians(angle + i * 60)
        x = center[0] + radius * math.cos(theta)
        y = center[1] + radius * math.sin(theta)
        points.append((x, y))
    return points

# Main loop
running = True
while running:
    screen.fill(WHITE)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Rotate hexagon
    HEX_ANGLE += ROTATION_SPEED
    hex_points = get_hexagon_points(HEX_CENTER, HEX_RADIUS, HEX_ANGLE)
    
    # Update ball position with gravity
    ball_vel[1] += G
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # Check for collisions with hexagon edges
    for i in range(6):
        p1, p2 = hex_points[i], hex_points[(i + 1) % 6]
        edge_vector = (p2[0] - p1[0], p2[1] - p1[1])
        edge_normal = (-edge_vector[1], edge_vector[0])
        edge_length = math.sqrt(edge_vector[0]**2 + edge_vector[1]**2)
        edge_normal = (edge_normal[0] / edge_length, edge_normal[1] / edge_length)
        
        # Check distance to edge
        to_ball = (ball_pos[0] - p1[0], ball_pos[1] - p1[1])
        distance = to_ball[0] * edge_normal[0] + to_ball[1] * edge_normal[1]
        
        if abs(distance) < BALL_RADIUS:
            dot_product = ball_vel[0] * edge_normal[0] + ball_vel[1] * edge_normal[1]
            ball_vel[0] -= 2 * dot_product * edge_normal[0] * BOUNCE_DAMPING
            ball_vel[1] -= 2 * dot_product * edge_normal[1] * BOUNCE_DAMPING
            ball_pos[0] += edge_normal[0] * (BALL_RADIUS - abs(distance))
            ball_pos[1] += edge_normal[1] * (BALL_RADIUS - abs(distance))
    
    # Draw hexagon
    pygame.draw.polygon(screen, BLACK, hex_points, 2)
    
    # Draw ball
    pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS)
    
    # Update display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
