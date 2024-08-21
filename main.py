import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shape RTS Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Define Building class
class Building:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect)

# Define Unit class
class Unit:
    def __init__(self, x, y, radius, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.selected = False

    def draw(self, surface):
        color = GREEN if self.selected else RED
        pygame.draw.circle(surface, color, (self.x, self.y), self.radius)

    def move_to(self, target):
        dx, dy = target[0] - self.x, target[1] - self.y
        dist = (dx ** 2 + dy ** 2) ** 0.5
        if dist > self.speed:
            dx, dy = dx / dist * self.speed, dy / dist * self.speed
        self.x += dx
        self.y += dy

# Subclass for specific buildings/units
class TownCenter(Building):
    pass

class Soldier(Unit):
    pass

# Initialize game objects
town_center = TownCenter(WIDTH//2 - 50, HEIGHT//2 - 50, 100, 100)
units = [Soldier(100, 100, 10, 2), Soldier(200, 150, 10, 2), Soldier(300, 200, 10, 2)]

# Selection box variables
selecting = False
selection_rect = pygame.Rect(0, 0, 0, 0)

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                selecting = True
                start_pos = event.pos
                selection_rect.topleft = start_pos
            elif event.button == 3:  # Right click
                target = event.pos
                for unit in units:
                    if unit.selected:
                        unit.move_to(target)
                pygame.draw.line(screen, BLACK, target, (target[0], target[1]-15), 2)
                pygame.display.update()
                pygame.time.wait(200)  # Display cross for a moment

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left click released
                selecting = False
                # Check for units within the selection rectangle
                for unit in units:
                    if selection_rect.collidepoint(unit.x, unit.y):
                        unit.selected = True
                    else:
                        unit.selected = False
                selection_rect.width = selection_rect.height = 0  # Reset selection rectangle

        elif event.type == pygame.MOUSEMOTION and selecting:
            # Update selection rectangle size
            end_pos = event.pos
            selection_rect.width = end_pos[0] - start_pos[0]
            selection_rect.height = end_pos[1] - start_pos[1]

    # Draw the town center and units
    town_center.draw(screen)
    for unit in units:
        unit.draw(screen)

    # Draw the selection rectangle if selecting
    if selecting:
        pygame.draw.rect(screen, BLACK, selection_rect, 2)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
