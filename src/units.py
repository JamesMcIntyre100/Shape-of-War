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
        
        # Super-sampling factor
        ss_factor = 4
        # Create a high-resolution surface
        high_res_surface = pygame.Surface((self.radius * 2 * ss_factor, self.radius * 2 * ss_factor), pygame.SRCALPHA)
        
        # Draw the high-resolution circle
        pygame.draw.circle(high_res_surface, color, (self.radius * ss_factor, self.radius * ss_factor), self.radius * ss_factor, 3 * ss_factor) # Thickness of 3 pixels
        
        # Scale down the high-resolution surface to fit the original size
        low_res_surface = pygame.transform.smoothscale(high_res_surface, (self.radius * 2, self.radius * 2))
        
        # Blit the low-resolution surface onto the main surface at the correct position
        surface.blit(low_res_surface, (self.x - self.radius, self.y - self.radius))

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
