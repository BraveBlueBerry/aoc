import re
from math import floor

import numpy as np
from PIL import Image

i = open("input.txt", "r")

at: ('8400', '5400')

data = []
matches = re.findall('-?\d+,-?\d+', i.read())

i.close()


class Robot:
    position = [0,0]
    def __init__(self, v: tuple, starting_position: tuple):
        self.velocity = v
        self.starting_position = starting_position
        self.position = starting_position

    def __repr__(self):
        return f'Robot is at {self.position} and moves {self.velocity} per second.'

    def move(self, seconds, b_w, b_h):
        move = (self.velocity[0] * seconds, self.velocity[1] * seconds)
        new_pos = [(move[0] + self.position[0]) % b_w,
                   (move[1] + self.position[1]) % b_h]
        self.position = new_pos
        return new_pos


class Bathroom:
    width = 11
    height = 7
    area = []
    empty_space = 0
    robots = []

    def __init__(self, w, h):
        self.width = w
        self.height = h
        for y in range(h):
            self.area.append([])
            for x in range(w):
                self.area[y].append(self.empty_space)

    def __repr__(self):
        string = ''
        for y, row in enumerate(self.area):
            for x, col in enumerate(row):
                string += str(self.area[y][x])
            string += '\n'
        return string

    def add_robot(self, r: Robot):
        pos = r.position
        spot = self.area[pos[1]][pos[0]]
        if spot == self.empty_space:
            self.area[pos[1]][pos[0]] = 1
        else:
            self.area[pos[1]][pos[0]] += 1
        print(spot)
        print(self.area[pos[1]][pos[0]])
        self.robots.append(robot)

    def add_second(self):
        for robot in robots:
            old_pos = robot.position
            new_pos = robot.move(1, self.width, self.height)
            self.area[old_pos[1]][old_pos[0]] -= 1
            if self.area[old_pos[1]][old_pos[0]] == 0:
                self.area[old_pos[1]][old_pos[0]] = self.empty_space
            if self.area[new_pos[1]][new_pos[0]] == self.empty_space:
                self.area[new_pos[1]][new_pos[0]] = 1
            else:
                self.area[new_pos[1]][new_pos[0]] += 1

    def get_quadrant(self, x):
        if x > 3:
            return
        max_col = floor(self.height / 2)
        print(max_col)

    def print_quadrants(self):
        printable = ''
        for y, row in enumerate(self.area):
            for x, col in enumerate(row):
                col_str = str(col)
                if x < floor(self.width / 2):
                    if y < floor(self.height / 2):
                        # First quadrant up - left
                        printable += col_str
                    elif y > floor(self.height / 2):
                        # Third quadrant bottom - left
                        printable += col_str
                    else:
                        printable += ' '
                elif x > floor(self.width / 2):
                    if y < floor(self.height / 2):
                        # Second quadrant top - right
                        printable += col_str
                    elif y > floor(self.height / 2):
                        # Fourth quadrant bottom - right
                        printable += col_str
                    else:
                        printable += ' '
                else:
                    printable += ' '

            printable += '\n'
        print(printable)

    def get_safety_factor(self):
        count = 1
        quadrants = [0, 0, 0, 0]
        for y, row in enumerate(self.area):
            for x, col in enumerate(row):
                if col == self.empty_space:
                    continue
                if x < floor(self.width / 2):
                    if y < floor(self.height / 2):
                        # First quadrant up - left
                        quadrants[0] += col
                    elif y > floor(self.height / 2):
                        # Third quadrant bottom - left
                        quadrants[2] += col
                elif x > floor(self.width / 2):
                    if y < floor(self.height / 2):
                        # Second quadrant top - right
                        quadrants[1] += col
                    elif y > floor(self.height / 2):
                        # Fourth quadrant bottom - right
                        quadrants[3] += col

        print(quadrants)
        for quadrant in quadrants:
            count *= quadrant
        return count


robots = []
v = tuple()
p = list()
for i, match in enumerate(reversed(matches)):
    match = match.split(",")
    for x, mat in enumerate(match):
        match[x] = int(mat)
    if i % 2 == 0 or i == 0:
        v = tuple(match)
    else:
        p = match
        robots.append(Robot(v, p))

bathroom = Bathroom(101, 103)
for robot in robots:
    bathroom.add_robot(robot)

for i in range(10000):
    bathroom.add_second()
    image = Image.fromarray(np.array(bathroom.area).astype(np.uint8) * 255, mode='L')
    image.save(f'images/{i + 1}.png')




# print("____")
# print(robots[len(robots)-2])
# print(bathroom)

print(bathroom.get_safety_factor())
bathroom.print_quadrants()