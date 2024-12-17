from common.map_solver import Maze

i = open("input.txt", "r")

data = []
original_map =  [(list(line.strip())) for line in i]

i.close()

maze = Maze(original_map, '>')
print(maze)

path, score = maze.solve_maze_a_star()


print(maze)
print(score)