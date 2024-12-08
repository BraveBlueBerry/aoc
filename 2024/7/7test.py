import itertools

# The values and the target total
values = [12, 31, 98, 2, 45]
target = 1678500
operators = ['+', '*']

# Function to evaluate the expression with the current combination of operators
def evaluate_expression(values, operators_combo):
    result = values[0]
    for i, operator in enumerate(operators_combo):
        if operator == '+':
            result += values[i + 1]
        elif operator == '*':
            result *= values[i + 1]
    return result

# Generate all combinations of operators (between each pair of values)
operator_combinations = list(itertools.product(operators, repeat=len(values) - 1))

# Check each combination
match_found = False
for operator_combo in operator_combinations:
    result = evaluate_expression(values, operator_combo)
    if result == target:
        match_found = True
        print(f"Match found! Expression: {values[0]} {operator_combo[0]} {values[1]} {operator_combo[1]} {values[2]} ... = {result}")
        break

if not match_found:
    print(f"No combination of operators produces the target {target}.")
