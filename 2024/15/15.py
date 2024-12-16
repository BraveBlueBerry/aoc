import re

i = open("input.txt", "r")

data = []
matches = i.read().split('\n\n')

i.close()

temp_w = matches[0].split('\n')
route = matches[1].replace('\n', '')

s_pos = [0,0]
s_big_pos = [0,0]
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
            s_pos = [z, i]
    warehouse.append(new_list)
    big_warehouse.append(new_big_list)

for y, row in enumerate(big_warehouse):
    for x, col in enumerate(row):
        if col == '@':
            s_big_pos = [x, y]

class Area:
    the_area = []
    directions = {
        '^' : (0, -1),
        '>' : (1, 0),
        'v' : (0, 1),
        '<' : (-1, 0)
    }
    wall = '#'
    moveable_obstruction = 'O'
    big_moveable_obstruction = ['[', ']']
    big_obstr_left = big_moveable_obstruction[0]
    big_obstr_right = big_moveable_obstruction[1]
    mover = '@'
    empty_space = '.'
    mover_position = [0,0]
    mover_starting_position = [0,0]

    def __init__(self, a: list[list[str]], start):
        self.the_area = a
        self.mover_position = start
        self.mover_starting_position = start


    def __repr__(self):
        string = ''
        for y, row in enumerate(self.the_area):
            for x, col in enumerate(row):
                string += str(self.the_area[y][x])
            string += '\n'
        return string

    def get_score(self):
        count = 0
        for y, row in enumerate(self.the_area):
            for x, col, in enumerate(row):
                if col == self.moveable_obstruction or col == self.big_obstr_left:
                    count += 100 * y + x
        return count

    def get_next_pos_for_mover(self, d):
        return self.mover_position[0] + d[0], self.mover_position[1] + d[1]

    @staticmethod
    def get_next_pos_for_pos(d, pos):
        return pos[0] + d[0], pos[1] + d[1]

    def is_in_map(self, pos):
        col, row = pos
        if not (0 <= row < len(self.the_area)):
            return False
        if not (0 <= col < len(self.the_area[row])):
            return False
        return True

    def get_spot(self, pos):
        return self.the_area[pos[1]][pos[0]]

    def change_spot(self, pos, new):
        self.the_area[pos[1]][pos[0]] = new

    def check_vertically_box(self, box_pos, d):
        found_boxes = []
        can_move = True
        for pos in box_pos:
            pos_above = [pos[0], pos[1] + d[1]]
            if self.get_spot(pos_above) in self.big_moveable_obstruction:
                # its part of a box
                box = [pos_above, self.get_other_part_box(pos_above)]
                found_boxes.append(box)
                new_can_move, new_result = self.check_vertically_box(box, d)
                found_boxes += new_result
                can_move = can_move and new_can_move

            if self.get_spot(pos_above) == self.wall:
                can_move = False
        return can_move, found_boxes

    def get_other_part_box(self, box_part_pos):
        if self.get_spot(box_part_pos) == self.big_obstr_left:
            return [box_part_pos[0] + 1, box_part_pos[1]]
        return [box_part_pos[0] - 1, box_part_pos[1]]

    def move_mover(self, n_pos):
        self.change_spot(n_pos, self.mover)
        self.change_spot(self.mover_position, self.empty_space)
        self.mover_position = n_pos

    def move(self, d):
        moving_horizontally = (d == '<' or d == '>')
        d = self.directions[d]
        new_pos = self.get_next_pos_for_mover(d)
        new_spot_would_be = self.get_spot(new_pos)
        match new_spot_would_be:
            # #
            case self.wall:
                return
            # .
            case self.empty_space:
                self.change_spot(self.mover_position, self.empty_space)
                self.change_spot(new_pos, self.mover)
                self.mover_position = new_pos
                return
            # O
            case self.moveable_obstruction:
                first_obstacle_in_row = new_pos
                pos_behind = self.get_next_pos_for_pos(d, new_pos)
                spot_behind = self.get_spot(pos_behind)
                while spot_behind == self.moveable_obstruction and spot_behind != self.wall:
                    pos_behind = self.get_next_pos_for_pos(d, pos_behind)
                    spot_behind = self.get_spot(pos_behind)

                if spot_behind == self.wall:
                    return

                free_space_after_obstacle_row = pos_behind
                self.change_spot(free_space_after_obstacle_row, self.moveable_obstruction)
                self.move_mover(first_obstacle_in_row)
                return
            # []
            case self.big_obstr_left | self.big_obstr_right:
                other_part_pos = self.get_other_part_box(new_pos)

                if moving_horizontally:
                    pos_behind = self.get_next_pos_for_pos(d, other_part_pos)
                    spot_behind = self.get_spot(pos_behind)

                    while spot_behind != self.empty_space and spot_behind != self.wall:
                        pos_behind = self.get_next_pos_for_pos(d, pos_behind)
                        spot_behind = self.get_spot(pos_behind)

                    if spot_behind == self.wall:
                        return

                    free_space_after_obstacle_row = pos_behind
                    self.the_area[free_space_after_obstacle_row[1]].pop(free_space_after_obstacle_row[0])
                    self.the_area[free_space_after_obstacle_row[1]].insert(self.mover_position[0], self.empty_space)
                    self.mover_position = new_pos
                    return
                else:
                    # Moving vertically
                    can_move, boxes_found_vertically = self.check_vertically_box([new_pos, other_part_pos], d)

                    boxes_found_vertically.append([new_pos, self.get_other_part_box(new_pos)])
                    if can_move:
                        for box in boxes_found_vertically:
                            for box_pos in box:
                                self.change_spot([box_pos[0], box_pos[1]], self.empty_space)

                        for box in boxes_found_vertically:
                            left = False
                            if box[0][0] < box[1][0]:
                                left = True
                            if left:
                                self.change_spot([box[0][0], box[0][1] + d[1]], self.big_obstr_left)
                                self.change_spot([box[1][0], box[1][1] + d[1]], self.big_obstr_right)
                            else:
                                self.change_spot([box[0][0], box[0][1] + d[1]], self.big_obstr_right)
                                self.change_spot([box[1][0], box[1][1] + d[1]], self.big_obstr_left)

                        self.move_mover(self.get_next_pos_for_mover(d))


## Part 1
# warehouse = Area(warehouse, s_pos)
# for direction in route:
#     warehouse.move(direction)
#     print(direction)
#     print(warehouse)
#
# print(warehouse.get_score())

## Part 2
big_warehouse = Area(big_warehouse, s_big_pos)
print(big_warehouse)
for direction in route:
    big_warehouse.move(direction)
    print(direction)
    print(big_warehouse)

print(big_warehouse.get_score())


