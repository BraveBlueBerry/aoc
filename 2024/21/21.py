"""
      0   1   2
    +---+---+---+
 0  | 7 | 8 | 9 |
    +---+---+---+
 1  | 4 | 5 | 6 |
    +---+---+---+
 2  | 1 | 2 | 3 |
    +---+---+---+
 3      | 0 | A |
        +---+---+

        +---+---+
 0      | ^ | A |
    +---+---+---+
 1  | < | v | > |
    +---+---+---+
"""
import re
from collections import deque
from copy import deepcopy
from functools import cache
from itertools import product

from common.a_star_alts import tentative_score_expensive_corners
from common.map_solver import Maze
from common.navigation_utils import Position

with open("input.txt", "r") as file:
    result = [list(line.strip()) for line in file]
# print(result)

numpad_area = [
    ['.', '.', '.', ],
    ['.', '.', '.', ],
    ['.', '.', '.', ],
    ['#', '.', 'S', ]
]

arrows_area = [
    ['#', '.', 'S', ],
    ['.', '.', '.', ]
]

numpad = Maze(numpad_area)
arrows = Maze(arrows_area)

navNum = {
    'A': Position(2, 3),
    '0': Position(1, 3),
    '1': Position(0, 2),
    '2': Position(1, 2),
    '3': Position(2, 2),
    '4': Position(0, 1),
    '5': Position(1, 1),
    '6': Position(2, 1),
    '7': Position(0, 0),
    '8': Position(1, 0),
    '9': Position(2, 0)
}

navArrows = {
    'A': Position(2, 0),
    '<': Position(0, 1),
    '>': Position(2, 1),
    '^': Position(1, 0),
    'v': Position(1, 1)
}

def extract_and_convert(code):
    the_extracted_stuff = int(re.search(r'\d+', code).group())
    print(f"Extracted Numeric Part: {the_extracted_stuff}")
    return the_extracted_stuff

class Command:
    keys = []

    def __init__(self, keys):
        if isinstance(keys, Command):
            self.keys = keys.keys
        else:
            self.keys = list(keys)

    def __repr__(self):
        return "".join(self.keys)

    def __eq__(self, other):
        if type(other) == list:
            for i, x in enumerate(other):
                if x != self.keys[i]:
                    return False
            return True
        if type(other) == str:
            if other != "".join(self.keys):
                return False
            return True
        return False

    def __hash__(self):
        return hash("".join(self.keys))

    def __len__(self):
        return len(self.keys)

    def __getitem__(self, index):
        return self.keys[index]

    def __setitem__(self, index, value):
        self.keys[index] = value

    def __delitem__(self, index):
        del self.keys[index]

    def __iter__(self):
        return iter(self.keys)

    def append(self, key_press):
        self.keys.append(key_press)

    def __add__(self, other):
        if isinstance(other, Command):
            return Command(self.keys + other.keys)
        elif isinstance(other, list):
            return Command(self.keys + other)
        elif isinstance(other, str):
            return Command(self.keys + list(other))
        else:
            raise TypeError(f"Cannot add Command with {type(other)}")

    def __radd__(self, other):
        if isinstance(other, list):
            return Command(other + self.keys)
        else:
            raise TypeError(f"Cannot add {type(other)} with Command")


def get_directions_for_numpad(k: str):
    next_c = []
    numpad.reset()
    if numpad.starting_position == navNum[k]:
        return [Command(['A'])]
    numpad.add_end(navNum[k])
    paths = numpad.bfs_find_all_paths()
    for p in paths:
        # numpad.visualize_path(p['path'], p['directions'])
        next_c.append(Command(p['directions'][1:] + ['A']))
    return next_c

def get_commands_for_command(command: Command):
    next_commands = []
    arrows.reset()
    arrows.add_start(navArrows['A'])
    if len(command) == 1 and command[0] == 'A':
        return [Command(['A'])]
    for key_press in command:
        command_options_for_key_press = []
        if navArrows[key_press] == arrows.starting_direction:
            command_options_for_key_press.append(['A'])
        else:
            arrows.add_end(navArrows[key_press])
            paths = arrows.bfs_find_all_paths()
            for p in paths:
                # arrows.visualize_path(p['path'], p['directions'])
                command_options_for_key_press.append(Command(p['directions'][1:] + ['A']))
            arrows.add_start(navArrows[key_press])
        next_commands.append(command_options_for_key_press)
    combinations = list(product(*next_commands))

    commands = []
    for combi in combinations:
        c = Command(combi[0])
        for partial in combi[1:]:
            c += partial
        commands.append(c)

    return commands

@cache
def search(start: Command):
    queue = deque([[start, [], 0]])
    # visited = set(start)
    all_paths = []
    while queue:
        current, path, depth = queue.pop()
        if depth == 26:
            all_paths.append({'end': current, 'intermediate': path})
        else:
            for command in get_commands_for_command(current):
                queue.append([command, path + [current] ,depth + 1])

    shortest = all_paths[0]
    for path in all_paths:
        if len(path['end']) < len(shortest['end']):
            shortest = path
    return shortest

totals = set()

for code in result:
    numpad.add_start(navNum['A'])
    whole_command_for_code = Command([])
    robot_one = Command([])
    robot_two = Command([])
    for num in code:
        all_starters = get_directions_for_numpad(num)
        numpad.add_start(navNum[num])
        shortest_commands = []
        for starter in all_starters:
            result = search(Command(starter))
            shortest_commands.append(result)
        shortest = shortest_commands[0]
        for path in shortest_commands:
            if len(path['end']) < len(shortest['end']):
                shortest = path
        whole_command_for_code += shortest['end']
        robot_one += shortest['intermediate'][0]
        robot_two += shortest['intermediate'][1]
    totals.add((len(whole_command_for_code), extract_and_convert("".join(code))))

total = 0
for pair in totals:
    intermediate = pair[0] * pair[1]
    print(f"Length: {pair[0]}, Numeric Part: {pair[1]}, Product: {intermediate}")
    total += intermediate
print(total)


# ([((x: 2, y: 1), [(x: 2, y: 2), (x: 2, y: 1)]), ((x: 2, y: 3), [(x: 2, y: 2), (x: 2, y: 3)]), ((x: 1, y: 2), [(x: 2, y: 2), (x: 1, y: 2)])])