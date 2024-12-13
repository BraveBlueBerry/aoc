i = open("input.txt", "r")

original_map = [(list(line.strip())) for line in i]

i.close()

directions = [
    (0, -1, 'N'),
    (1, 0, 'W'),
    (0, 1, 'S'),
    (-1, 0, 'E')
]

def is_in_map(pos, m):
    col, row = pos
    if not (0 <= row < len(m)):
        return False
    if not (0 <= col < len(m[row])):
        return False
    return True

def look_for_neighbours(pos, m, s, vis):
    current_veg = m[pos[1]][pos[0]]
    neighbours = []
    for direction in directions:
        new_pos = (pos[0] + direction[0], pos[1] + direction[1], direction[2])
        if is_in_map((new_pos[0], new_pos[1]), m) and m[new_pos[1]][new_pos[0]] == current_veg:
            neighbours.append(new_pos)
            # if (new_pos[0], new_pos[1]) not in vis:
            #     side = frozenset([pos, (new_pos[0], new_pos[1])])
            #     s.add(side)

    return neighbours


def flood_fill(m : list, start_pos : tuple):
    stack = [start_pos]
    region = set()
    region.add(start_pos)
    perimeter = 0
    sides = {}

    while not len(stack) == 0:
        current = stack.pop()
        neighbouring_vegs = look_for_neighbours(current, m, sides, region)
        perimeter += (4 - len(neighbouring_vegs))
        for neighbour in neighbouring_vegs:
            neighbour_pos = neighbour[0], neighbour[1]
            direction_found = neighbour[2]
            if not neighbour_pos in region:
                region.add(neighbour_pos)
                stack.append(neighbour_pos)
                if neighbour[2] in sides:
                    sides[direction_found].add(neighbour_pos)
                else:
                    sides[direction_found] = set()
                    sides[direction_found].add(neighbour_pos)

    f_price = len(region) * perimeter
    print(m[start_pos[1]][start_pos[0]])
    print(region)
    for side in sides:
        print(side)
    print(len(sides))
    # print(start_pos)
    # print(f'Found {len(sides)} directions')
    # d = {'NS': set(), 'EW': set()}
    # for side in sides:
    #     print(f'Direction: [{len(sides[side])}]{side} => {sides[side]}')
    #     for coords in sides[side]:
    #         if side == 'N' or side == 'S':
    #             d['NS'].add(coords[0])
    #         else:
    #             d['EW'].add(coords[1])
    # print(f'The different axes?: {d}')
    # print(len(d['NS']) * (len(sides['W']) - len(sides['E'])))

    # print(sides)
    return region, f_price

visited = set()
regions = []
total_fence_price = 0

for x, row in enumerate(original_map):
    for y, col in enumerate(row):
        pos = (x, y)
        if pos not in visited:
            region, fence_price = flood_fill(original_map, (x, y))
            total_fence_price += fence_price
            regions.append(region)
            for r in region:
                visited.add(r)

# print(regions)
print(f'Totale prijs van de hekjes: {total_fence_price}')
for region in regions:
    print(region)

# def calc_price(region):
#     for r in region:
