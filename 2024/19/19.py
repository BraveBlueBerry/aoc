from copy import deepcopy

i = open("input.txt", "r")

parts = i.read().split('\n\n')

i.close()

available_towel_patterns, desired_towel_patterns = (
    [pattern.strip() for pattern in parts[0].split(',')],
    [pattern.strip() for pattern in parts[1].split('\n')]
)
print(available_towel_patterns)
print(desired_towel_patterns)

available_towel_patterns.sort(key=len, reverse=True)

print(available_towel_patterns)
print(len(desired_towel_patterns))

possible = 0

for desired_pattern in desired_towel_patterns:
    print(f'~~~~~~~~~~~~~~~~~~~~~~ WE WANT: {desired_pattern} ~~~~~~~~~~~~~~~~~~~~~~')
    building_pattern = ''
    potential = []
    for available_pattern in available_towel_patterns:
        if available_pattern in desired_pattern:
            potential.append(available_pattern)
    print(desired_pattern)
    loop = 0
    found_next = True
    while (building_pattern != desired_pattern) and found_next:
        found_next = False
        patterns_to_remove = []
        print(building_pattern)
        for pattern in potential:
            print(f'{pattern} vs {desired_pattern[len(building_pattern):len(building_pattern) + len(pattern)]}')
            # print(f'Building pattern length: {len(building_pattern)}, Current pattern length: {len(pattern)}')
            # print(f'Checking part of desired pattern: {desired_pattern[len(building_pattern):len(building_pattern) + len(pattern)]}')

            # Check if the current pattern matches the next part of the desired pattern
            if pattern == desired_pattern[len(building_pattern):len(building_pattern) + len(pattern)]:
                building_pattern += pattern
                found_next = True
                print(f'Match found: {building_pattern}')

                # Check if the pattern can match further in the desired pattern
                if pattern not in desired_pattern[len(building_pattern):]:
                    patterns_to_remove.append(pattern)
                print(f'Updated building pattern: {building_pattern}')

            # print('----------------------------------------------')

            # Remove patterns that are no longer useful
        for pattern in patterns_to_remove:
            potential.remove(pattern)
        loop += 1
        print(potential)
        print(f'===== {loop}x geprobeerd =====')
    if building_pattern == desired_pattern:
        possible += 1

print(f'{possible} of the {len(desired_towel_patterns)} designs are possible with the available towel patterns.')