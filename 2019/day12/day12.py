#!/usr/bin/python3

import re
import math
import itertools


class Moon:
    def __init__(self, x, y, z):
        self.pos = [int(x), int(y), int(z)]
        self.vel = [0, 0, 0]

    def __str__(self):
        return "pos=<x={}, y={}, z={}>, vel=<x={}, y={}, z={}>" \
               .format(*(self.pos + self.vel))

    def apply_gravity_by_coord(self, moon, i):
        if self.pos[i] < moon.pos[i]:
            self.vel[i] += 1
            moon.vel[i] -= 1
        elif self.pos[i] > moon.pos[i]:
            self.vel[i] -= 1
            moon.vel[i] += 1

    def apply_gravity(self, moon):
        for i in range(3):
            self.apply_gravity_by_coord(moon, i)

    def apply_velocity_by_coord(self, i):
        self.pos[i] += self.vel[i]

    def apply_velocity(self):
        for i in range(3):
            self.apply_velocity_by_coord(i)

    def total_energy_by_coord(self, i):
        return abs(self.pos[i]) * abs(self.vel[i])

    def total_energy(self):
        return sum(map(abs, self.pos)) * sum(map(abs, self.vel))


def make_step(moons):
    for m1, m2 in itertools.combinations(moons, 2):
        m1.apply_gravity(m2)
    for m in moons:
        m.apply_velocity()


def make_step_by_coord(moons, i):
    for m1, m2 in itertools.combinations(moons, 2):
        m1.apply_gravity_by_coord(m2, i)
    for m in moons:
        m.apply_velocity_by_coord(i)


def fix_state_by_coord(moons, i):
    orig = [m.pos[i] for m in moons]
    step = 0
    while True:
        make_step_by_coord(moons, i)
        step += 1
        for j, moon in enumerate(moons):
            if moon.vel[i] != 0 or moon.pos[i] != orig[j]:
                break
        else:
            return step


def lcm(l):
    if not l:
        raise Exception('Empty list')
    elif len(l) == 1:
        return l
    elif len(l) == 2:
        return int((l[0]*l[1]) / math.gcd(*l))
    else:
        r = lcm(l[1:])
        return int((l[0]*r) / math.gcd(l[0], r))


def load_moons():
    moons = []
    for l in open('input_part1').readlines():
        m = re.search(r'<x=([0-9\-]+), y=([0-9\-]+), z=([0-9\-]+)>', l)
        moons.append(Moon(*m.groups()))
    return moons


# Part 1 - Test cases
moons = [Moon(-1, 0, 2), Moon(2, -10, -7), Moon(4, -8, 8), Moon(3, 5, -1)]
for _ in range(1, 11):
    make_step(moons)
assert sum(m.total_energy() for m in moons) == 179

moons = [Moon(-8, -10, 0), Moon(5, 5, 10), Moon(2, -7, 3), Moon(9, -8, -3)]
for _ in range(1, 101):
    make_step(moons)
assert sum(m.total_energy() for m in moons) == 1940

# Part 1 - Main
moons = load_moons()
for _ in range(1, 1001):
    make_step(moons)
print('Part 1 answer: {}'.format(sum(m.total_energy() for m in moons)))

# Part 2 - Test cases
moons = [Moon(-1, 0, 2), Moon(2, -10, -7), Moon(4, -8, 8), Moon(3, 5, -1)]
assert lcm([fix_state_by_coord(moons, i) for i in range(3)]) == 2772

moons = [Moon(-8, -10, 0), Moon(5, 5, 10), Moon(2, -7, 3), Moon(9, -8, -3)]
assert lcm([fix_state_by_coord(moons, i) for i in range(3)]) == 4686774924

# Part 2 - Main
moons = load_moons()
print('Part 2 answer: {}'.format(
      lcm([fix_state_by_coord(moons, i) for i in range(3)])))
