from common.a_star_alts import tentative_score_expensive_corners
from common.map_solver import Maze

i = open("input.txt", "r")

data = []
original_map =  [(list(line.strip())) for line in i]

i.close()

maze = Maze(original_map, '>')
print(maze)

# def tentative_score_expensive_corners(path_score_up_to_now, current: Position):
#     tentative_score = path_score[current_pos] + 1
#     if current_direction_symbol != self.starting_symbol and current_direction_symbol != direction.get_symbol():
#         tentative_score += 1000

path, score = maze.solve_maze_a_star(det_tentative_cost=tentative_score_expensive_corners, direction_matters=True)


print(maze)
print(score)
#
# maze.reconstruct_path(maze.all_paths)
# print(maze)

# for p in maze.all_paths:
#     print(f'{p}: {maze.all_paths[p]}')
#
# def make_path(all_path_dict, pos: Position, path):
#     paths = []
#     path.append(pos)
#     if pos not in all_path_dict:
#         return [path]
#     if len(all_path_dict[pos]) == 1:
#         return make_path(all_path_dict, all_path_dict[pos][0], path)
#     for previous in all_path_dict[pos]:
#         paths.append(make_path(all_path_dict, previous, deepcopy(path)))
#     print(len(paths), pos)
#     return paths
#
# end = maze.end_position
# all_paths = make_path(maze.all_paths, end, [])
# for p in all_paths:
#     maze.reconstruct_path(p)
#     print(maze)