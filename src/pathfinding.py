import pygame
import heapq

def heuristic(a, b):
    return abs(b[0] - a[0]) + abs(b[1] - a[1])

def a_star(start, goal, buildings, units, unit_radius):
    neighbors = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]
    close_set = set()
    came_from = {}
    gscore = {start:0}
    fscore = {start:heuristic(start, goal)}
    open_set = []
    heapq.heappush(open_set, (fscore[start], start))
    
    def is_valid(pos):
        for building in buildings:
            if building.rect.colliderect(pygame.Rect(pos[0] - unit_radius, pos[1] - unit_radius, unit_radius * 2, unit_radius * 2)):
                return False
        for unit in units:
            if ((pos[0] - unit[0])**2 + (pos[1] - unit[1])**2)**0.5 < unit_radius * 2:
                return False
        return True

    while open_set:
        current = heapq.heappop(open_set)[1]
        
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        close_set.add(current)

        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            if not is_valid(neighbor):
                continue
            tentative_g_score = gscore[current] + ((i**2 + j**2)**0.5)
            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue
            
            if tentative_g_score < gscore.get(neighbor, float('inf')) or neighbor not in [i[1]for i in open_set]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = gscore[neighbor] + heuristic(neighbor, goal)
                heapq.heappush(open_set, (fscore[neighbor], neighbor))
    
    return None