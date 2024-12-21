from abc import ABC, abstractmethod
import heapq
from collections import deque
from copy import deepcopy
from itertools import count

from common.a_star_alts import determine_tentative_cost
from common.navigation_utils import Position, Direction


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
    original_area: list[list[str | int]] = deepcopy(the_area)
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

    def change_spot(self, pos: Position, new: str | int):
        self.the_area[pos.y][pos.x] = new

    def make_the_area(self, space_size: int):
        for y in range(space_size):
            row = []
            for x in range(space_size):
                row.append(self.empty_space)
            self.the_area.append(row)
            self.original_area.append(row)

    def add_obstruction(self, pos: Position):
        self.the_area[pos.y][pos.x] = self.wall
        self.original_area[pos.y][pos.x] = self.wall

    def get_walls(self, only_inner_walls=False):
        walls = []
        for y, row in enumerate(self.the_area):
            for x, col in enumerate(row):
                if col == self.wall:
                    if only_inner_walls and (x == 0 or y == 0 or x == len(row) or y == len(self.the_area)):
                        continue
                    walls.append(Position(x, y))
        return walls

    @staticmethod
    def get_next_pos_for_pos(pos: Position, d: Direction):
        return Position(pos.x + d.move().x, pos.y + d.move().y)

    def get_neighbours(self, pos: Position):
        neighbours = {}
        for d in Direction:
            neighbours[d] = self.get_next_pos_for_pos(pos, d)
        return neighbours

class AbsRoom(Area):
    mover: Mover

    def __init__(self, a: list[list[str|int]],m: Mover):
        self.the_area = deepcopy(a)
        self.original_area = deepcopy(a)
        self.mover = m

    @abstractmethod
    def get_score(self):
        pass

    def get_next_pos_for_mover(self, d: Direction):
        return Position(self.mover.position.x + d.move().x, self.mover.position.y + d.move().y)


    def move_mover(self, n_pos: Position):
        self.change_spot(n_pos, self.mover.visual)
        self.change_spot(self.mover.position, self.empty_space)
        self.mover.move(n_pos)

    @abstractmethod
    def move(self, d: Direction):
        pass


class AbsRoomWithMoveableObjects(AbsRoom):
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
        self.the_area = deepcopy(a)
        self.original_area = deepcopy(a)
        self.starting_direction = starting_direction
        for y, row in enumerate(self.the_area):
            for x, col in enumerate(row):
                if col == self.starting_symbol:
                    self.starting_position = Position(x, y)
                if col == self.end_symbol:
                    self.end_position = Position(x, y)
        self.counter = count()

    # def get_path_count(self):

    def add_start(self, pos: Position):
        self.change_spot(pos, self.starting_symbol)
        self.original_area[pos.y][pos.x] = self.starting_symbol
        self.starting_position = pos

    def add_end(self, pos: Position):
        self.change_spot(pos, self.end_symbol)
        self.original_area[pos.y][pos.x] = self.end_symbol
        self.end_position = pos

    def reset(self):
        self.the_area = deepcopy(self.original_area)

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

    def manhattan_heuristic(self, current: Position):
        goal = self.end_position
        return abs(current.x - goal.x) + abs(current.y - goal.y)

    def solve_maze_a_star(self, heuristic=None, det_tentative_cost=None, direction_matters=False):
        if heuristic is None:
            heuristic = self.manhattan_heuristic
        if det_tentative_cost is None:
            det_tentative_cost = determine_tentative_cost

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

                if direction_matters:
                    tentative_score = det_tentative_cost(path_score, current_pos, Direction.from_symbol(current_direction_symbol), direction)
                else:
                    tentative_score = det_tentative_cost(path_score, current_pos)

                if neighbour_pos not in path_score or tentative_score < path_score[neighbour_pos]:
                    path[neighbour_pos] = (current_pos, direction.get_symbol())
                    path_score[neighbour_pos] = tentative_score
                    estimated_score[neighbour_pos] = tentative_score + heuristic(neighbour_pos)
                    heapq.heappush(to_visit, (estimated_score[neighbour_pos], next(self.counter), neighbour_pos, direction.get_symbol()))
            loop += 1

        return {}, 0

    def bfs_find_all_paths(self):
        """Find all shortest paths from 'S' to 'E' using BFS"""
        start = self.starting_position
        end = self.end_position

        queue = deque([(start, [start])])  # Queue to store (position, path taken so far)
        visited = set([start])  # Set of visited positions to avoid revisiting

        shortest_paths = []
        shortest_length = float('inf')

        while queue:
            current_pos, path = queue.popleft()

            # If we reach the endpoint
            if current_pos == end:
                # If we find a shorter path, reset the shortest paths list
                if len(path) < shortest_length:
                    shortest_paths = [path]  # Found a new shortest path
                    shortest_length = len(path)
                # If the path length matches the shortest length, add it as a valid path
                elif len(path) == shortest_length:
                    shortest_paths.append(path)  # Another shortest path

            # Explore neighbors (up, down, left, right)
            for direction in Direction:
                d = direction.move()
                next_pos = Position(current_pos.x + d.x, current_pos.y + d.y)

                # Check if the position is valid, not a wall, and hasn't been visited in the current path
                if self.is_in_map(next_pos) and next_pos not in visited and self.get_spot(next_pos) != self.wall:
                    visited.add(next_pos)
                    queue.append((next_pos, path + [next_pos]))

        return shortest_paths

