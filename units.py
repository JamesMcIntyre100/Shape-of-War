import pygame

from colours import GREEN, RED

# Define Unit class
class Unit:
    def __init__(self, x, y, radius, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.selected = False
        self.target = None

    def draw(self, surface):
        color = GREEN if self.selected else RED
        pygame.draw.circle(surface, color, (self.x, self.y), self.radius)

    def move(self):
        if self.target:
            dx, dy = self.target[0] - self.x, self.target[1] - self.y
            dist = (dx ** 2 + dy ** 2) ** 0.5
            if dist > self.speed:
                dx, dy = dx / dist * self.speed, dy / dist * self.speed
                self.x += dx
                self.y += dy
            else:
                self.target = None  # Stop moving when the target is reached



class Soldier(Unit):
    pass