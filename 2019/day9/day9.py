#!/usr/bin/python3

from collections import deque
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
        self.relative_base = None
        self.memory = None

    def run(self):
        self.opcode_pos = 0
        self.relative_base = 0
        self.memory = {k: v for k, v in enumerate(self.program)}
        while self.program[self.opcode_pos] != 99:
            self._run()

    def _run(self):
        opcode = int(str(self.program[self.opcode_pos])[-2:])
        modes = list(reversed(str(self.program[self.opcode_pos])[:-2]))

        if self.verbose:
            print('Run opcode {0}, modes {1}'.format(opcode, modes))

        try:
            {
                1: self._add,
                2: self._multiply,
                3: self._input,
                4: self._output,
                5: self._jump_if_true,
                6: self._jump_if_false,
                7: self._less_than,
                8: self._equals,
                9: self._set_relative_base
            }[opcode](modes)
        except KeyError:
            raise Exception('Something went wrong')

    def _get_value_address(self, mode, offset):
        if mode == 0:
            return self.program[self.opcode_pos + offset]
        elif mode == 1:
            return self.opcode_pos + offset
        elif mode == 2:
            return self.program[self.opcode_pos + offset] + self.relative_base
        else:
            raise Exception('Unknown mode : {0}'.format(mode))

    def _get_mode(self, modes, offset):
        try:
            return int(modes[offset - 1])
        except IndexError:
            return 0

    def _get_value(self, modes, offset):
        mode = self._get_mode(modes, offset)
        address = self._get_value_address(mode, offset)
        value = self.memory.get(address, 0)

        if self.verbose:
            print('Get Offset {0}, address {1}, value {2}'
                  .format(offset, address, value))

        return value

    def _set_value(self, value, modes, offset):
        mode = self._get_mode(modes, offset)
        address = self._get_value_address(mode, offset)
        self.memory[address] = value

        if self.verbose:
            print('Set Offset {0}, address {1}, value {2}'
                  .format(offset, address, value))

    def _get_input(self):
        while True:
            if self.inputs:
                return int(self.inputs.popleft())
            if self.verbose:
                print('Computer {0} wait input'.format(self.name))

    def _add(self, modes):
        a = self._get_value(modes, offset=1)
        b = self._get_value(modes, offset=2)
        self._set_value(a + b, modes, offset=3)
        self.opcode_pos += 4

    def _multiply(self, modes):
        a = self._get_value(modes, offset=1)
        b = self._get_value(modes, offset=2)
        self._set_value(a * b, modes, offset=3)
        self.opcode_pos += 4

    def _input(self, modes):
        self._set_value(self._get_input(), modes, offset=1)
        self.opcode_pos += 2

    def _output(self, modes):
        value = self._get_value(modes, offset=1)
        self.outputs.append(value)
        if self.verbose:
            print('Computer {0} added output'.format(self.name))
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
        self._set_value(int(a < b), modes, offset=3)
        self.opcode_pos += 4

    def _equals(self, modes):
        a = self._get_value(modes, offset=1)
        b = self._get_value(modes, offset=2)
        self._set_value(int(a == b), modes, offset=3)
        self.opcode_pos += 4

    def _set_relative_base(self, modes):
        self.relative_base += self._get_value(modes, offset=1)
        if self.verbose:
            print('Relative base : {0}'.format(self.relative_base))
        self.opcode_pos += 2


def run_program(program, inputs, verbose=None):
    outputs = deque([])
    c = Computer(args=(program, inputs, outputs), verbose=verbose)
    c.start()
    c.join()
    return list(outputs)


# Part 1 - Test cases
program = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006,
           101, 0, 99]
assert run_program(program, deque([])) == \
    [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
program = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
assert len(str(run_program(program, deque([]))[0])) == 16
program = [104, 1125899906842624, 99]
assert run_program(program, deque([])) == [1125899906842624]

# Part 1 - Main
program = list(map(int, open('input_part1').read().strip().split(',')))
print('Part 1 answer: {0}'.format(run_program(program, deque([1]))[0]))

# Part 2 - Main
program = list(map(int, open('input_part1').read().strip().split(',')))
print('Part 2 answer: {0}'.format(run_program(program, deque([2]))[0]))
