from abc import ABC, abstractmethod
from enum import Enum

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'x: {self.x}, y: {self.y}'

class Direction(Enum):
    UP = ('^', Position(0, -1))
    RIGHT = ('>', Position(1, 0))
    DOWN = ('v', Position(0, 1))
    LEFT = ('<', Position(-1, 0))

    @classmethod
    def from_symbol(cls, symbol):
        for direction in cls:
            if direction.value[0] == symbol:
                return direction
        raise ValueError(f"Invalid direction symbol: {symbol}")

    def move(self):
        return self.value[1]  # Returns the Position

class Mover(ABC):
    position: Position
    starting_position: Position
    visual: str|int = '@'

    def __init__(self, s_pos: Position):
        self.starting_position = s_pos
        self.position = s_pos

    def move(self, n_pos: Position):
        self.position = n_pos


class Area(ABC):
    the_area: list[list[str|int]] = []
    mover: Mover
    empty_space: str|int = '.'

    def __init__(self, a: list[list[str|int]],m: Mover):
        self.the_area = a
        self.mover = m

    def __repr__(self):
        string = ''
        for y, row in enumerate(self.the_area):
            for x, col in enumerate(row):
                string += str(self.the_area[y][x])
            string += '\n'
        return string

    @abstractmethod
    def get_score(self):
        pass

    def get_next_pos_for_mover(self, d: Direction):
        return Position(self.mover.position.x + d.move().x, self.mover.position.y + d.move().y)

    @staticmethod
    def get_next_pos_for_pos(pos: Position, d: Direction):
        return Position(pos.x + d.move().x, pos.y + d.move().y)

    def is_in_map(self, pos: Position):
        if not (0 <= pos.y < len(self.the_area)):
            return False
        if not (0 <= pos.x < len(self.the_area[pos.y])):
            return False
        return True

    def get_spot(self, pos: Position):
        return self.the_area[pos.y][pos.x]

    def change_spot(self, pos: Position, new: str|int):
        self.the_area[pos.y][pos.x] = new

    def move_mover(self, n_pos: Position):
        self.change_spot(n_pos, self.mover.visual)
        self.change_spot(self.mover.position, self.empty_space)
        self.mover.move(n_pos)

    @abstractmethod
    def move(self, d: Direction):
        pass


class AreaWithMoveableObjects(Area):
    wall: str = '#'
    moveable_obstruction: str =  'O'
    big_moveable_obstruction: list[str] = ['[', ']']
    big_obstr_left: str = big_moveable_obstruction[0]
    big_obstr_right: str = big_moveable_obstruction[1]

    def check_vertically_box(self, box_pos: list[Position], d: Direction):
        found_boxes = []
        can_move = True
        for pos in box_pos:
            pos_above = Position(pos.x, pos.y + d.move().y)
            if self.get_spot(pos_above) in self.big_moveable_obstruction:
                # its part of a box
                box = [pos_above, self.get_pos_other_part_box(pos_above)]
                found_boxes.append(box)
                new_can_move, new_result = self.check_vertically_box(box, d)
                found_boxes += new_result
                can_move = can_move and new_can_move

            if self.get_spot(pos_above) == self.wall:
                can_move = False
        return can_move, found_boxes

    def get_pos_other_part_box(self, box_part_pos: Position):
        if self.get_spot(box_part_pos) == self.big_obstr_left:
            return Position(box_part_pos.x + 1, box_part_pos.y)
        return Position(box_part_pos.x - 1, box_part_pos.y)

    def move(self, d: Direction):
        moving_horizontally = (d == Direction.LEFT or d == Direction.RIGHT)
        # d_movement = d.move()
        new_pos = self.get_next_pos_for_mover(d)
        new_spot_would_be = self.get_spot(new_pos)
        match new_spot_would_be:
            # #
            case self.wall:
                return
            # .
            case self.empty_space:
                self.move_mover(new_pos)
                return
            # O
            case self.moveable_obstruction:
                pos_behind = self.get_next_pos_for_pos(new_pos, d)
                spot_behind = self.get_spot(pos_behind)
                while spot_behind == self.moveable_obstruction and spot_behind != self.wall:
                    pos_behind = self.get_next_pos_for_pos(pos_behind, d)
                    spot_behind = self.get_spot(pos_behind)

                if spot_behind == self.wall:
                    return

                free_space_after_obstacle_row = pos_behind
                self.change_spot(free_space_after_obstacle_row, self.moveable_obstruction)
                self.move_mover(new_pos)
                return
            # []
            case self.big_obstr_left | self.big_obstr_right:
                other_part_pos = self.get_pos_other_part_box(new_pos)

                if moving_horizontally:
                    pos_behind = self.get_next_pos_for_pos(other_part_pos, d)
                    spot_behind = self.get_spot(pos_behind)

                    while spot_behind != self.empty_space and spot_behind != self.wall:
                        pos_behind = self.get_next_pos_for_pos(pos_behind, d)
                        spot_behind = self.get_spot(pos_behind)

                    if spot_behind == self.wall:
                        return

                    free_space_after_obstacle_row = pos_behind
                    self.the_area[free_space_after_obstacle_row.y].pop(free_space_after_obstacle_row.x)
                    self.the_area[free_space_after_obstacle_row.y].insert(self.mover.position.x, self.empty_space)
                    self.mover.position = new_pos
                    return
                else:
                    # Moving vertically
                    print(new_pos, other_part_pos)
                    can_move, boxes_found_vertically = self.check_vertically_box([new_pos, other_part_pos], d)

                    boxes_found_vertically.append([new_pos, self.get_pos_other_part_box(new_pos)])
                    if can_move:
                        for box in boxes_found_vertically:
                            for box_pos in box:
                                self.change_spot(box_pos, self.empty_space)

                        for box in boxes_found_vertically:
                            left = False
                            if box[0].x < box[1].x:
                                left = True
                            if left:
                                self.change_spot(Position(box[0].x, box[0].y + d.move().y), self.big_obstr_left)
                                self.change_spot(Position(box[1].x, box[1].y + d.move().y), self.big_obstr_right)
                            else:
                                self.change_spot(Position(box[0].x, box[0].y + d.move().y), self.big_obstr_right)
                                self.change_spot(Position(box[1].x, box[1].y + d.move().y), self.big_obstr_left)

                        self.move_mover(self.get_next_pos_for_mover(d))

    def get_score(self):
        count = 0
        for y, row in enumerate(self.the_area):
            for x, col, in enumerate(row):
                if col == self.moveable_obstruction or col == self.big_obstr_left:
                    count += 100 * y + x
        return count


class Bbb:
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