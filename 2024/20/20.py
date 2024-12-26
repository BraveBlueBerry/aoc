from copy import deepcopy

from common.map_solver import Maze
from common.navigation_utils import Direction, Position

i = open("input.txt", "r")

data = []
original_map =  [(list(line.strip())) for line in i]

i.close()

og_maze = Maze(original_map, '>')
maze = Maze(original_map, '>')
print(og_maze)

og_score, _ = og_maze.solve_maze_a_star()

print(og_maze)
print(og_score)

inner_walls = maze.get_walls(only_inner_walls=True)
counter = 0
inner_walls_trimmed = deepcopy(inner_walls)

for i, wall_pos in enumerate(inner_walls):
    neighbours: dict[Direction:Position] = maze.get_neighbours(wall_pos)
    for n in neighbours:
        if n[]

for i, wall_pos in enumerate(inner_walls):
    # print(maze)
    maze.reset()

    maze.change_spot(wall_pos, maze.empty_space)
    score, _  = maze.solve_maze_a_star()

    if og_score - score >= 100:
        print(wall_pos)
        print(f'Saved: {og_score - score}')
        # print(maze)
        counter += 1
    # print(maze)

print(counter)