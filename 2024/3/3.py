import re

f = open("input.txt", "r")
corrupted_memory = f.read()

matches = re.findall(r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)", corrupted_memory)

total = 0

do_count = True
do = "do()"
dont = "don't()"

for match in matches:
    numbers = re.findall(r"\d{1,3}", match)
    if len(numbers) == 0:
        do_count = match == do
        continue
    if do_count:
        total += int(numbers[0]) * int(numbers[1])

print(total)
