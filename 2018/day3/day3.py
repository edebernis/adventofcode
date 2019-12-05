#!/usr/bin/python3

import re


class Claim:
    def __init__(self, claim_str):
        match = re.search(
                 r'^#([0-9]+)\s@\s([0-9]+),([0-9]+):\s([0-9]+)x([0-9]+)$',
                 claim_str)
        self.id, self.left, self.top, self.width, self.height = \
            map(int, match.groups())

    def iter_coords(self):
        for x in range(self.left + 1, self.left + self.width + 1):
            for y in range(self.top + 1, self.top + self.height + 1):
                yield x, y


def get_overlapping_coords(claims):
    grid = {}
    for claim in claims:
        for coord in claim.iter_coords():
            if coord in grid:
                grid[coord] += 1
            else:
                grid[coord] = 1

    for coord, count in grid.items():
        if count > 1:
            yield coord


def get_nonoverlapping_claims(claims):
    grid = {}
    for claim in claims:
        for coord in claim.iter_coords():
            if coord in grid:
                grid[coord] += 1
            else:
                grid[coord] = 1

    for claim in claims:
        for coord in claim.iter_coords():
            if grid[coord] > 1:
                break
        else:
            yield claim


# Part 1 - Test cases
claim_strs = ['#1 @ 1,3: 4x4', '#2 @ 3,1: 4x4', '#3 @ 5,5: 2x2']
claims = [Claim(s) for s in claim_strs]
assert len(list(get_overlapping_coords(claims))) == 4

# Part 1 - Main
claim_strs = open('input_part1').readlines()
claims = [Claim(s) for s in claim_strs]
print('Part 1 answer: {0}'.format(len(list(get_overlapping_coords(claims)))))

# Part 2 - Test cases
claim_strs = ['#1 @ 1,3: 4x4', '#2 @ 3,1: 4x4', '#3 @ 5,5: 2x2']
claims = [Claim(s) for s in claim_strs]
nonoverlapping_claims = list(get_nonoverlapping_claims(claims))
assert len(nonoverlapping_claims) == 1
assert nonoverlapping_claims[0].id == 3

# Part 2 - Main
claim_strs = open('input_part1').readlines()
claims = [Claim(s) for s in claim_strs]
nonoverlapping_claims = list(get_nonoverlapping_claims(claims))
print('Part 2 answer: {0}'.format(nonoverlapping_claims[0].id))
