import copy

def printd(string):
    if debuglogging: print(string)

f = open("map_big.txt", "r")
original_map = []
map = []
for line in f:
    original_map.append(list(line.strip()))
    map.append(list(line.strip()))

f.close()

debuglogging = False

start_symbol = '^'
starting_pos = (0, 0)
path_symbol = 'X'
obstacle_symbol = '#'

for y in range(len(map)):
    r = map[y]
    printd(r)
    for x in range(len(r)):
        if map[y][x] == start_symbol:
            starting_pos = (x, y)


def pos_is_out_of_map(pos, m):
    # Check if pos is out of bounds
    row, col = pos
    if not (0 <= row < len(m)):
        return True  # Row index is out of bounds
    if not (0 <= col < len(m[row])):
        return True  # Column index is out of bounds
    return False  # Both row and column are within bounds

def get_next_pos(c_pos, d):
    return c_pos[0] + d[0], c_pos[1] + d[1]

def next_pos_is_obstacle(c_pos, d, m):
    next_pos = get_next_pos(c_pos, d)
    return m[next_pos[1]][next_pos[0]] == obstacle_symbol

# def next_pos_is_end(c_pos, d):
#     next_pos = get_next_pos(c_pos, d)
#     return next_pos == starting_pos

def enters_a_loop(next_pos, d, m):
    return m[next_pos[1]][next_pos[0]] == d[2]

def simulate_path(start_pos, m, path_symbol = ''):
    # for j in range(len(m)):
    #     print(m[j])
    # print('\n')
    end_not_reached = True
    current_pos = start_pos
    direction_rotation = [
        (0, -1, '^'),
        (1, 0, '>'),
        (0, 1, 'v'),
        (-1, 0, '<')
    ]
    direction = direction_rotation[0]
    current_rotation = 0

    while end_not_reached:
        if path_symbol:
            m[current_pos[1]][current_pos[0]] = path_symbol
        else:
           m[current_pos[1]][current_pos[0]] = direction[2]

        if pos_is_out_of_map(get_next_pos(current_pos, direction), m):
            end_not_reached = False
            continue

        while next_pos_is_obstacle(current_pos, direction, m):
            if current_rotation < 3:
                current_rotation += 1
            else:
                current_rotation = 0
            direction = direction_rotation[current_rotation]

        if enters_a_loop(get_next_pos(current_pos, direction), direction, m):
            return True

        current_pos = get_next_pos(current_pos, direction)
        m[current_pos[1]][current_pos[0]] = 'X'

        # for y in range(len(m)):
        #     print(m[y])
        # print('\n')
        # print(current_pos)
        # print(direction)
        # print('\n')

        # if next_pos_is_end(current_pos, direction) and direction == direction_rotation[0]:
        #     end_not_reached = False

solution_one = 0

simulate_path(starting_pos, map, 'X')

for y in range(len(map)):
    r = map[y]
    solution_one += r.count('X')

count_loops = 0

# for y in range(len(original_map)):
#     print(original_map[y])

loop = 0
for y in range(len(map)):
    # print(map[y])
    for x in range(len(map[y])):
        # print(map[y][x])
        if map[y][x] == path_symbol:

            new_map = copy.deepcopy(original_map)


            new_map[y][x] = '#'
            # for jup in range(len(new_map)):
            #     print(new_map[jup])
            # print('\n')

            is_loop = simulate_path(starting_pos, new_map)
            # for jup in range(len(new_map)):
            #     print(new_map[jup])
            # print('\n')
            if is_loop:
                count_loops += 1
            # if loop == 0: exit()
            loop += 1


print(f"========== SOLUTION 1: {solution_one} ==========")
print(f"========== SOLUTION 2: {count_loops} ==========")