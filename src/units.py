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
        # Set the color based on whether the unit is selected or not
        color = GREEN if self.selected else RED
        # Draw the circle outline with a specified border thickness
        pygame.draw.circle(surface, color, (self.x, self.y), self.radius, 3)  # Thickness of 3 pixels

    def move(self, buildings, units):
        if self.target:
            dx, dy = self.target[0] - self.x, self.target[1] - self.y
            dist = (dx ** 2 + dy ** 2) ** 0.5
            if dist > self.speed:
                dx, dy = dx / dist * self.speed, dy / dist * self.speed
            
            # Predict the new position after moving
            new_x = self.x + dx
            new_y = self.y + dy

            # Check for collisions with buildings
            new_rect = pygame.Rect(new_x - self.radius, new_y - self.radius, self.radius * 2, self.radius * 2)
            for building in buildings:
                if new_rect.colliderect(building.rect):
                    return  # Stop movement if collision with building is detected

            # Check for collisions with other units using circle distance
            for unit in units:
                if unit != self:  # Avoid self-collision
                    distance_to_unit = ((new_x - unit.x) ** 2 + (new_y - unit.y) ** 2) ** 0.5
                    if distance_to_unit < self.radius + unit.radius:
                        return  # Stop movement if collision with another unit is detected

            # Move to the new position if no collisions
            self.x = new_x
            self.y = new_y
        else:
            self.target = None  # Stop moving when the target is reached

# Subclass for specific units
class Soldier(Unit):
    pass
