import heapq

def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    came_from = {}
    g_score = {start: 0}
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]
        
        neighbors = [(0,1),(1,0),(-1,0),(0,-1)]
        
        for dx, dy in neighbors:
            nx, ny = current[0]+dx, current[1]+dy
            
            if 0 <= nx < rows and 0 <= ny < cols:
                if grid[nx][ny] == 1:
                    continue
                
                temp = g_score[current] + 1
                
                if (nx,ny) not in g_score or temp < g_score[(nx,ny)]:
                    g_score[(nx,ny)] = temp
                    f_score = temp + heuristic((nx,ny), goal)
                    heapq.heappush(open_set, (f_score, (nx,ny)))
                    came_from[(nx,ny)] = current
                    
    return []