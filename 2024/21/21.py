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

from common.a_star_alts import tentative_score_expensive_corners
from common.map_solver import Maze
from common.navigation_utils import Position

with open("input.txt", "r") as file:
    result = [list(line.strip()) for line in file]
print(result)

numpad_area = [
    ['.', '.', '.',],
    ['.', '.', '.',],
    ['.', '.', '.',],
    ['#', '.', 'S',]
]

arrows_area = [
    ['#', '.', 'S', ],
    ['.', '.', '.', ]
]

numpad = Maze(numpad_area)
arrows = Maze(arrows_area)

navNum = {
    'A' : Position(2, 3),
    '0' : Position(1, 3),
    '1' : Position(0, 2),
    '2' : Position(1, 2),
    '3' : Position(2, 2),
    '4' : Position(0, 1),
    '5' : Position(1, 1),
    '6' : Position(2, 1),
    '7' : Position(0, 0),
    '8' : Position(1, 0),
    '9' : Position(2, 0)
}

navArrows = {
    'A' : Position(2, 0),
    '<' : Position(0, 1),
    '>' : Position(2, 1),
    '^' : Position(1, 0),
    'v' : Position(1, 1)
}

# numpad.add_end(navNum['0'])
# score, path = numpad.solve_maze_a_star()
# directional_path = path[1]
# print(numpad)
# print(score)
# print(path)
# print(directions)

def extract_and_convert(code):
    the_extracted_stuff = int(re.search(r'\d+', code).group())
    print(f"Extracted Numeric Part: {the_extracted_stuff}")
    return the_extracted_stuff

def get_all_options_for_command(keypad: Maze, command: list, navigation: dict):
    next_command = []
    keypad.add_start(navigation['A'])
    for key in command:
        keypad.reset()
        keypad.add_end(navigation[key])
        score, path = numpad.solve_maze_a_star(det_tentative_cost=tentative_score_expensive_corners,
                                               direction_matters=True)
        print(score)
        print(path[1])
        print(numpad)
        next_command += path[1]
        next_command.append('A')
        keypad.add_start(navigation[key])
        print('--------------')

total = 0
totals_per = []

for command in result:

    command_1 = []
    button_presses = 0
    numpad.add_start(navNum['A'])
    for key in command:
        numpad.reset()
        numpad.add_end(navNum[key])
        score, path = numpad.solve_maze_a_star(det_tentative_cost=tentative_score_expensive_corners, direction_matters=True)
        print(score)
        print(path[1])
        print(numpad)
        button_presses += score
        command_1 += path[1]
        command_1.append('A')
        numpad.add_start(navNum[key])
        print('--------------')

    print('=====================================COMMAND1=====================================')
    print(command_1)
    print(len(command_1))
    print('=====================================COMMAND1=====================================')

    arrows.add_start(navArrows['A'])

    command_2 = []
    for key in command_1:
        print(f'Key = {key}')
        arrows.reset()
        if arrows.starting_position == navArrows[key]:
            print('We\'re already at the spot')
            command_2.append('A')
            button_presses += 1
            continue
        arrows.add_end(navArrows[key])
        print(arrows)
        score, path = arrows.solve_maze_a_star(det_tentative_cost=tentative_score_expensive_corners, direction_matters=True)
        print(score)
        print(path[1])
        print(arrows)
        button_presses += score + 1
        command_2 += path[1]
        command_2.append('A')
        arrows.add_start(navArrows[key])
        print('--------------')

    print('=====================================COMMAND2=====================================')
    print(command_2)
    print(len(command_2))
    print('=====================================COMMAND2=====================================')

    arrows.add_start(navArrows['A'])

    command_3 = []
    for key in command_2:
        print(f'Key = {key}')
        arrows.reset()
        if arrows.starting_position == navArrows[key]:
            print('We\'re already at the spot')
            command_3.append('A')
            button_presses += 1
            continue
        arrows.add_end(navArrows[key])
        score, path = arrows.solve_maze_a_star(det_tentative_cost=tentative_score_expensive_corners, direction_matters=True)
        print(score)
        print(path[1])
        print(arrows)
        button_presses += score + 1
        command_3 += path[1]
        command_3.append('A')
        arrows.add_start(navArrows[key])
        print('--------------')

    print('=====================================COMMAND3=====================================')
    print("".join(command_1))
    print("".join(command_2))
    print("".join(command_3))
    print(len(command_3))
    print('=====================================COMMAND3=====================================')

    numeric_part = extract_and_convert("".join(command))
    total += (len(command_3) * numeric_part)
    totals_per.append((len(command_3), numeric_part))




print(f'TOTAL = {total}')
print(totals_per)
testing_total = 0
for pair in totals_per:
    intermediate = pair[0] * pair[1]
    print(f"Length: {pair[0]}, Numeric Part: {pair[1]}, Product: {intermediate}")
    testing_total += intermediate
print(testing_total)
