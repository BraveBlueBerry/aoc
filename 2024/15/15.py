import re
from common.map_solver import AreaWithMoveableObjects, Direction, Mover, Position, Area

i = open("input.txt", "r")

data = []
matches = i.read().split('\n\n')

i.close()

temp_w = matches[0].split('\n')
route = matches[1].replace('\n', '')

s_pos = Position(0,0)
s_big_pos = Position(0,0)
warehouse = []
big_warehouse = []
for i, x in enumerate(temp_w):
    new_list = []
    new_big_list = []
    for z, y in enumerate(temp_w[i]):
        new_list.append(y)
        match y:
            case '#':
                new_big_list.append('#')
                new_big_list.append('#')
            case 'O':
                new_big_list.append('[')
                new_big_list.append(']')
            case '.':
                new_big_list.append('.')
                new_big_list.append('.')
            case '@':
                new_big_list.append('@')
                new_big_list.append('.')
        if y == '@':
            s_pos = Position(z, i)
    warehouse.append(new_list)
    big_warehouse.append(new_big_list)

for y, row in enumerate(big_warehouse):
    for x, col in enumerate(row):
        if col == '@':
            s_big_pos = Position(x, y)


## Part 1
mover = Mover(s_pos)
warehouse = AreaWithMoveableObjects(warehouse, mover)
for direction in route:
    print(direction)
    direction = Direction.from_symbol(direction)
    warehouse.move(direction)
    print(warehouse)

print(warehouse.get_score())

## Part 2
mover = Mover(s_big_pos)
big_warehouse = AreaWithMoveableObjects(big_warehouse, mover)
print(big_warehouse)
# for direction in route:
#     print(direction)
#     direction = Direction.from_symbol(direction)
#     big_warehouse.move(direction)
#     print(big_warehouse)

print(big_warehouse.get_score())


