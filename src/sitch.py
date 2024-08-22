
import pygame

from units import Soldier
class state():
    units = [Soldier(100, 100, 10, 2), Soldier(200, 150, 10, 2), Soldier(300, 200, 10, 2)]
    selecting = False
    selection_rect = pygame.Rect(0, 0, 0, 0)
    start_pos = None
    running = True