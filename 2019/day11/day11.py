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

    def is_running(self):
        return self.isAlive()

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


class Direction:
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Color:
    BLACK = 0
    WHITE = 1


class Robot:
    def __init__(self):
        self.direction = Direction.UP
        self.pos = (0, 0)

    def _get_output(self, outputs):
        while True:
            try:
                return outputs.popleft()
            except IndexError:
                continue

    def turn_left(self):
        if self.direction == Direction.UP:
            self.direction = Direction.LEFT
        elif self.direction == Direction.DOWN:
            self.direction = Direction.RIGHT
        elif self.direction == Direction.LEFT:
            self.direction = Direction.DOWN
        elif self.direction == Direction.RIGHT:
            self.direction = Direction.UP
        else:
            raise Exception('Unknown direction : %d' % self.direction)

    def turn_right(self):
        if self.direction == Direction.UP:
            self.direction = Direction.RIGHT
        elif self.direction == Direction.DOWN:
            self.direction = Direction.LEFT
        elif self.direction == Direction.LEFT:
            self.direction = Direction.UP
        elif self.direction == Direction.RIGHT:
            self.direction = Direction.DOWN
        else:
            raise Exception('Unknown direction : %d' % self.direction)

    def look(self, inputs, panels):
        try:
            color = panels[self.pos[0]][self.pos[1]]
        except KeyError:
            color = Color.BLACK

        inputs.append(color)

    def paint(self, outputs, panels):
        color = self._get_output(outputs)
        if not (self.pos[0] in panels):
            panels[self.pos[0]] = {}

        if color == 0:
            panels[self.pos[0]][self.pos[1]] = Color.BLACK
        elif color == 1:
            panels[self.pos[0]][self.pos[1]] = Color.WHITE
        else:
            raise Exception('Unknown color : %d' % color)

    def move(self, outputs):
        turn = self._get_output(outputs)
        if turn == 0:
            self.turn_left()
        elif turn == 1:
            self.turn_right()
        else:
            raise Exception('Unknown turn : %d' % turn)

        if self.direction == Direction.UP:
            self.pos = (self.pos[0], self.pos[1] + 1)
        elif self.direction == Direction.DOWN:
            self.pos = (self.pos[0], self.pos[1] - 1)
        elif self.direction == Direction.LEFT:
            self.pos = (self.pos[0] - 1, self.pos[1])
        elif self.direction == Direction.RIGHT:
            self.pos = (self.pos[0] + 1, self.pos[1])
        else:
            raise Exception('Unknown direction')

    def _start_computer(self, program, inputs, outputs):
        c = Computer(args=(program, inputs, outputs))
        c.start()
        return c

    def _do(self, inputs, outputs, panels):
        self.look(inputs, panels)
        self.paint(outputs, panels)
        self.move(outputs)

    def run(self, program, panels):
        # Start computer
        inputs = deque([])
        outputs = deque([])
        computer = self._start_computer(program, inputs, outputs)

        # Run robot
        while True:
            self._do(inputs, outputs, panels)
            if not computer.is_running():
                break

        return panels


def print_panels(panels):
    min_x = min(panels.keys())
    max_x = max(panels.keys())
    all_y = [y for x in panels.keys() for y in panels[x].keys()]
    min_y = min(all_y)
    max_y = max(all_y)

    for y in range(max_y, min_y-1, -1):
        line = ''
        for x in range(min_x, max_x+1):
            try:
                line += '#' if panels[x][y] == Color.WHITE else ' '
            except KeyError:
                line += ' '
        print(line)


# Part 1 - Main
program = list(map(int, open('input_part1').read().strip().split(',')))
panels = Robot().run(program, {})
print('Part 1 answer: {0}'.format(
      sum([len(panels[k].keys()) for k in panels.keys()])))

# Part 2 - Main
program = list(map(int, open('input_part1').read().strip().split(',')))
panels = Robot().run(program, {0: {0: Color.WHITE}})
print_panels(panels)
