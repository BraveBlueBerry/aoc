# output 4,6,3,5,6,3,5,2,1,0
import re

i = open("input.txt", "r")

r = {}
program = []

for line in i:
    match = re.findall(r'Register ([ABC]): (\d+)', line)
    if len(match) == 1:
        r[match[0][0]] = int(match[0][1])

    program = re.findall(r'Program: (.*)', line)

i.close()
program = list(map(int, program[0].split(',')))

instruction_pointer = 0

class Computer:

    output = []
    operands = {
        4: 'A',
        5: 'B',
        6: 'C'
    }
    instruction_pointer = 0
    def __init__(self, registers):
        self.registers = registers
        print(self.registers)

    def run(self, program):
        print("Running the following program:")
        print(program)
        loop = 0
        while self.instruction_pointer < len(program):
            print(f'instruction pointer = {self.instruction_pointer}')
            self.voer_uit(program[self.instruction_pointer], program[self.instruction_pointer + 1])
            loop += 1
        print(",".join(self.output))


    def get_register_or_literal(self, operand):
        if operand in self.operands:
            return self.registers[self.operands[operand]]
        return operand


    def voer_uit(self, instruction, operand):
        print(f'Wordt uitgevoerd: instructie = {instruction}, operand = {operand}')

        match instruction:
            case 0: # adv

                self.registers['A'] //= (2 ** self.get_register_or_literal(operand))
                self.instruction_pointer += 2

            case 1: # bxl
                self.registers['B'] = self.registers['B'] ^ operand
                self.instruction_pointer += 2

            case 2: # bst
                self.registers['B'] = self.get_register_or_literal(operand) % 8
                self.instruction_pointer += 2

            case 3: #jnz
                if self.registers['A'] == 0:
                    self.instruction_pointer += 2
                else:
                    self.instruction_pointer = operand
            case 4:
                self.registers['B'] = self.registers['B'] ^ self.registers['C']
                self.instruction_pointer += 2

            case 5:
                self.output.append(str(self.get_register_or_literal(operand) % 8))
                self.instruction_pointer += 2

            case 6:
                self.registers['B'] = int(self.registers['A'] / (2 ** self.get_register_or_literal(operand)))
                self.instruction_pointer += 2

            case 7:
                self.registers['C'] = int(self.registers['A'] / (2 ** self.get_register_or_literal(operand)))
                self.instruction_pointer += 2

        print(self.registers)
        print('__________________________________________________________________')

computer = Computer(r)
computer.run(program)
