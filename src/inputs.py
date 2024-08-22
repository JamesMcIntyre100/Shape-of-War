import pygame

from display import screen
from colours import BLACK

# Event handling
def events(units, start_pos, running):
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
    
    return selecting, selection_rect, start_pos, running