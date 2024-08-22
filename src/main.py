import pygame
import sys

from display import screen
from buildings import TownCenter
from units import Soldier
from colours import GREEN, RED, WHITE, BLACK

# Initialize Pygame
pygame.init()

pygame.display.set_caption("Shape RTS Game")

# Get the width and height
WIDTH, HEIGHT = screen.get_width(), screen.get_height()

# Initialize game objects
town_center = TownCenter(WIDTH // 2 - 50, HEIGHT // 2 - 50, 100, 100)
units = [Soldier(100, 100, 10, 2), Soldier(200, 150, 10, 2), Soldier(300, 200, 10, 2)]
buildings = [town_center]

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
                        unit.target = target
                # Draw the cross at the target position
                pygame.draw.line(screen, BLACK, (target[0] - 10, target[1]), (target[0] + 10, target[1]), 2)
                pygame.draw.line(screen, BLACK, (target[0], target[1] - 10), (target[0], target[1] + 10), 2)
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
