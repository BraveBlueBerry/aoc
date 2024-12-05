i = open("input_big.txt", "r")

look_for_word = "XMAS"
board = []
lfw_list = list(look_for_word)

for line in i:
    board.append(list(line.replace("\n", "")))

def check_neighbours(current_location):
    row = board[current_location[1]]
    current_letter = row[current_location[0]]
    neighbouring_coordinates = [                                # fe current_location = [2, 2]
        [current_location[0] - 1, current_location[1]],         # [1, 2] left
        [current_location[0] + 1, current_location[1]],         # [2, 2] right
        [current_location[0], current_location[1] - 1],         # [2, 1] up
        [current_location[0], current_location[1] + 1],         # [2, 3] down
        [current_location[0] - 1, current_location[1] - 1],     # [1, 1] up left
        [current_location[0] + 1, current_location[1] - 1],     # [3, 1] up right
        [current_location[0] - 1, current_location[1] + 1],     # [2, 3] down left
        [current_location[0] + 1, current_location[1] + 1],     # [2, 3] down right
    ]

    looking_for_letter = ""

    for i in range(len(lfw_list)):
        if lfw_list[i] == current_letter:
            looking_for_letter = lfw_list[i + 1]

    candidate_neighbours = []
    for coord in neighbouring_coordinates:
        if is_on_board(coord) and (board[coord[1]][coord[0]] == looking_for_letter):
            candidate_neighbours.append(coord)

    return candidate_neighbours

def is_on_board(coord):
    return not (((coord[0] < 0) or (coord[0] >= len(row))) or ((coord[1] < 0) or (coord[1] >= len(board))))

def search(direction, coord, current_char):
    if current_char == len(look_for_word) + 1:
        return True
    next_coord = [coord[0] + direction[0], coord[1] + direction[1]]
    if is_on_board(next_coord):
        next_neighbour = board[next_coord[1]][next_coord[0]]
    else:
        return False
    if next_neighbour == lfw_list[current_char - 1]:
        return search(direction, [coord[0] + direction[0], coord[1] + direction[1]], current_char + 1)
    else:
        return False


total = 0
total2 = 0
for y in range(len(board)):
    row = board[y]
    for x in range(len(row)):
        letter = row[x]
        # part 1
        if letter == lfw_list[0]:

            neighbours = check_neighbours([x, y])

            for neighbour in neighbours:
                direction = (neighbour[0] - x, neighbour[1]- y)

                if search(direction, neighbour, 3):
                    total +=1

        # part 2
        if letter == "A" and (0 < y < (len(board) - 1)) and (0 < x < (len(row) - 1)):
            upright = board[y - 1][x + 1]
            bottomleft = board[y + 1][x - 1]
            upleft = board[y - 1][x - 1]
            bottomright = board[y + 1][x + 1]

            if ((upright == "M" and bottomleft == "S")
                or (upright == "S" and bottomleft == "M")) \
                and ((upleft == "M" and bottomright == "S")
                or (upleft == "S" and bottomright == "M")):
                total2 += 1

print("============ TOTAL: " + str(total) + " ============")
print("============ TOTAL2: " + str(total2) + " ============")

