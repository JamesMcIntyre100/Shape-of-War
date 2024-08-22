import pygame

from colours import BLUE

# Define Building class
class Building:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect)

# Subclass for specific buildings/units
class TownCenter(Building):
    pass