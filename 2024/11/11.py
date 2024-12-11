import re
from copy import deepcopy
from functools import cache

small_input = 'xxx'

og_stones = re.findall('\d{1,999999999}', small_input)
for i, og_stone in enumerate(og_stones):
    og_stones[i] = int(og_stone)

def blink(stones : list):
    new_stones = deepcopy(stones)
    inserted = 0
    for i, stone in enumerate(stones):
        str_stone = str(stone)
        if stone == 0:
            new_stones[i + inserted] = 1
        elif len(str_stone) % 2 == 0:
            half = int(len(str_stone) / 2)
            stone_part_one = int(str_stone[:half])
            stone_part_two = int(str_stone[half:])
            new_stones[i + inserted] = stone_part_one
            new_stones.insert(i + inserted + 1, stone_part_two)
            inserted += 1
        else:
            new_stones[i + inserted] = stone * 2024
    return new_stones

def blink_many_times(times: int, stones: list):
    for i in range(times):
        stones = blink(stones)
        print(stones)

    return stones

@cache
def blink_v2(stone, times):
    if times == 0:
        return 1
    str_stone = str(stone)
    if stone == 0:
        return blink_v2(1, times - 1)
    elif len(str_stone) % 2 == 0:
        half = int(len(str_stone) / 2)
        stone_part_one = int(str_stone[:half])
        stone_part_two = int(str_stone[half:])
        return blink_v2(stone_part_one, times - 1) + blink_v2(stone_part_two, times - 1)
    else:
        return blink_v2(stone * 2024, times - 1)

stones_after_blinking = blink_many_times(25, [872027])
print(f'part one: {len(stones_after_blinking)}')

# count = 0
# for stone in og_stones:
#     count += blink_v2(stone, 75)
# print(f'part two: {count}')
