import pygame
import time

from colours import GREEN, RED
from pathfinding import a_star

# Define Unit class
class Unit:
    def __init__(self, x, y, radius, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.selected = False
        self.target = None
        self.path = None
        self.last_path_calculation = 0
        self.path_calculation_cooldown = 1  # seconds

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

    def move(self, buildings, units, screen_width, screen_height):
        current_time = time.time()
        if self.target:
            if not self.path:
                if current_time - self.last_path_calculation > self.path_calculation_cooldown:
                    other_units = [(u.x, u.y) for u in units if u != self]
                    self.path = a_star((int(self.x), int(self.y)), self.target, buildings, other_units, self.radius)
                    self.last_path_calculation = current_time
                    if self.path:
                        self.path.pop(0)  # Remove starting position
                        self.smooth_path(buildings, units, screen_width, screen_height)
            if self.path:
                next_pos = self.path[0]
                dx, dy = next_pos[0] - self.x, next_pos[1] - self.y
                dist = (dx ** 2 + dy ** 2) ** 0.5
                
                if dist <= self.speed:
                    new_x, new_y = next_pos
                else:
                    new_x = self.x + (dx / dist) * self.speed
                    new_y = self.y + (dy / dist) * self.speed

                # Check for collisions
                if not self.check_collision(new_x, new_y, buildings, units, screen_width, screen_height):
                    self.x, self.y = new_x, new_y
                    if (int(self.x), int(self.y)) == self.path[0]:
                        self.path.pop(0)
                else:
                    # If collision detected, recalculate path less frequently
                    self.path = None
            else:
                self.target = None

    def check_collision(self, new_x, new_y, buildings, units, screen_width, screen_height):
        # Check screen boundaries
        if new_x - self.radius < 0 or new_x + self.radius > screen_width or \
           new_y - self.radius < 0 or new_y + self.radius > screen_height:
            return True

        # Check collision with buildings
        new_rect = pygame.Rect(new_x - self.radius, new_y - self.radius, self.radius * 2, self.radius * 2)
        for building in buildings:
            if new_rect.colliderect(building.rect):
                return True

        # Check collision with other units
        for unit in units:
            if unit != self:
                distance = ((new_x - unit.x) ** 2 + (new_y - unit.y) ** 2) ** 0.5
                if distance < self.radius + unit.radius:
                    return True

        return False
    
    def smooth_path(self, buildings, units, screen_width, screen_height):
        if len(self.path) < 3:
            return

        i = 0
        while i < len(self.path) - 2:
            start = self.path[i]
            end = self.path[i + 2]
            if not any(self.check_collision(x, y, buildings, units, screen_width, screen_height)
                    for x, y in self.interpolate(start, end)):
                self.path.pop(i + 1)
            else:
                i += 1

        def interpolate(self, start, end):
            dx = end[0] - start[0]
            dy = end[1] - start[1]
            dist = max(abs(dx), abs(dy))
            for i in range(dist):
                yield (start[0] + dx * i / dist, start[1] + dy * i / dist)

    def interpolate(self, start, end):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        dist = max(abs(dx), abs(dy))
        for i in range(dist):
            yield (start[0] + dx * i / dist, start[1] + dy * i / dist)

# Subclass for specific units
class Soldier(Unit):
    pass
