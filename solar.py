import pygame
import math

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
CENTER = (WIDTH // 2, HEIGHT // 2)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = {
    "Mercury": (169, 169, 169),
    "Venus": (255, 223, 186),
    "Earth": (0, 0, 255),
    "Mars": (255, 0, 0),
    "Jupiter": (255, 165, 0),
    "Saturn": (210, 180, 140),
    "Uranus": (173, 216, 230),
    "Neptune": (0, 0, 139)
}

# Planet Data (name: (distance from sun, radius, orbital speed))
PLANETS = {
    "Mercury": (40, 4, 0.04),
    "Venus": (60, 7, 0.03),
    "Earth": (90, 8, 0.02),
    "Mars": (120, 6, 0.015),
    "Jupiter": (180, 14, 0.008),
    "Saturn": (240, 12, 0.006),
    "Uranus": (300, 10, 0.004),
    "Neptune": (360, 9, 0.002)
}

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System Simulation")
clock = pygame.time.Clock()

def draw_planet(name, angle):
    """ Draw a planet at its orbit position."""
    distance, radius, speed = PLANETS[name]
    x = CENTER[0] + int(distance * math.cos(angle))
    y = CENTER[1] + int(distance * math.sin(angle))
    pygame.draw.circle(screen, COLORS[name], (x, y), radius)

def main():
    running = True
    angles = {planet: 0 for planet in PLANETS}
    while running:
        screen.fill(BLACK)
        pygame.draw.circle(screen, (255, 204, 0), CENTER, 30)  # Sun
        
        for planet in PLANETS:
            angles[planet] += PLANETS[planet][2]
            draw_planet(planet, angles[planet])
        
        pygame.display.flip()
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
    pygame.quit()

if __name__ == "__main__":
    main()
