import re

from common.map_solver import Maze
from common.navigation_utils import Position

i = open("input.txt", "r")

fallen_bytes = []

for line in i:
    matches = re.findall(r'\d+', line)
    fallen_bytes.append(Position(matches[0], matches[1]))

i.close()



memory_space = Maze([])

# Build up the area
space_size = 71
memory_space.make_the_area(space_size)
stop_bytes_from_falling_after = 1024

for i, byte_pos in enumerate(fallen_bytes):
    if i == stop_bytes_from_falling_after:
        break
    memory_space.add_obstruction(byte_pos)
memory_space.add_start(Position(0,0))
memory_space.add_end(Position(70,70))
print(memory_space)

# Solving the maze
_, score = memory_space.solve_maze_a_star()

print(memory_space)

# Part two
# for i in range(stop_bytes_from_falling_after, len(fallen_bytes)):
#     memory_space.add_obstruction(fallen_bytes[i])
#     print(fallen_bytes[i])
#     memory_space.reset()
#     _, score = memory_space.solve_maze_a_star()
#     print(memory_space)
#     if score == 0:
#         exit()
    # if i > 1050:
    #     exit()

for y, row in enumerate(memory_space.original_area):
    print(row)