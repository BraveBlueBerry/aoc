from copy import deepcopy

i = open("input_big.txt", "r")

equations = []

original_map = [(list(line.strip())) for line in i]
part_one_map = deepcopy(original_map)
part_two_map = deepcopy(original_map)

i.close()

antenna_groups = {}

def is_in_map(m, coord):
    return 0 <= coord[1] < len(m) and 0 <= coord[0] < len(m[coord[1]])

for y in range(len(part_one_map)):
    row = part_one_map[y]
    for x in range(len(row)):
        symbol = part_one_map[y][x]
        if not symbol == '.':
            if symbol in antenna_groups:
                antenna_groups[symbol].append((x, y))
            else:
                antenna_groups[symbol] = [(x, y)]

for antenna in antenna_groups:
    antennas = antenna_groups[antenna]
    for a in range(len(antennas)):
        for b in range(len(antennas)):

            if b == a:
                continue
            diff = (antennas[b][0] - antennas[a][0], antennas[b][1] - antennas[a][1])
            new_pos = (antennas[b][0] + diff[0], antennas[b][1] + diff[1])

            if is_in_map(part_one_map, new_pos):
                part_one_map[new_pos[1]][new_pos[0]] = '#'

    for t in range(len(part_one_map)):
        print(part_one_map[t])


solution_one = 0
for y in range(len(part_one_map)):
    for x in range(len(part_one_map[y])):
        if part_one_map[y][x] == '#':
            solution_one += 1

print('\n')

for antenna in antenna_groups:
    antennas = antenna_groups[antenna]
    for a in range(len(antennas)):
        for b in range(len(antennas)):

            if b == a:
                continue
            diff = (antennas[b][0] - antennas[a][0], antennas[b][1] - antennas[a][1])


            new_positions = []
            out_of_map = False
            loop = 1
            while not out_of_map:
                new_pos = (antennas[b][0] + diff[0] * loop, antennas[b][1] + diff[1] * loop)
                print(new_pos)
                loop += 1

                if is_in_map(part_two_map, new_pos):
                    if part_two_map[new_pos[1]][new_pos[0]] == '.':
                        part_two_map[new_pos[1]][new_pos[0]] = '#'
                else:
                    out_of_map = True

    for t in range(len(part_two_map)):
        print(part_two_map[t])

solution_two = 0
for y in range(len(part_two_map)):
    for x in range(len(part_two_map[y])):
        if not part_two_map[y][x] == '.':
            solution_two += 1

print(f'Solution one: {solution_one}')
print(f'Solution two: {solution_two}')