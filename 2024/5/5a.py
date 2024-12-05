from math import floor

rules_f = open("rules_big.txt", "r")
printing_f = open("printing_big.txt", "r")

rules = {}
updates = []

for line in rules_f:
    rule = line.strip().split("|")
    if rule[0] not in rules.keys():
        rules[rule[0]] = [rule[1]]
    else:
        rules[rule[0]].append(rule[1])

for line in printing_f:
    updates.append(line.strip().split(","))

valid_updates_count = 0
invalid_updates = {}
valid_updates = []
sum = 0
id = 1

for update in updates:
    looked_over = []
    update_is_valid = True
    for i, page in enumerate(update):
        if i == 0:
            looked_over.append(page)
            continue
        if page in rules:
            should_come_after = rules[page]
            for looked_at_page in looked_over:
                if looked_at_page in should_come_after:
                    update_is_valid = False
                    if id in invalid_updates:
                        invalid_updates[id]["wrong_page"].append(page)
                    else:
                        invalid_updates[id] = {"update": update, "wrong_page": [page]}

        looked_over.append(page)

    if update_is_valid:
        valid_updates_count += 1
        sum += int(update[floor(len(update) / 2)])

    id += 1

print(f"Oplossing eerste deel: {sum}")

new_valid_updates = []
new_valid_updates_sum = 0

for id in invalid_updates:
    current_update = invalid_updates[id]['update']

    for wrong_page in invalid_updates[id]['wrong_page']:
        should_come_after = rules[wrong_page]
        index_wrong_page = current_update.index(wrong_page)
        the_pages_that_should_come_after = []
        pages_before = current_update[:index_wrong_page]
        should_move_before_index = None
        for x in should_come_after:
            for y in pages_before:
                if x == y:
                    should_move_before_index = pages_before.index(y)

        if not should_move_before_index is None:
            current_update.remove(wrong_page)
            current_update.insert(should_move_before_index, wrong_page)

    new_valid_updates.append(current_update)
    new_valid_updates_sum += int(current_update[floor(len(current_update) / 2)])

print(f"Oplossing tweede deel: {new_valid_updates_sum}")