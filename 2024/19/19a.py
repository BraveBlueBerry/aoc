from functools import cache

i = open("input.txt", "r")

parts = i.read().split('\n\n')

i.close()

available_towel_patterns, desired_towel_patterns = (
    [pattern.strip() for pattern in parts[0].split(',')],
    [pattern.strip() for pattern in parts[1].split('\n')]
)

@cache
def get_options(d_pattern: str, b_pattern: str):
    options = []
    for pattern in available_towel_patterns:
        if pattern == d_pattern[len(b_pattern):len(b_pattern) + len(pattern)]:
            options.append(pattern)
    return options


def bfs(goal):
    to_visit = []
    starting_options = get_options(goal, '')
    print(starting_options)
    for starting_option in starting_options:
        to_visit.append([starting_option])
    print(to_visit)
    loop = 0
    options = 0
    while to_visit:
        current = to_visit.pop(0)
        if ''.join(current) == goal:
            options += 1
            print(options)

        if desired_pattern.startswith(''.join(current)):
            for option in get_options(goal, ''.join(current)):
                to_visit.append(current + [option])

        loop += 1

    return options

total_options = 0
for desired_pattern in desired_towel_patterns:
    potential = []
    for available_pattern in available_towel_patterns:
        if available_pattern in desired_pattern:
            potential.append(available_pattern)

    print(f'~~~~~~~~~~~~~~~~~~~~ WE WANT: {desired_pattern} ~~~~~~~~~~~~~~~~~~~~')

    total_options += bfs(desired_pattern)


print(total_options)