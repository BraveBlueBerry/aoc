from collections import deque, defaultdict

i = open("input.txt", "r")

parts = i.read().split('\n\n')

i.close()

class gate:
    inputs: tuple
    type: str
    output_wire: str
    values : dict
    output: int

    def __init__(self, l, r, t, o):
        self.inputs = (l, r)
        self.type = t
        self.output_wire = o
        self.values = defaultdict(list)


    def __repr__(self):
        string = f'{self.inputs[0]} {self.type} {self.inputs[1]} -> {self.output_wire}'
        if len(self.values) > 0:
            string += ' {'
        for i, v in enumerate(self.values):
            string += f'{v}: {self.values[v]}'
            if i == 0 and len(self.values) > 1:
                string += ' '
        if len(self.values) > 0:
            string += '}'
        return string

    def has_one_input(self):
        return len(self.values) == 1

    def has_both_inputs(self):
        return len(self.values) == 2

    def is_z_gate(self):
        return 'z' in self.output_wire

    def set_and_get_output(self):
        values = [int(value) for value in self.values.values()]
        match self.type:
            case 'AND':
                self.output = values[0] & values[1]
                return self.output
            case 'XOR':
                self.output = values[0] ^ values[1]
                return self.output
            case 'OR':
                self.output = values[0] | values[1]
                return self.output

    def __lt__(self, other):
        return self.output_wire < other.output_wire

inputs = [line.strip().split(': ') for line in parts[0].split('\n')]

gates = []
for line in parts[1].split('\n'):
    x = line.strip().replace('-> ', '').split(' ')
    gates.append(gate(x[0], x[2], x[1], x[3]))

input_to_gate = defaultdict(list)

# Lookup dict
for g in gates:
    for inp in g.inputs:
        input_to_gate[inp].append(g)

todo = deque(inputs)
waiting_gates = []
while todo:
    current = todo.pop()
    wire = current[0] # y04
    carries = current[1] # 0 / 1

    if wire in input_to_gate:
        for gate in input_to_gate[wire]:
            gate.values[wire] = carries
            if gate.has_both_inputs():
                gate.set_and_get_output()
                todo.appendleft([gate.output_wire, gate.output])


output = ''
gates.sort()
for gate in reversed(gates):
    if gate.is_z_gate():
        output += str(gate.output)
print(f'Final output: {output}')
print(f'And in binary: {int(output, 2)}')


