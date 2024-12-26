from math import floor

with open("input.txt", "r") as file:
    secret_numbers = [int(line.strip()) for line in file]

def evolve(number: int):
    secret_number = number
    result = secret_number * 64
    secret_number = mix(secret_number, result)
    secret_number = prune(secret_number)
    result = int(floor(secret_number / 32))
    secret_number = mix(secret_number, result)
    secret_number = prune(secret_number)
    result = secret_number * 2048
    secret_number = mix(secret_number, result)
    secret_number = prune(secret_number)
    return secret_number

def mix(secret_number: int, value: int):
    return secret_number ^ value

def prune(secret_number: int):
    return secret_number % 16777216

total = 0

for sn in secret_numbers:
    new_sn = sn
    for i in range(2000):
        new_sn = evolve(new_sn)
    total += new_sn

print(total)