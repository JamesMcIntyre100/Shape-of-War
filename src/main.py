import pygame
import sys

from display import screen
from inputs import events
from buildings import TownCenter
from units import Soldier
from colours import WHITE, BLACK

# Initialize Pygame
pygame.init()

pygame.display.set_caption("Shape RTS Game")

# Get the width and height
WIDTH, HEIGHT = screen.get_width(), screen.get_height()

# Initialize game objects
town_center = TownCenter(WIDTH // 2 - 50, HEIGHT // 2 - 50, 100, 100)
units = [Soldier(100, 100, 10, 2), Soldier(200, 150, 10, 2), Soldier(300, 200, 10, 2)]
buildings = [town_center]

# Initialize selection variables
selecting = False
selection_rect = pygame.Rect(0, 0, 0, 0)
start_pos = None
running = True

# Main game loop
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)

    selecting, selection_rect, start_pos, running = events(units, start_pos, running)

    # Move and draw units
    for unit in units:
        unit.move(buildings, units)
        unit.draw(screen)

    # Draw the town center
    town_center.draw(screen)

    # Draw the selection rectangle if selecting
    if selecting:
        pygame.draw.rect(screen, BLACK, selection_rect, 2)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
