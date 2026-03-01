import pygame
import random
import time
import math
from queue import PriorityQueue


WIDTH = 1000 # Increased width for the UI Sidebar
GRID_WIDTH = 800
ROWS = 40
NODE_WIDTH = GRID_WIDTH // ROWS
WIN = pygame.display.set_mode((WIDTH, GRID_WIDTH))
pygame.display.set_caption("Dynamic Pathfinding Agent - FAST CFD")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
GREY = (128, 128, 128)
TEXT_COLOR = (200, 200, 200)

pygame.font.init()
FONT = pygame.font.SysFont("consolas", 18)

class Node:
    def __init__(self, row, col):
        self.row, self.col = row, col
        self.x, self.y = row * NODE_WIDTH, col * NODE_WIDTH
        self.color = WHITE
        self.neighbors = []

    def get_pos(self): return self.row, self.col
    def is_wall(self): return self.color == BLACK
    def make_start(self): self.color = BLUE
    def make_wall(self): self.color = BLACK
    def make_goal(self): self.color = PURPLE
    def make_visited(self): 
        if self.color not in [BLUE, PURPLE]: self.color = RED
    def make_frontier(self):
        if self.color not in [BLUE, PURPLE]: self.color = YELLOW
    def make_path(self):
        if self.color not in [BLUE, PURPLE]: self.color = GREEN
    def reset(self): self.color = WHITE
    def draw(self, win): pygame.draw.rect(win, self.color, (self.x, self.y, NODE_WIDTH, NODE_WIDTH))

    def update_neighbors(self, grid):
        self.neighbors = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dr, dc in directions:
            r, c = self.row + dr, self.col + dc
            if 0 <= r < ROWS and 0 <= c < ROWS and not grid[r][c].is_wall():
                self.neighbors.append(grid[r][c])

# --- Heuristics ---
def h_manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def h_euclidean(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# --- UI Rendering ---
def draw_ui(win, metrics, mode, heuristic):
    pygame.draw.rect(win, (30, 30, 30), (GRID_WIDTH, 0, WIDTH - GRID_WIDTH, GRID_WIDTH))
    
    texts = [
        f"ALGO: {mode}",
        f"HEURISTIC: {heuristic}",
        "--- METRICS ---",
        f"Nodes Visited: {metrics['visited']}",
        f"Path Cost: {metrics['cost']}",
        f"Time: {metrics['time']:.2f}ms",
        "--- CONTROLS ---",
        "SPACE: Start Search",
        "M: Toggle Manhattan/Euclidean",
        "G: Toggle A*/Greedy",
        "R: Random Map (30%)",
        "C: Clear Grid"
    ]
    
    for i, text in enumerate(texts):
        render = FONT.render(text, True, TEXT_COLOR)
        win.blit(render, (GRID_WIDTH + 10, 20 + (i * 30)))

def draw(win, grid, metrics, mode, heuristic):
    win.fill(WHITE)
    for row in grid:
        for node in row: node.draw(win)
    
    for i in range(ROWS):
        pygame.draw.line(win, GREY, (0, i * NODE_WIDTH), (GRID_WIDTH, i * NODE_WIDTH))
        pygame.draw.line(win, GREY, (i * NODE_WIDTH, 0), (i * NODE_WIDTH, GRID_WIDTH))
    
    draw_ui(win, metrics, mode, heuristic)
    pygame.display.update()

# --- Search Algorithm ---
def search_algorithm(draw_func, grid, start, goal, mode, heur_type, metrics):
    start_time = time.perf_counter()
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    
    visited_count = 0
    open_set_hash = {start}
    heuristic = h_manhattan if heur_type == "Manhattan" else h_euclidean

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)
        visited_count += 1

        if current == goal:
            path = []
            while current in came_from:
                current = came_from[current]
                if current != start: current.make_path()
                path.append(current)
            
            metrics['visited'] = visited_count
            metrics['cost'] = len(path)
            metrics['time'] = (time.perf_counter() - start_time) * 1000
            return path[::-1]

        for neighbor in current.neighbors:
            temp_g = g_score[current] + 1
            if temp_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g
                h_val = heuristic(neighbor.get_pos(), goal.get_pos())
                f_score = temp_g + h_val if mode == "A*" else h_val
                
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score, count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_frontier()
        
        if current != start: current.make_visited()
        draw_func()

    return None

def main():
    grid = [[Node(i, j) for j in range(ROWS)] for i in range(ROWS)]
    start, goal = None, None
    mode, heur_type = "A*", "Manhattan"
    metrics = {'visited': 0, 'cost': 0, 'time': 0.0}
    run = True

    while run:
        draw(WIN, grid, metrics, mode, heur_type)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: run = False
            
            if pygame.mouse.get_pressed()[0]: # Left Click
                pos = pygame.mouse.get_pos()
                if pos[0] < GRID_WIDTH:
                    row, col = pos[0] // NODE_WIDTH, pos[1] // NODE_WIDTH
                    node = grid[row][col]
                    if not start: start = node; start.make_start()
                    elif not goal and node != start: goal = node; goal.make_goal()
                    elif node != start and node != goal: node.make_wall()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g: mode = "Greedy" if mode == "A*" else "A*"
                if event.key == pygame.K_m: heur_type = "Euclidean" if heur_type == "Manhattan" else "Manhattan"
                
                if event.key == pygame.K_r: # Random Map Generator (Requirement 1)
                    for row in grid:
                        for node in row:
                            if node != start and node != goal:
                                node.reset()
                                if random.random() < 0.3: node.make_wall()

                if event.key == pygame.K_c:
                    start, goal = None, None
                    grid = [[Node(i, j) for j in range(ROWS)] for i in range(ROWS)]
                    metrics = {'visited': 0, 'cost': 0, 'time': 0.0}

                if event.key == pygame.K_SPACE and start and goal:
                    for row in grid:
                        for node in row: node.update_neighbors(grid)
                    
                    path = search_algorithm(lambda: draw(WIN, grid, metrics, mode, heur_type), 
                                          grid, start, goal, mode, heur_type, metrics)
                    
                    # Dynamic Mode (Requirement 3)
                    if path:
                        for step in path:
                            start.reset(); start = step; start.make_start()
                            if random.random() < 0.1: # Obstacle spawning
                                r, c = random.randint(0, ROWS-1), random.randint(0, ROWS-1)
                                if grid[r][c] not in [start, goal]:
                                    grid[r][c].make_wall()
                                    for row_ in grid:
                                        for n_ in row_: n_.update_neighbors(grid)
                                    if grid[r][c] in path:
                                        path = search_algorithm(lambda: draw(WIN, grid, metrics, mode, heur_type), 
                                                              grid, start, goal, mode, heur_type, metrics)
                                        if not path: break
                            draw(WIN, grid, metrics, mode, heur_type)
                            pygame.time.delay(50)

    pygame.quit()

main()
