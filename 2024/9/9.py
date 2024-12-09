i = open("input_big.txt", "r")

disk_map = (list(i.read().strip()))

i.close()

# print(disk_map)

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


free_space_index = 0
debug = False
for reversed_index, block in enumerate(reversed(block_representation)):
    # print(block_representation)
    current_index = len(block_representation) - reversed_index - 1
    # if debug: print(f'[{current_index}] => {block}')
    if block != '.':
        # if debug: print(f'Free space index pointer at: {free_space_index}')
        found_next_empty_space = False
        while not found_next_empty_space:
            if block_representation[free_space_index] == '.':
                # if debug: print(f'   Found free space at: {free_space_index}')
                found_next_empty_space = True
            else:
                # if debug: print(f'   Upping the free space index: {free_space_index}')
                free_space_index += 1
        if free_space_index <= current_index:
            # print(f'Placing {current_index} with {block} at new position: {free_space_index}')
            block_representation[free_space_index] = block
            # print(f'And replacing {current_index} with . at new position')
            block_representation[current_index] = '.'
        else:
            break

print(block_representation)
for index, block in enumerate(block_representation):
    print(f'[{index}] => {block}')

checksum = 0
for index, block in enumerate(block_representation):
    if block != '.':  # Skip free spaces
        checksum += index * int(block)

print(checksum)
