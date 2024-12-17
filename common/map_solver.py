from abc import ABC, abstractmethod
from enum import Enum
import heapq
from itertools import count


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'(x: {self.x}, y: {self.y})'

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        return False

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

    def get_symbol(self):
        return self.value[0]

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
    the_area: list[list[str | int]] = []
    empty_space: str|int = '.'
    wall: str|int = '#'

    def __repr__(self):
        string = '   '
        for i in range(len(self.the_area[0])):
            string += (str(i)[-1])
        string += '\n'
        for y, row in enumerate(self.the_area):
            string += f'{y}' + (3 - len(str(y))) * ' '
            for x, col in enumerate(row):
                string += str(self.the_area[y][x])
            string += '\n'
        return string

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

class Room(Area):
    mover: Mover
    empty_space: str|int = '.'

    def __init__(self, a: list[list[str|int]],m: Mover):
        self.the_area = a
        self.mover = m

    @abstractmethod
    def get_score(self):
        pass

    def get_next_pos_for_mover(self, d: Direction):
        return Position(self.mover.position.x + d.move().x, self.mover.position.y + d.move().y)

    @staticmethod
    def get_next_pos_for_pos(pos: Position, d: Direction):
        return Position(pos.x + d.move().x, pos.y + d.move().y)


    def move_mover(self, n_pos: Position):
        self.change_spot(n_pos, self.mover.visual)
        self.change_spot(self.mover.position, self.empty_space)
        self.mover.move(n_pos)

    @abstractmethod
    def move(self, d: Direction):
        pass


class RoomWithMoveableObjects(Room):
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

class Maze(Area):
    starting_symbol: str|int = 'S'
    end_symbol: str|int = 'E'
    starting_position: Position
    end_position: Position
    starting_direction: str # S if it doesn't matter

    def __init__(self, a: list[list[str | int]], starting_direction = 'S'):
        self.the_area = a
        self.starting_direction = starting_direction
        for y, row in enumerate(self.the_area):
            for x, col in enumerate(row):
                if col == self.starting_symbol:
                    self.starting_position = Position(x, y)
                if col == self.end_symbol:
                    self.end_position = Position(x, y)
        self.counter = count()

    def reconstruct_path(self, path):
        reconstructed_path = []
        current = self.end_position
        while current != self.starting_position:
            if current != self.end_position:
                self.change_spot(current, direction_symbol)

            reconstructed_path.append(current)
            direction_symbol = path[current][1]
            current = path[current][0]

        reconstructed_path.append(self.starting_position)
        return reconstructed_path[::-1]

    def solve_maze_a_star(self):
        def heuristic(current: Position):
            goal = self.end_position
            return abs(current.x - goal.x) + abs(current.y - goal.y)

        visited = set()
        to_visit = []
        path = {}
        heapq.heappush(to_visit, (0, next(self.counter), self.starting_position, self.starting_direction))
        # cost-so-far
        path_score: dict[Position, int] = {self.starting_position: 0}
        # cost-so-far + heuristic
        estimated_score = {self.starting_position: heuristic(self.starting_position)}

        loop = 0
        while to_visit:
            _, _, current_pos, current_direction_symbol = heapq.heappop(to_visit)
            if current_pos == self.end_position:
                return self.reconstruct_path(path), path_score[self.end_position]
            if current_pos in visited:
                continue
            visited.add(current_pos)


            for direction in Direction:
                d = direction.move()
                neighbour_pos = Position(current_pos.x + d.x, current_pos.y + d.y)
                if neighbour_pos in visited:
                    continue
                if not self.is_in_map(neighbour_pos) or self.get_spot(neighbour_pos) == self.wall:
                    continue

                tentative_score = path_score[current_pos] + 1
                if current_direction_symbol != self.starting_symbol and current_direction_symbol != direction.get_symbol():
                    tentative_score += 1000
                if neighbour_pos not in path_score or tentative_score < path_score[neighbour_pos]:
                    path[neighbour_pos] = (current_pos, direction.get_symbol())
                    path_score[neighbour_pos] = tentative_score
                    estimated_score[neighbour_pos] = tentative_score + heuristic(neighbour_pos)
                    heapq.heappush(to_visit, (estimated_score[neighbour_pos], next(self.counter), neighbour_pos, direction.get_symbol()))

            loop += 1


