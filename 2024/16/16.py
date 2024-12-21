from common.map_solver import Maze

i = open("input.txt", "r")

data = []
original_map =  [(list(line.strip())) for line in i]

i.close()

maze = Maze(original_map, '>')
print(maze)

# path, score = maze.solve_maze_a_star(det_tentative_cost=tentative_score_expensive_corners, direction_matters=True)

all_paths = maze.bfs_find_all_paths()

for path in all_paths:
    print(path)
