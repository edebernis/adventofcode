#!/usr/bin/python3

from itertools import permutations
from collections import deque
import string
import threading


class Computer(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(),
                 kwargs=None, verbose=None):
        super(Computer, self).__init__(group=group, target=target,
                                       name=name)
        self.program = args[0]
        self.inputs = args[1]
        self.outputs = args[2]
        self.verbose = verbose
        self.opcode_pos = None

    def run(self):
        self.opcode_pos = 0
        while self.program[self.opcode_pos] != 99:
            self._run()

    def _run(self):
        opcode = int(str(self.program[self.opcode_pos])[-2:])
        modes = list(reversed(str(self.program[self.opcode_pos])[:-2]))
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
            }[opcode](modes)
        except KeyError:
            raise Exception('Something went wrong')

    def _get_value(self, modes, offset):
        try:
            mode = int(modes[offset - 1])
        except IndexError:
            mode = 0

        if mode == 0:
            return self.program[self.program[self.opcode_pos + offset]]
        elif mode == 1:
            return self.program[self.opcode_pos + offset]
        else:
            raise Exception('Unknown mode : {0}'.format(mode))

    def _get_input(self):
        while True:
            if self.inputs:
                return int(self.inputs.popleft())
            if self.verbose:
                print('Amplifier {0} wait input'.format(self.name))

    def _add(self, modes):
        a = self._get_value(modes, offset=1)
        b = self._get_value(modes, offset=2)
        self.program[self.program[self.opcode_pos + 3]] = a + b
        self.opcode_pos += 4

    def _multiply(self, modes):
        a = self._get_value(modes, offset=1)
        b = self._get_value(modes, offset=2)
        self.program[self.program[self.opcode_pos + 3]] = a * b
        self.opcode_pos += 4

    def _input(self, modes):
        self.program[self.program[self.opcode_pos + 1]] = self._get_input()
        self.opcode_pos += 2

    def _output(self, modes):
        value = self._get_value(modes, offset=1)
        self.outputs.append(value)
        if self.verbose:
            print('Amplifier {0} added output'.format(self.name))
        self.opcode_pos += 2

    def _jump_if_true(self, modes):
        value = self._get_value(modes, offset=1)
        if value:
            self.opcode_pos = self._get_value(modes, offset=2)
        else:
            self.opcode_pos += 3

    def _jump_if_false(self, modes):
        value = self._get_value(modes, offset=1)
        if not value:
            self.opcode_pos = self._get_value(modes, offset=2)
        else:
            self.opcode_pos += 3

    def _less_than(self, modes):
        a = self._get_value(modes, offset=1)
        b = self._get_value(modes, offset=2)
        self.program[self.program[self.opcode_pos + 3]] = 1 if a < b else 0
        self.opcode_pos += 4

    def _equals(self, modes):
        a = self._get_value(modes, offset=1)
        b = self._get_value(modes, offset=2)
        self.program[self.program[self.opcode_pos + 3]] = 1 if a == b else 0
        self.opcode_pos += 4


def test_sequence(program, sequence):
    ea = deque([sequence[0], 0])
    ab = deque([sequence[1]])
    bc = deque([sequence[2]])
    cd = deque([sequence[3]])
    de = deque([sequence[4]])
    inputs = [ea, ab, bc, cd, de]
    outputs = [ab, bc, cd, de, ea]
    amplifiers = [Computer(name=string.ascii_uppercase[i],
                           args=(program.copy(), inputs[i], outputs[i]))
                  for i in range(5)]

    for a in amplifiers:
        a.start()
    for a in amplifiers:
        a.join()

    return outputs[4].popleft()


# Part 1 - Test cases
program = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
assert test_sequence(program, [4, 3, 2, 1, 0]) == 43210
program = [3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23,
           1, 24, 23, 23, 4, 23, 99, 0, 0]
assert test_sequence(program, [0, 1, 2, 3, 4]) == 54321
program = [3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33,
           1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0]
assert test_sequence(program, [1, 0, 4, 3, 2]) == 65210

# Part 1 - Main
program = list(map(int, open('input_part1').read().split(',')))
print('Part 1 answer: {0}'.format(
      max([test_sequence(program, seq)
          for seq in permutations(range(5))])))

# Part 2 - Test cases
program = [3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26,
           27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5]
assert test_sequence(program, [9, 8, 7, 6, 5]) == 139629729
program = [3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55,
           1005, 55, 26, 1001, 54, -5, 54, 1105, 1, 12, 1, 53, 54, 53,
           1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4, 53, 1001,
           56, -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10]
assert test_sequence(program, [9, 7, 8, 5, 6]) == 18216

# Part 2 - Main
program = list(map(int, open('input_part1').read().split(',')))
print('Part 2 answer: {0}'.format(
      max([test_sequence(program, seq)
          for seq in permutations(range(5, 10))])))
