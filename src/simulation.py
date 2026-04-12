import pygame
import random
import time
from src.utils import *
from src.planner import astar
from src.agent import Agent

class Simulation:
    def __init__(self):
        pygame.init()
        self.replans = 0
        self.total_replans = 0
        self.goal_reached = False
        self.last_replan_frame = 0
        self.win = pygame.display.set_mode((COLS*CELL_SIZE, ROWS*CELL_SIZE))
        pygame.display.set_caption("Autonomous Navigation System")

        self.font = pygame.font.SysFont("Arial", 16)

        self.grid = [[0]*COLS for _ in range(ROWS)]

        # Static obstacles
        for _ in range(40):
            x, y = random.randint(0,ROWS-1), random.randint(0,COLS-1)
            self.grid[x][y] = 1

        # Dynamic obstacles
        self.dynamic_obstacles = []
        for _ in range(10):
            x, y = random.randint(0,ROWS-1), random.randint(0,COLS-1)
            self.dynamic_obstacles.append([x, y])

        self.start = (0,0)
        self.goal = (ROWS-1, COLS-1)

        self.agent = Agent(self.start, CELL_SIZE)

        self.frame_count = 0

        # Metrics
        self.start_time = time.time()
        self.path_length = 0

        self.replan()

    def replan(self):
        self.replans += 1
        self.total_replans += 1
        path = astar(self.grid, self.agent.grid_position, self.goal)
        if path:
            self.agent.set_path(path, self.goal)
            self.path_length = len(path)

    def move_dynamic_obstacles(self):
        if self.frame_count % 10 != 0:
            return

        for obs in self.dynamic_obstacles:
            self.grid[obs[0]][obs[1]] = 0

            dx, dy = random.choice([(0,1),(1,0),(-1,0),(0,-1)])
            nx, ny = obs[0] + dx, obs[1] + dy

            if 0 <= nx < ROWS and 0 <= ny < COLS:
                if (nx, ny) != self.start and (nx, ny) != self.goal:
                    obs[0], obs[1] = nx, ny

        for obs in self.dynamic_obstacles:
            self.grid[obs[0]][obs[1]] = 1

    def draw_grid_lines(self):
        for x in range(0, COLS*CELL_SIZE, CELL_SIZE):
            pygame.draw.line(self.win, (200,200,200), (x,0), (x,ROWS*CELL_SIZE))
        for y in range(0, ROWS*CELL_SIZE, CELL_SIZE):
            pygame.draw.line(self.win, (200,200,200), (0,y), (COLS*CELL_SIZE,y))

    def draw_ui(self):
        elapsed_time = round(time.time() - self.start_time, 2)
        pygame.draw.rect(self.win, (220,220,220), (0, ROWS*CELL_SIZE - 50, COLS*CELL_SIZE, 50))
        text1 = self.font.render(f"Path Length: {self.path_length}", True, (0,0,0))
        text2 = self.font.render(f"Time: {elapsed_time}s", True, (0,0,0))
        text3 = self.font.render(f"Session Replans: {self.replans} | Total Replans: {self.total_replans}", True, (0,0,0))
        self.win.blit(text3, (350, ROWS*CELL_SIZE - 30))

        self.win.blit(text1, (10, ROWS*CELL_SIZE - 40))
        self.win.blit(text2, (10, ROWS*CELL_SIZE - 20))

        if self.agent.grid_position == self.goal:
            status = self.font.render("Status: Goal Reached", True, (0,150,0))
        else:
            status = self.font.render("Status: Navigating...", True, (150,0,0))

        self.win.blit(status, (200, ROWS*CELL_SIZE - 30))

    def draw(self):
        self.win.fill(WHITE)

        for i in range(ROWS):
            for j in range(COLS):
                color = WHITE
                if self.grid[i][j] == 1:
                    color = BLACK

                pygame.draw.rect(self.win, color,
                    (j*CELL_SIZE, i*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Path
        for p in self.agent.path:
            pygame.draw.rect(self.win, BLUE,
                (p[1]*CELL_SIZE, p[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Start & Goal
        pygame.draw.rect(self.win, GREEN,
            (self.start[1]*CELL_SIZE, self.start[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.draw.rect(self.win, RED,
            (self.goal[1]*CELL_SIZE, self.goal[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Agent (smooth)
        pygame.draw.rect(self.win, (255,165,0),
            (self.agent.pixel_position[0],
             self.agent.pixel_position[1],
             CELL_SIZE, CELL_SIZE))

        self.draw_grid_lines()
        self.draw_ui()

        pygame.display.update()

    def handle_mouse(self):
        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            row = y // CELL_SIZE
            col = x // CELL_SIZE

            if self.grid[row][col] == 0:
                self.goal = (row, col)
                self.replans = 0
                self.start_time = time.time()
                self.goal_reached = False
                self.replan()

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.frame_count += 1

            self.move_dynamic_obstacles()

            if self.frame_count % 5 == 0:
                if not self.goal_reached:
                    if self.agent.needs_replan(self.grid):
                        if self.frame_count - self.last_replan_frame > 15:
                            self.replan()
                            self.last_replan_frame = self.frame_count

            self.handle_mouse()
            if not self.goal_reached:
                self.agent.move()
            if self.agent.grid_position == self.goal:
                self.goal_reached = True
            self.draw()

        pygame.quit()