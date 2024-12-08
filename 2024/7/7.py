import re
import itertools
from copy import deepcopy

i = open("input_big.txt", "r")

equations = []

for line in i:
    values = [int(v) for v in re.findall("\d{1,99999}", line)[1:]]
    equations.append({int(re.findall("\d{1,99999}", line)[0]): values})
    print(f"Extracted values: {values}")

i.close()

operators = ['+', '*', '||']

def evaluate_expression(vals, o_combo):
    r = int(vals[0])
    # print(f"    Initial value: {r}")
    adjusted_vals = deepcopy(vals)
    adjusted_combo = deepcopy(o_combo)

    # if adjusted_combo.count('||') > 0:
    #     print(f'|| in combo, combo is: {adjusted_combo}')
    #     combine_indices = [index for index, value in enumerate(adjusted_combo) if value == '||']
    #     for combine_index in reversed(combine_indices):
    #         new_val = int(str(vals[combine_index]) + str(vals[combine_index + 1]))
    #         del adjusted_combo[combine_index]
    #         del adjusted_vals[combine_index]
    #         del adjusted_vals[combine_index]
    #         adjusted_vals.insert(combine_index, new_val)



    for i, operator in enumerate(adjusted_combo):
        if operator == '+':
            r += int(adjusted_vals[i + 1])
        elif operator == '*':
            r *= int(adjusted_vals[i + 1])
        elif operator == '||':
            r = int(str(r) + str(adjusted_vals[i + 1]))

    return r

solution_one = 0

for x in equations:
    wanted_total = int(list(x.keys())[0])
    values = list(x.values())[0]

    operator_combinations = list(itertools.product(operators, repeat=len(values) - 1))

    loop = 1
    tried_results = []

    for operator_combo in operator_combinations:
        # print(f"Trying: {values} with {operator_combo} (Wanted: {wanted_total})")
        result = evaluate_expression(values, list(operator_combo))

        if result == wanted_total:
            solution_one += result
            # print(f"Match found! {values} with {operator_combo} => {result}")
            break
        # print('=============')
        tried_results.append(result)
        # if loop == len(operator_combinations):
            # print(f"Not found: {wanted_total}:  {values} ")

        loop +=1
    # print('----------------------------------')


print(solution_one)