i = open("input_big.txt", "r")

original_map = [(list(line.strip())) for line in i]

i.close()

directions = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0)
]

found_combinations = {}

def is_in_map(pos, m):
    col, row = pos
    if not (0 <= row < len(m)):
        return False
    if not (0 <= col < len(m[row])):
        return False
    return True

def get_next_pos(c_pos, m):
    current_height = m[c_pos[1]][c_pos[0]]
    print(f'Checking next positions for current height: {current_height}')
    next_positions = []
    for direction in directions:
        next_pos = (c_pos[0] + direction[0], c_pos[1] + direction[1])
        if is_in_map(next_pos, m) and m[next_pos[1]][next_pos[0]] == str((int(current_height) + 1)):
            next_positions.append(next_pos)
    return next_positions

def look_for_trail(start_pos, c_pos, m, depth = 0):
    current_height = m[c_pos[1]][c_pos[0]]
    print('  ' * depth + f'Current height = {current_height}')
    print('  ' * depth + f'Current position = {c_pos}')
    if current_height == '9':
        if start_pos in found_combinations:
            print(found_combinations)
            found_combinations[start_pos].add(c_pos)
        else:
            found_combinations[start_pos] = set()
            found_combinations[start_pos].add(c_pos)

        return 1
    next_positions = get_next_pos(c_pos, m)
    print('  ' * depth + f'Next_positions = {next_positions}')

    count = 0
    if len(next_positions) > 0:
        for next_position in next_positions:
            count += look_for_trail(start_pos, next_position, m, depth + 1)

    print('  ' * depth + f'Count = {count}')
    return count

trails = 0
for y in range(len(original_map)):
    row = original_map[y]
    for x in range(len(row)):
        print(original_map[y][x])
        if original_map[y][x] == '0':
            trails += look_for_trail((x, y),(x, y), original_map)


print(trails)
print(found_combinations)
coutn = 0
for combination in found_combinations:
    for peak in found_combinations[combination]:
        coutn += 1

print(coutn)
