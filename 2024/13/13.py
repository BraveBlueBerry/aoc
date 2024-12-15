import itertools
import re

class SlotMachine:
    claw = [0,0]
    buttons = ['A', 'B']
    cost = 0
    def __init__(self, button_a: tuple, button_b: tuple, prize_location: tuple):
        self.button_a = (int(button_a[0]), int(button_a[1]))
        self.button_b = (int(button_b[0]), int(button_b[1]))
        self.prize_location = (int(prize_location[0]), int(prize_location[1]))

    def press_button_a_once(self):
        self.claw = [self.claw[0] + self.button_a[0], self.claw[1] + self.button_a[1]]
        self.cost += 3

    def press_button_b_once(self):
        self.claw = [self.claw[0] + self.button_b[0], self.claw[1] + self.button_b[1]]
        self.cost += 1

    def press_button_a_times(self, times: int):
        self.claw = [self.claw[0] + (self.button_a[0] * times), self.claw[1] + (self.button_a[1] * times)]
        self.cost += (3 * times)


    def press_button_b_times(self, times: int):
        self.claw = [self.claw[0] + (self.button_b[0] * times), self.claw[1] + (self.button_b[1] * times)]
        self.cost += (1 * times)

    def reset_machine(self):
        self.reset_cost()
        self.reset_claw()

    def reset_claw(self):
        self.claw = [0,0]

    def reset_cost(self):
        self.cost = 0

    def is_claw_at_prize(self):
        return tuple(self.claw) == self.prize_location

    def print_claw(self):
        print(f'Claw is at: {self.claw}')

    def print_cost(self):
        print(f'Amount of tokens used: {self.cost}')

    def is_prize_posible_after_times(self, times: int):
        max_x = self.button_a[0] * times + self.button_b[0] * times
        max_y = self.button_a[1] * times + self.button_b[1] * times

        if max_x < self.prize_location[0]:
            return False
        if max_y < self.prize_location[1]:
            return False
        return True

    def is_a_cheaper_for_x(self):
        return (self.button_a[0] / 3) > self.button_b[0]

    def is_a_cheaper_for_y(self):
        return (self.button_a[1] / 3) > self.button_b[1]

    def print_some_debugging(self):
        print(f'is button a cheaper for x? A / 3: {self.button_a[0] / 3} vs B: {self.button_b[0]} => {(self.button_a[0] / 3) > self.button_b[0]}')
        print(f'is button a cheaper for y? A / 3: {self.button_a[1] / 3} vs B: {self.button_b[1]} => {(self.button_a[1] / 3) > self.button_b[1]}')
        print(f'{self.prize_location[0] / self.button_a[0]}')

    def __str__(self):
        return f'============== Slot Machine ==============\nButton A moves X: {self.button_a[0]} and Y: {self.button_a[1]}\nButton B moves X: {self.button_b[0]} and Y: {self.button_b[1]}\nThe prize is located at: {self.prize_location}\n=========================================='

i = open("input.txt", "r")

at: ('8400', '5400')

data = []
matches = re.findall('\d+, Y[+|=]\d+', i.read())

i.close()

# for i, match in enumerate(matches):
#     xy = tuple(re.findall('\d{1,999999999}', match))
#     print(xy)
slot_machines = []
processed_matches = [tuple(re.findall(r'\d+', item)) for item in matches]
for i in range(0, len(processed_matches), 3):
    chunk = processed_matches[i:i + 3]
    slot_machines.append(SlotMachine(chunk[0], chunk[1], chunk[2]))

amount_of_tokens_needed = 0
for slot_machine in slot_machines:
    print(slot_machine)
    if slot_machine.is_prize_posible_after_times(100):
        valid_options = []
        for a in range(100):
            for b in range(100):
                slot_machine.press_button_a_times(a)
                slot_machine.press_button_b_times(b)
                if slot_machine.is_claw_at_prize():
                    valid_options.append({"cost": slot_machine.cost, "press_buttons": (a, b)})
                slot_machine.reset_machine()

        print(valid_options)
        if len(valid_options) > 0:
            cheapest = 99999999999999999999999999999
            for valid_option in valid_options:
                cheapest = valid_option['cost'] if valid_option['cost'] < cheapest else cheapest

            amount_of_tokens_needed += cheapest


print(amount_of_tokens_needed)






