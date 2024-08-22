import pygame
import sys

from display import screen
from inputs import events
from buildings import TownCenter
from colours import WHITE, BLACK
from sitch import state

# Initialize Pygame
pygame.init()

pygame.display.set_caption("Shape RTS Game")

# Get the width and height
WIDTH, HEIGHT = screen.get_width(), screen.get_height()

# Initialize game objects
town_center = TownCenter(WIDTH // 2 - 50, HEIGHT // 2 - 50, 100, 100)
buildings = [town_center]

# Main game loop
clock = pygame.time.Clock()
    

while state.running:
    screen.fill(WHITE)

    state = events(state)

    # Move and draw units
    for unit in state.units:
        unit.move(buildings, state.units)
        unit.draw(screen)

    # Draw the town center
    town_center.draw(screen)

    # Draw the selection rectangle if selecting
    if state.selecting:
        pygame.draw.rect(screen, BLACK, state.selection_rect, 2)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
