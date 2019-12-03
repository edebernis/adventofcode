#!/usr/bin/python3


class Wire:
    def __init__(self, path):
        self.path = path
        self.current_coord = (0, 0)
        self.coords = []

        self._set_coords()

    def _set_coords(self):
        for move in self.path:
            direction = move[0]
            number_of_moves = int(move[1:])

            for _ in range(number_of_moves):
                try:
                    {'U': self._up,
                     'D': self._down,
                     'L': self._left,
                     'R': self._right}[direction]()
                except Exception:
                    raise Exception('Unknown direction: {0}'.format(direction))

    def _move(self, x, y):
        self.current_coord = (x, y)
        self.coords.append(self.current_coord)

    def _up(self):
        return self._move(self.current_coord[0], self.current_coord[1]+1)

    def _down(self):
        return self._move(self.current_coord[0], self.current_coord[1]-1)

    def _left(self):
        return self._move(self.current_coord[0]-1, self.current_coord[1])

    def _right(self):
        return self._move(self.current_coord[0]+1, self.current_coord[1])

    def get_number_of_steps_to_coord(self, target_coord):
        for steps, coord in enumerate(self.coords, start=1):
            if coord == target_coord:
                return steps


def get_wires_crossings(wire1, wire2):
    return set(wire1.coords) & set(wire2.coords)


def calc_manhattan_distance(coord):
    return abs(coord[0]) + abs(coord[1])


# Part 1 - Test cases
wire1 = Wire("R75,D30,R83,U83,L12,D49,R71,U7,L72".split(','))
wire2 = Wire("U62,R66,U55,R34,D71,R55,D58,R83".split(','))
assert min([calc_manhattan_distance(coord)
            for coord in get_wires_crossings(wire1, wire2)]) == 159
wire1 = Wire("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51".split(','))
wire2 = Wire("U98,R91,D20,R16,D67,R40,U7,R15,U6,R7".split(','))
assert min([calc_manhattan_distance(coord)
            for coord in get_wires_crossings(wire1, wire2)]) == 135

# Part 1 - Main
paths = open('input_part1').readlines()
wire1 = Wire(paths[0].split(','))
wire2 = Wire(paths[1].split(','))
print('Part 1 answer: {0}'.format(min([calc_manhattan_distance(coord)
      for coord in get_wires_crossings(wire1, wire2)])))

# Part 2 - Test cases
wire1 = Wire("R75,D30,R83,U83,L12,D49,R71,U7,L72".split(','))
wire2 = Wire("U62,R66,U55,R34,D71,R55,D58,R83".split(','))
assert min([wire1.get_number_of_steps_to_coord(crossing) +
            wire2.get_number_of_steps_to_coord(crossing)
            for crossing in get_wires_crossings(wire1, wire2)]) == 610
wire1 = Wire("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51".split(','))
wire2 = Wire("U98,R91,D20,R16,D67,R40,U7,R15,U6,R7".split(','))
assert min([wire1.get_number_of_steps_to_coord(crossing) +
            wire2.get_number_of_steps_to_coord(crossing)
            for crossing in get_wires_crossings(wire1, wire2)]) == 410

# Part 2 - Main
paths = open('input_part1').readlines()
wire1 = Wire(paths[0].split(','))
wire2 = Wire(paths[1].split(','))
print('Part 2 answer: {0}'.format(
      min([wire1.get_number_of_steps_to_coord(crossing) +
           wire2.get_number_of_steps_to_coord(crossing)
           for crossing in get_wires_crossings(wire1, wire2)])))
