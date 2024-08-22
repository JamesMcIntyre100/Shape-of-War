import pygame

from display import screen
from colours import BLACK

# Event handling
def events(state):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                state.selecting = True
                state.start_pos = event.pos
                state.selection_rect.topleft = state.start_pos
            elif event.button == 3:  # Right click
                target = event.pos
                for unit in state.units:
                    if unit.selected:
                        unit.target = target
                # Draw the cross at the target position
                pygame.draw.line(screen, BLACK, (target[0] - 10, target[1]), (target[0] + 10, target[1]), 2)
                pygame.draw.line(screen, BLACK, (target[0], target[1] - 10), (target[0], target[1] + 10), 2)
                pygame.display.update()
                pygame.time.wait(200)  # Display cross for a moment

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left click released
                state.selecting = False
                # Check for units within the selection rectangle
                for unit in state.units:
                    if state.selection_rect.collidepoint(unit.x, unit.y):
                        unit.selected = True
                    else:
                        unit.selected = False
                state.selection_rect.width = state.selection_rect.height = 0  # Reset selection rectangle

        elif event.type == pygame.MOUSEMOTION and state.selecting:
            # Update selection rectangle size
            end_pos = event.pos
            state.selection_rect.width = end_pos[0] - state.start_pos[0]
            state.selection_rect.height = end_pos[1] - state.start_pos[1]
    
    return state