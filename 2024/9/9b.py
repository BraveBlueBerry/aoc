from collections import deque

i = open("input_big.txt", "r")

disk_map = (list(i.read().strip()))

i.close()

block_representation = []
is_block = True
block_id = 0

for d in disk_map:
    digit = int(d)
    if is_block:
        block_representation.extend([str(block_id)] * digit)
        is_block = False
        block_id += 1
    else:
        block_representation.extend(['.'] * digit)
        is_block = True

print(block_representation)
print('\n\n\n')

def determine_free_space(l, wanted_space: int, start_looking_from, end_looking_at):
    look_from = start_looking_from
    # print(wanted_space, start_looking_from, end_looking_at)
    while look_from < end_looking_at:
        count_free_space = 0
        last_i = 0
        for i in range(look_from, end_looking_at):
            if l[i] == '.':
                count_free_space += 1
            else:
                break
        if count_free_space >= wanted_space:
            return look_from
        # print(f'det_free_space: {look_from}, {last_i}, {wanted_space}, {count_free_space}, {len(l)}')
        look_from = last_i + look_from + 1
    return 0




#
# free_space_index = 0
# for reversed_index, block in enumerate(reversed(block_representation)):
#     current_index = len(block_representation) - reversed_index - 1
#     if block is not '.':
#         total = 0
only_nums = list(deque(x for x in block_representation if x != '.'))
for reversed_index, block in enumerate(reversed(block_representation)):
    current_index = len(block_representation) - reversed_index - 1
    if block != '.':
        count_file_size = 0
        if len(only_nums) <= 0:
            break
        current_file = only_nums[-1]
        if current_file != block:
            continue
        print(current_file)
        while only_nums and only_nums[-1] == current_file:
            only_nums.pop()
            count_file_size += 1

        # print(f'current file = {current_file}')
        place_for_file = determine_free_space(block_representation, count_file_size, 0, current_index)
        # print(current_index, place_for_file, count_file_size)
        if place_for_file != 0:
            # print('hello')

            block_representation = ['.' if x == current_file else x for x in block_representation]

            for x in range(count_file_size):
                block_representation[place_for_file + x] = current_file
        # print(block_representation)

    else:
        continue
        # exit()

print(block_representation)
checksum = 0
for index, block in enumerate(block_representation):
    if block != '.':
        checksum += index * int(block)

print(checksum)