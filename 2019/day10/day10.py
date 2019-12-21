#!/usr/bin/python3


class Asteroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vaporized = False
        self.station = None

    def __lt__(self, other):
        if self.x - self.station.x >= 0 and other.x - self.station.x < 0:
            return True
        if self.x - self.station.x < 0 and other.x - self.station.x >= 0:
            return False
        if self.x - self.station.x == 0 and other.x - self.station.x == 0:
            return self.y < other.y

        det = (self.x - self.station.x) * (other.y - self.station.y) - \
              (other.x - self.station.x) * (self.y - self.station.y)
        return det > 0

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return 'A(%d,%d)' % (self.x, self.y)

    def vaporize(self):
        self.vaporized = True

    def intersect(self, a1, a2):
        aligned = (self.x - a1.x) * (a2.y - a1.y) - \
                  (self.y - a1.y) * (a2.x - a1.x) == 0
        if not aligned:
            return False

        k1 = (a2.x - a1.x) * (self.x - a1.x) + (a2.y - a1.y) * (self.y - a1.y)
        k2 = (a2.x - a1.x) * (a2.x - a1.x) + (a2.y - a1.y) * (a2.y - a1.y)
        in_between = 0 < k1 and k1 < k2
        return in_between

    def get_asteroids_in_sight(self, asteroids):
        for a1 in asteroids:
            if a1 != self and not a1.vaporized:
                for a2 in asteroids:
                    if a2 not in (self, a1) and \
                       not a2.vaporized and \
                       a2.intersect(self, a1):
                        break
                else:
                    yield a1


def load_asteroids(map_str):
    return [Asteroid(x, y) for y, row in enumerate(map_str.split('\n'))
            for x, c in enumerate(row) if c == '#']


def get_max_asteroids_in_sight(asteroids):
    return max([len(list(a.get_asteroids_in_sight(asteroids)))
                for a in asteroids])


def get_monitoring_station(asteroids):
    d = {}
    for a in asteroids:
        in_sight = list(a.get_asteroids_in_sight(asteroids))
        d[len(in_sight)] = (a, in_sight)

    return d[max(d.keys())]


def vaporize(asteroids):
    count = 0
    station, in_sight = get_monitoring_station(asteroids)
    while in_sight:
        for a in in_sight:
            a.station = station
        in_sight.sort()
        for a in in_sight:
            a.vaporize()
            count += 1
            if count == 200:
                return a
        in_sight = list(station.get_asteroids_in_sight(asteroids))


# Part 1 - Test cases
map_input = \
 """.#..#
.....
#####
....#
...##"""
assert get_max_asteroids_in_sight(load_asteroids(map_input)) == 8

map_input = \
 """......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####"""
assert get_max_asteroids_in_sight(load_asteroids(map_input)) == 33

map_input = \
 """#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###."""
assert get_max_asteroids_in_sight(load_asteroids(map_input)) == 35

map_input = \
 """.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#.."""
assert get_max_asteroids_in_sight(load_asteroids(map_input)) == 41

map_input = \
 """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""
# assert get_max_asteroids_in_sight(load_asteroids(map_input)) == 210

# Part 1 - Main
# map_str = open('input_part1').read()
# print('Part 1 answer: {0}'.format(
#      get_max_asteroids_in_sight(load_asteroids(map_str))))

# Part 2 - Test cases
map_input = \
 """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""
asteroids = load_asteroids(map_input)
# vaporize(asteroids)

# Part 2 - Main
map_str = open('input_part1').read()
asteroids = load_asteroids(map_str)
a = vaporize(asteroids)
print('Part 2 answer: {0}'.format(a.x * 100 + a.y))
