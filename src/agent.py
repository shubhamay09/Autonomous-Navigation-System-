class Agent:
    def __init__(self, start, cell_size):
        self.grid_position = start
        self.pixel_position = [start[1]*cell_size, start[0]*cell_size]
        self.cell_size = cell_size

        self.path = []
        self.goal = None
        self.speed = 4  # pixels per frame

    def set_path(self, path, goal):
        self.path = path
        self.goal = goal

    def move(self):
        if not self.path:
            return

        target = self.path[0]
        target_pixel = [target[1]*self.cell_size, target[0]*self.cell_size]

        dx = target_pixel[0] - self.pixel_position[0]
        dy = target_pixel[1] - self.pixel_position[1]

        # Move smoothly
        if abs(dx) > self.speed:
            self.pixel_position[0] += self.speed if dx > 0 else -self.speed
        else:
            self.pixel_position[0] = target_pixel[0]

        if abs(dy) > self.speed:
            self.pixel_position[1] += self.speed if dy > 0 else -self.speed
        else:
            self.pixel_position[1] = target_pixel[1]

        # If reached cell → update grid position
        if self.pixel_position == target_pixel:
            self.grid_position = target
            self.path.pop(0)

    def needs_replan(self, grid):
        if not self.path:
            return True

        next_pos = self.path[0]
        if grid[next_pos[0]][next_pos[1]] == 1:
            return True

        return False