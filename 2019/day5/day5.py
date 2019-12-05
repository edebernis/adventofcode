#!/usr/bin/python3


class Computer:
    def __init__(self):
        self.opcode_pos = None

    def run_program(self, program):
        self.opcode_pos = 0
        while program[self.opcode_pos] != 99:
            self._run(program)

        return program

    def _run(self, program):
        opcode = int(str(program[self.opcode_pos])[-2:])
        modes = list(reversed(str(program[self.opcode_pos])[:-2]))
        try:
            {
                1: self._add,
                2: self._multiply,
                3: self._input,
                4: self._output,
                5: self._jump_if_true,
                6: self._jump_if_false,
                7: self._less_than,
                8: self._equals
            }[opcode](program, modes)
        except KeyError:
            raise Exception('Something went wrong')

    def _get_value(self, program, modes, offset):
        try:
            mode = int(modes[offset - 1])
        except IndexError:
            mode = 0

        if mode == 0:
            return program[program[self.opcode_pos + offset]]
        elif mode == 1:
            return program[self.opcode_pos + offset]
        else:
            raise Exception('Unknown mode : {0}'.format(mode))

    def _add(self, program, modes):
        a = self._get_value(program, modes, offset=1)
        b = self._get_value(program, modes, offset=2)
        program[program[self.opcode_pos + 3]] = a + b
        self.opcode_pos += 4

    def _multiply(self, program, modes):
        a = self._get_value(program, modes, offset=1)
        b = self._get_value(program, modes, offset=2)
        program[program[self.opcode_pos + 3]] = a * b
        self.opcode_pos += 4

    def _input(self, program, modes):
        program[program[self.opcode_pos + 1]] = int(input('INPUT: '))
        self.opcode_pos += 2

    def _output(self, program, modes):
        value = self._get_value(program, modes, offset=1)
        print('OUTPUT: {0}'.format(value))
        self.opcode_pos += 2

    def _jump_if_true(self, program, modes):
        value = self._get_value(program, modes, offset=1)
        if value:
            self.opcode_pos = self._get_value(program, modes, offset=2)
        else:
            self.opcode_pos += 3

    def _jump_if_false(self, program, modes):
        value = self._get_value(program, modes, offset=1)
        if not value:
            self.opcode_pos = self._get_value(program, modes, offset=2)
        else:
            self.opcode_pos += 3

    def _less_than(self, program, modes):
        a = self._get_value(program, modes, offset=1)
        b = self._get_value(program, modes, offset=2)
        program[program[self.opcode_pos + 3]] = 1 if a < b else 0
        self.opcode_pos += 4

    def _equals(self, program, modes):
        a = self._get_value(program, modes, offset=1)
        b = self._get_value(program, modes, offset=2)
        program[program[self.opcode_pos + 3]] = 1 if a == b else 0
        self.opcode_pos += 4


# Part 1 - Test cases
computer = Computer()
computer.run_program([1002, 4, 3, 4, 33])

# Part 1 - Main
program = list(map(int, open('input_part1').read().split(',')))
Computer().run_program(program)

# Part 2 - Test cases
computer = Computer()
computer.run_program([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8])
computer.run_program([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8])
computer.run_program([3, 3, 1108, -1, 8, 3, 4, 3, 99])
computer.run_program([3, 3, 1107, -1, 8, 3, 4, 3, 99])
computer.run_program(
    [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9])
computer.run_program([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1])
computer.run_program(
    [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
     1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
     999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99])

# Part 2 - Main
program = list(map(int, open('input_part1').read().split(',')))
Computer().run_program(program)
